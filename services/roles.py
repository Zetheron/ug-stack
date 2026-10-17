"""Peran dan otorisasi: admin (semua), dosen (kelola konten), mahasiswa (belajar)."""

ROLES = ("admin", "dosen", "mahasiswa")


def is_admin(user) -> bool:
    return bool(user) and user.get("role") == "admin"


def is_dosen(user) -> bool:
    return bool(user) and user.get("role") == "dosen"


def can_manage_content(user) -> bool:
    """Admin dan dosen boleh mengelola modul dan soal quiz; hanya admin mengelola akun dan data."""
    return bool(user) and user.get("role") in ("admin", "dosen")
