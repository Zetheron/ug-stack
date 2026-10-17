"""Validasi input pengguna."""
import re

BAHASA = ["HTML", "CSS", "JavaScript", "Python", "SQL", "PHP", "Java", "C++", "C#", "React", "MySQL"]
LEVELS = ["Beginner", "Intermediate", "Advanced"]
_USERNAME_RE = re.compile(r"^[A-Za-z0-9_]{4,20}$")


def validate_username(username: str):
    if not username or not username.strip():
        return False, "Username tidak boleh kosong."
    if not _USERNAME_RE.match(username.strip()):
        return False, "Username 4-20 karakter: huruf, angka, atau underscore."
    return True, ""


def validate_password(password: str):
    if not password:
        return False, "Password tidak boleh kosong."
    if len(password) < 8:
        return False, "Password minimal 8 karakter."
    if not any(c.isalpha() for c in password) or not any(c.isdigit() for c in password):
        return False, "Password harus mengandung huruf dan angka."
    return True, ""


def validate_module(data: dict):
    """Mengembalikan (ok, pesan, data_bersih)."""
    judul = (data.get("judul") or "").strip()
    if not judul:
        return False, "Judul tidak boleh kosong.", None
    if not 3 <= len(judul) <= 60:
        return False, "Judul harus 3-60 karakter.", None
    bahasa = data.get("bahasa")
    if bahasa not in BAHASA:
        return False, "Pilih bahasa pemrograman yang valid.", None
    level = data.get("level")
    if level not in LEVELS:
        return False, "Pilih level yang valid.", None
    try:
        durasi = int(str(data.get("durasi", "")).strip())
    except ValueError:
        return False, "Durasi harus berupa angka bulat (menit).", None
    if not 1 <= durasi <= 600:
        return False, "Durasi harus antara 1 dan 600 menit.", None
    deskripsi = (data.get("deskripsi") or "").strip()
    if len(deskripsi) > 200:
        return False, "Deskripsi maksimal 200 karakter.", None
    return True, "", {"judul": judul, "bahasa": bahasa, "level": level,
                      "durasi": durasi, "deskripsi": deskripsi}
