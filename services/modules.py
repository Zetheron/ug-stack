"""CRUD modul materi + pencarian, filter, dan pengurutan."""
from . import algorithms, audit, progress, storage
from .roles import can_manage_content
from .storage import StorageError
from .validators import LEVELS, validate_module

MODULES_FILE = "modules.json"

SEED_MODULES = [
    {"id": 1, "judul": "Pengenalan HTML", "bahasa": "HTML", "level": "Beginner", "durasi": 45, "deskripsi": "Struktur dasar halaman web dan tag utama."},
    {"id": 2, "judul": "Dasar CSS", "bahasa": "CSS", "level": "Beginner", "durasi": 40, "deskripsi": "Selector, warna, dan tata letak sederhana."},
    {"id": 3, "judul": "Variabel dan Tipe Data Python", "bahasa": "Python", "level": "Beginner", "durasi": 50, "deskripsi": "Mengenal variabel, tipe data, dan operator."},
    {"id": 4, "judul": "Percabangan dan Perulangan Python", "bahasa": "Python", "level": "Beginner", "durasi": 60, "deskripsi": "if/elif/else, for, dan while."},
    {"id": 5, "judul": "Function dan Modularitas Python", "bahasa": "Python", "level": "Intermediate", "durasi": 70, "deskripsi": "Memecah program menjadi function yang terstruktur."},
    {"id": 6, "judul": "JavaScript Interaktif", "bahasa": "JavaScript", "level": "Intermediate", "durasi": 75, "deskripsi": "DOM dan event pada halaman web."},
    {"id": 7, "judul": "Query SQL Dasar", "bahasa": "SQL", "level": "Beginner", "durasi": 55, "deskripsi": "SELECT, WHERE, dan ORDER BY."},
    {"id": 8, "judul": "Desain Basis Data MySQL", "bahasa": "MySQL", "level": "Advanced", "durasi": 90, "deskripsi": "Normalisasi dan relasi antar tabel."},
]

_NOT_ADMIN = "Hanya admin atau dosen yang boleh mengubah data modul."


def list_modules() -> list:
    return storage.load_json(MODULES_FILE, SEED_MODULES)


def get_module(module_id: int):
    """Cari modul berdasarkan ID: pencarian biner (daftar tersimpan berurutan menurut ID)."""
    modules = list_modules()
    idx = algorithms.binary_search(modules, module_id, key=lambda m: m["id"])
    if idx == -1:                                    # jaga-jaga bila file diubah manual
        idx = algorithms.linear_search(modules, module_id, key=lambda m: m["id"])
    return modules[idx] if idx != -1 else None


def add_module(user, data: dict):
    if not can_manage_content(user):
        return False, _NOT_ADMIN
    ok, msg, clean = validate_module(data)
    if not ok:
        return False, msg
    try:
        with storage.LOCK:
            modules = list_modules()
            new_id = max([m["id"] for m in modules], default=0) + 1
            clean["id"] = new_id
            modules.append(clean)
            storage.save_json(MODULES_FILE, modules)
    except StorageError as e:
        return False, str(e)
    audit.log(user["username"], "MODUL_TAMBAH", clean["judul"])
    return True, "Modul berhasil ditambahkan."


def update_module(user, module_id: int, data: dict):
    if not can_manage_content(user):
        return False, _NOT_ADMIN
    ok, msg, clean = validate_module(data)
    if not ok:
        return False, msg
    try:
        with storage.LOCK:
            modules = list_modules()
            for i, m in enumerate(modules):
                if m["id"] == module_id:
                    clean["id"] = module_id
                    modules[i] = clean
                    storage.save_json(MODULES_FILE, modules)
                    audit.log(user["username"], "MODUL_UBAH", clean["judul"])
                    return True, "Modul berhasil diubah."
    except StorageError as e:
        return False, str(e)
    return False, "Modul tidak ditemukan."


def delete_module(user, module_id: int):
    if not can_manage_content(user):
        return False, _NOT_ADMIN
    try:
        with storage.LOCK:
            modules = list_modules()
            remaining = [m for m in modules if m["id"] != module_id]
            if len(remaining) == len(modules):
                return False, "Modul tidak ditemukan."
            storage.save_json(MODULES_FILE, remaining)
            progress.remove_module(module_id)
    except StorageError as e:
        return False, str(e)
    audit.log(user["username"], "MODUL_HAPUS", f"id {module_id}")
    return True, "Modul berhasil dihapus."


def search_modules(modules: list, keyword: str = "", bahasa: str = "Semua",
                   sort_by: str = "judul", descending: bool = False) -> list:
    """Filter berdasarkan kata kunci dan bahasa, lalu urutkan."""
    keyword = (keyword or "").strip().lower()
    result = []
    for m in modules:
        if bahasa != "Semua" and m["bahasa"] != bahasa:
            continue
        if keyword and keyword not in m["judul"].lower() and keyword not in m["deskripsi"].lower():
            continue
        result.append(m)
    if sort_by == "durasi":
        key = lambda m: m["durasi"]
    elif sort_by == "level":
        key = lambda m: LEVELS.index(m["level"])
    else:
        key = lambda m: m["judul"].lower()
    return algorithms.merge_sort(result, key=key, descending=descending)   # merge sort buatan sendiri
