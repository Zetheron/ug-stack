"""Autentikasi dan manajemen akun: PBKDF2, kunci akun persisten, ganti password, kelola pengguna."""
import csv
import hashlib
import hmac
import io
import os
import secrets
import string
import time
from datetime import datetime

from . import admin_code, audit, enrollment, progress, quiz, settings, storage
from .roles import ROLES, is_admin
from .storage import StorageError
from .validators import validate_password, validate_username

ITERATIONS = 100_000
MAX_ATTEMPTS = 3
LOCK_SECONDS = 30
USERS_FILE = "users.json"
LOCK_FILE = "lockouts.json"
MAX_BATCH = 100
DEFAULT_ADMIN_PASSWORD = "Admin123"
_DUMMY_SALT = "00" * 16          # dipakai agar waktu respons sama untuk username tak dikenal


def hash_password(password: str, salt_hex: str = None):
    salt = bytes.fromhex(salt_hex) if salt_hex else os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, ITERATIONS)
    return salt.hex(), digest.hex()


def _new_user(username, password, role, must_change=False):
    salt, pw_hash = hash_password(password)
    return {"username": username, "salt": salt, "password_hash": pw_hash, "role": role,
            "created_at": datetime.now().isoformat(timespec="seconds"), "must_change": must_change}


def _public(user: dict) -> dict:
    return {"username": user["username"], "role": user["role"], "must_change": bool(user.get("must_change"))}


def _find(users: list, username: str):
    for u in users:                       # pencarian linear
        if u["username"].lower() == username.lower():
            return u
    return None


def _verify(user, password: str) -> bool:
    if user is None:
        hash_password(password, _DUMMY_SALT)          # samakan waktu proses
        return False
    _, digest = hash_password(password, user["salt"])
    return hmac.compare_digest(digest, user["password_hash"])


def init_data():
    """Buat admin bawaan; tandai wajib ganti password bila admin masih memakai password bawaan."""
    with storage.LOCK:
        users = storage.load_json(USERS_FILE, [])
        changed = False
        if not users:
            seed = os.getenv("UG_ADMIN_PASSWORD") or DEFAULT_ADMIN_PASSWORD     # server online: set UG_ADMIN_PASSWORD
            if not validate_password(seed)[0]:
                seed = DEFAULT_ADMIN_PASSWORD
            users.append(_new_user("admin", seed, "admin", must_change=(seed == DEFAULT_ADMIN_PASSWORD)))
            changed = True
        else:
            for u in users:
                if u["role"] == "admin" and not u.get("must_change") and _verify(u, DEFAULT_ADMIN_PASSWORD):
                    u["must_change"] = True
                    changed = True
        if changed:
            storage.save_json(USERS_FILE, users)


# ------------------------------------------------------------------ kunci akun (disimpan ke file)
def _load_locks() -> dict:
    try:
        return storage.load_json(LOCK_FILE, {})
    except StorageError:
        return {}


def _save_locks(locks: dict) -> None:
    try:
        storage.save_json(LOCK_FILE, locks)
    except StorageError:
        pass


def reset_lock():
    _save_locks({})


# ------------------------------------------------------------------ registrasi dan login
def register(username: str, password: str, confirm: str):
    if not settings.registration_open():
        return False, "Pendaftaran mandiri sedang ditutup. Hubungi admin untuk dibuatkan akun."
    ok, msg = validate_username(username)
    if not ok:
        return False, msg
    ok, msg = validate_password(password)
    if not ok:
        return False, msg
    if password != confirm:
        return False, "Konfirmasi password tidak sama."
    try:
        with storage.LOCK:
            users = storage.load_json(USERS_FILE, [])
            if _find(users, username.strip()):
                return False, "Username sudah dipakai."
            users.append(_new_user(username.strip(), password, "mahasiswa"))
            storage.save_json(USERS_FILE, users)
    except StorageError as e:
        return False, str(e)
    audit.log(username.strip(), "REGISTER", "akun mahasiswa baru")
    return True, "Registrasi berhasil. Silakan login."


def login(username: str, password: str, expected_role: str = None, allow_admin: bool = False):
    """Mengembalikan (ok, pesan, user_publik|None).
    expected_role: peran yang dipilih di halaman login (mahasiswa/dosen); akun dengan peran lain ditolak.
    Akun admin TIDAK boleh masuk dengan password (allow_admin=False); admin memakai login_admin() dengan kode berputar."""
    username = (username or "").strip()
    if not username or not password:
        return False, "Username dan password wajib diisi.", None
    key = username.lower()
    now = time.time()
    locks = _load_locks()
    rec = locks.get(key, {"count": 0, "locked_until": 0})
    if rec["locked_until"] > now:
        return False, f"Akun terkunci sementara. Coba lagi dalam {int(rec['locked_until'] - now) + 1} detik.", None
    try:
        users = storage.load_json(USERS_FILE, [])
    except StorageError as e:
        return False, str(e), None
    user = _find(users, username)
    if _verify(user, password):
        if key in locks:
            locks.pop(key)
            _save_locks(locks)
        if user["role"] == "admin" and not allow_admin:            # admin hanya lewat kode khusus
            audit.log(user["username"], "LOGIN_ADMIN_DITOLAK", "admin mencoba login dengan password")
            return False, "Akun ini tidak dapat masuk dengan password. Gunakan jalur login khusus admin.", None
        if expected_role and user["role"] != expected_role:        # password benar tetapi peran yang dipilih salah
            audit.log(user["username"], "LOGIN_PERAN_SALAH", f"memilih {expected_role}, akun {user['role']}")
            return False, f"Akun ini terdaftar sebagai {user['role']}. Pilih peran {user['role']} di halaman login.", None
        audit.log(user["username"], "LOGIN_OK")
        return True, "Login berhasil.", _public(user)
    rec["count"] += 1
    audit.log(username, "LOGIN_GAGAL", f"percobaan ke-{rec['count']}")
    if rec["count"] >= MAX_ATTEMPTS:
        locks[key] = {"count": 0, "locked_until": now + LOCK_SECONDS}
        _save_locks(locks)
        return False, f"Terlalu banyak percobaan gagal. Akun dikunci {LOCK_SECONDS} detik.", None
    locks[key] = {"count": rec["count"], "locked_until": 0}
    _save_locks(locks)
    return False, f"Username atau password salah. Sisa percobaan: {MAX_ATTEMPTS - rec['count']}.", None


def login_admin(username: str, code_text: str, now: float = None):
    """Login admin dengan kode berputar 60 detik (lihat services/admin_code.py). Mengembalikan (ok, pesan, user|None)."""
    username = (username or "admin").strip() or "admin"
    ok, msg = admin_code.verify(code_text, now)
    if not ok:
        return False, msg, None
    try:
        users = storage.load_json(USERS_FILE, [])
    except StorageError as e:
        return False, str(e), None
    user = _find(users, username)
    if user is None or user["role"] != "admin":
        audit.log("(admin-kode)", "LOGIN_ADMIN_GAGAL", f"akun admin '{username}' tidak ditemukan")
        return False, "Akun admin tidak ditemukan.", None
    audit.log(user["username"], "LOGIN_ADMIN_KODE")
    result = _public(user)
    result["must_change"] = False                                   # admin tidak memakai password
    return True, "Login admin berhasil.", result


def log_logout(username: str) -> None:
    audit.log(username, "LOGOUT")


# ------------------------------------------------------------------ akun sendiri
def change_password(username: str, old: str, new: str, confirm: str):
    ok, msg = validate_password(new)
    if not ok:
        return False, msg
    if new != confirm:
        return False, "Konfirmasi password tidak sama."
    try:
        with storage.LOCK:
            users = storage.load_json(USERS_FILE, [])
            user = _find(users, username)
            if user is None or not _verify(user, old):
                return False, "Password lama salah."
            if old == new:
                return False, "Password baru harus berbeda dari password lama."
            user["salt"], user["password_hash"] = hash_password(new)
            user["must_change"] = False
            storage.save_json(USERS_FILE, users)
    except StorageError as e:
        return False, str(e)
    audit.log(username, "GANTI_PASSWORD")
    return True, "Password berhasil diubah."


# ------------------------------------------------------------------ manajemen pengguna (admin)
def list_users(actor):
    if not is_admin(actor):
        return []
    return [{"username": u["username"], "role": u["role"], "created_at": u["created_at"][:10],
             "must_change": bool(u.get("must_change"))} for u in storage.load_json(USERS_FILE, [])]


def _count_admins(users) -> int:
    return len([u for u in users if u["role"] == "admin"])


def reset_password(actor, target: str, temp_password: str):
    if not is_admin(actor):
        return False, "Hanya admin yang boleh mengelola pengguna."
    ok, msg = validate_password(temp_password)
    if not ok:
        return False, msg
    try:
        with storage.LOCK:
            users = storage.load_json(USERS_FILE, [])
            user = _find(users, target)
            if user is None:
                return False, "Pengguna tidak ditemukan."
            user["salt"], user["password_hash"] = hash_password(temp_password)
            user["must_change"] = True
            storage.save_json(USERS_FILE, users)
    except StorageError as e:
        return False, str(e)
    audit.log(actor["username"], "RESET_PASSWORD", target)
    return True, f"Password {target} direset. Pengguna wajib menggantinya saat login."


def set_role(actor, target: str, role: str):
    if not is_admin(actor):
        return False, "Hanya admin yang boleh mengelola pengguna."
    if role not in ROLES:
        return False, "Peran tidak valid."
    try:
        with storage.LOCK:
            users = storage.load_json(USERS_FILE, [])
            user = _find(users, target)
            if user is None:
                return False, "Pengguna tidak ditemukan."
            if user["role"] == "admin" and role != "admin" and _count_admins(users) <= 1:
                return False, "Admin terakhir tidak boleh diturunkan perannya."
            user["role"] = role
            storage.save_json(USERS_FILE, users)
    except StorageError as e:
        return False, str(e)
    audit.log(actor["username"], "UBAH_PERAN", f"{target} -> {role}")
    return True, f"Peran {target} menjadi {role}."


def delete_user(actor, target: str):
    if not is_admin(actor):
        return False, "Hanya admin yang boleh mengelola pengguna."
    if actor["username"].lower() == target.lower():
        return False, "Anda tidak dapat menghapus akun sendiri."
    try:
        with storage.LOCK:
            users = storage.load_json(USERS_FILE, [])
            user = _find(users, target)
            if user is None:
                return False, "Pengguna tidak ditemukan."
            if user["role"] == "admin" and _count_admins(users) <= 1:
                return False, "Admin terakhir tidak boleh dihapus."
            users.remove(user)
            storage.save_json(USERS_FILE, users)
            progress.remove_user(target)
            quiz.remove_user(target)
            enrollment.remove_user(target)
    except StorageError as e:
        return False, str(e)
    audit.log(actor["username"], "HAPUS_PENGGUNA", target)
    return True, f"Pengguna {target} dihapus."


def generate_password(length: int = 12) -> str:
    """Password acak yang kuat (mengandung huruf besar, kecil, dan angka; tanpa karakter membingungkan)."""
    letters = "".join(c for c in string.ascii_letters if c not in "lIO")
    digits = "23456789"
    while True:
        pw = "".join(secrets.choice(letters + digits) for _ in range(length))
        if any(c.islower() for c in pw) and any(c.isupper() for c in pw) and any(c.isdigit() for c in pw):
            return pw


def create_user(actor, username: str, role: str, temp_password: str = None):
    """Admin membuat akun (mahasiswa/dosen/admin). Mengembalikan (ok, pesan, password_sementara)."""
    if not is_admin(actor):
        return False, "Hanya admin yang boleh membuat akun.", None
    if role not in ROLES:
        return False, "Peran tidak valid.", None
    ok, msg = validate_username(username)
    if not ok:
        return False, msg, None
    password = (temp_password or "").strip() or generate_password()
    ok, msg = validate_password(password)
    if not ok:
        return False, msg, None
    try:
        with storage.LOCK:
            users = storage.load_json(USERS_FILE, [])
            if _find(users, username.strip()):
                return False, "Username sudah dipakai.", None
            users.append(_new_user(username.strip(), password, role, must_change=True))
            storage.save_json(USERS_FILE, users)
    except StorageError as e:
        return False, str(e), None
    audit.log(actor["username"], "BUAT_AKUN", f"{username.strip()} ({role})")
    return True, f"Akun {username.strip()} ({role}) dibuat. Berikan password sementara ini kepada pengguna.", password


def import_users_csv(actor, text: str):
    """Buat banyak akun sekaligus dari CSV (kolom: username, role[opsional]). Password dibuat otomatis.
    Mengembalikan (ok, pesan, laporan) dengan laporan {'created': [(username, role, password)], 'skipped': [(baris, alasan)]}."""
    if not is_admin(actor):
        return False, "Hanya admin yang boleh membuat akun.", None
    if not (text or "").strip():
        return False, "Teks CSV kosong.", None
    reader = csv.DictReader(io.StringIO(text.strip()))
    header = [h.strip().lower() for h in (reader.fieldnames or [])]
    if "username" not in header:
        return False, "Kolom wajib 'username' tidak ada.", None
    reader.fieldnames = header
    created, skipped = [], []
    try:
        with storage.LOCK:
            users = storage.load_json(USERS_FILE, [])
            for line, row in enumerate(reader, start=2):
                if len(created) >= MAX_BATCH:
                    skipped.append((line, f"melebihi batas {MAX_BATCH} akun per impor"))
                    break
                name = (row.get("username") or "").strip()
                role = (row.get("role") or "mahasiswa").strip().lower() or "mahasiswa"
                ok, msg = validate_username(name)
                if not ok:
                    skipped.append((line, msg))
                elif role not in ROLES:
                    skipped.append((line, f"peran '{role}' tidak valid"))
                elif _find(users, name):
                    skipped.append((line, "username sudah dipakai"))
                else:
                    pw = generate_password()
                    users.append(_new_user(name, pw, role, must_change=True))
                    created.append((name, role, pw))
            if created:
                storage.save_json(USERS_FILE, users)
    except StorageError as e:
        return False, str(e), None
    audit.log(actor["username"], "IMPOR_AKUN", f"{len(created)} dibuat, {len(skipped)} dilewati")
    return True, f"{len(created)} akun dibuat, {len(skipped)} baris dilewati.", {"created": created, "skipped": skipped}


def list_students():
    users = storage.load_json(USERS_FILE, [])
    return [u["username"] for u in users if u["role"] == "mahasiswa"]
