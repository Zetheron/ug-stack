"""Kode login admin yang berganti setiap 60 detik (HMAC-SHA256). Admin TIDAK login dengan password.

Kode dibuat oleh admin dari `tools/admin_generator.html` (atau `python tools/admin_code.py`) memakai kunci rahasia yang sama
dengan server. Kunci dibaca dari variabel lingkungan UG_ADMIN_KEY atau berkas admin_key.txt (tidak ikut ke GitHub).
Kode berlaku untuk menit saat ini (toleransi 1 menit untuk selisih jam) dan hanya bisa dipakai SEKALI.
"""
import hashlib
import hmac
import os
import re
import secrets
import time
import urllib.parse

from . import audit, storage

WINDOW = 60
TOLERANCE = 1
CODE_LEN = 16
MAX_FAILS = 5
LOCK_SECONDS = 120
USED_FILE = "admin_used.json"
LOCK_FILE = "lockouts.json"
LOCK_KEY = "__admin_code__"
_HEX = re.compile(r"^[0-9a-f]{%d}$" % CODE_LEN)


def _project_root() -> str:
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_secret():
    """Kunci rahasia admin, atau None bila belum dikonfigurasi."""
    env = os.getenv("UG_ADMIN_KEY", "").strip()
    if env:
        return env
    try:
        with open(os.path.join(_project_root(), "admin_key.txt"), "r", encoding="utf-8") as f:
            return f.read().strip() or None
    except OSError:
        return None


def ensure_secret():
    """Dipanggil saat aplikasi mulai. Bila belum ada kunci, buat satu dan simpan di admin_key.txt (pengembangan lokal).
    Mengembalikan (kunci_baru|None). Di APK/server read-only: tidak membuat apa pun (admin_login dinonaktifkan)."""
    if get_secret():
        return None
    new = secrets.token_hex(16)
    try:
        with open(os.path.join(_project_root(), "admin_key.txt"), "w", encoding="utf-8") as f:
            f.write(new + "\n")
    except OSError:
        return None
    return new


def code_for_minute(secret: str, minute: int) -> str:
    return hmac.new(secret.encode("utf-8"), str(minute).encode("utf-8"), hashlib.sha256).hexdigest()[:CODE_LEN]


def current_code(secret: str = None, now: float = None) -> str:
    secret = secret or get_secret()
    minute = int((time.time() if now is None else now) // WINDOW)
    return code_for_minute(secret, minute)


def seconds_left(now: float = None) -> int:
    now = time.time() if now is None else now
    return WINDOW - int(now % WINDOW)


def extract_code(text: str) -> str:
    """Menerima kode polos atau URL berisi ?key=KODE (atau ?admin=KODE)."""
    text = (text or "").strip()
    if "=" in text:
        query = urllib.parse.parse_qs(urllib.parse.urlparse(text).query)
        for name in ("key", "admin", "kode"):
            if query.get(name):
                text = query[name][0]
                break
    return text.strip().lower()


def verify(text: str, now: float = None):
    """Mengembalikan (ok, pesan). Menghitung percobaan gagal dan mengunci sementara."""
    secret = get_secret()
    if not secret:
        return False, "Kunci admin belum dikonfigurasi di server (UG_ADMIN_KEY)."
    now = time.time() if now is None else now
    minute = int(now // WINDOW)
    try:
        with storage.LOCK:
            locks = storage.load_json(LOCK_FILE, {})
            rec = locks.get(LOCK_KEY, {"count": 0, "locked_until": 0})
            if rec["locked_until"] > now:
                return False, f"Terlalu banyak percobaan. Coba lagi dalam {int(rec['locked_until'] - now) + 1} detik."
            code = extract_code(text)
            matched = None
            if _HEX.match(code):
                for m in range(minute - TOLERANCE, minute + TOLERANCE + 1):
                    if hmac.compare_digest(code, code_for_minute(secret, m)):
                        matched = m
                        break
            if matched is not None:
                used = {k: v for k, v in storage.load_json(USED_FILE, {}).items() if v >= minute - 5}
                if code in used:
                    return False, "Kode sudah dipakai. Tunggu kode baru (berganti tiap 60 detik)."
                used[code] = matched
                storage.save_json(USED_FILE, used)
                if LOCK_KEY in locks:
                    locks.pop(LOCK_KEY)
                    storage.save_json(LOCK_FILE, locks)
                return True, "Kode valid."
            rec["count"] += 1
            if rec["count"] >= MAX_FAILS:
                locks[LOCK_KEY] = {"count": 0, "locked_until": now + LOCK_SECONDS}
                msg = f"Terlalu banyak percobaan. Dikunci {LOCK_SECONDS} detik."
            else:
                locks[LOCK_KEY] = {"count": rec["count"], "locked_until": 0}
                msg = "Kode salah atau kedaluwarsa."
            storage.save_json(LOCK_FILE, locks)
    except storage.StorageError as e:
        return False, str(e)
    audit.log("(admin-kode)", "ADMIN_KODE_GAGAL", f"percobaan ke-{rec['count']}")
    return False, msg
