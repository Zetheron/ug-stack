"""Log aktivitas (audit). Tidak pernah mencatat password."""
import math
from datetime import datetime

from . import storage

LOG_FILE = "activity_log.json"
MAX_ENTRIES = 1000


def log(actor: str, action: str, detail: str = "") -> None:
    """Mencatat kejadian. Kegagalan mencatat tidak boleh menghentikan aplikasi."""
    try:
        with storage.LOCK:
            entries = storage.load_json(LOG_FILE, [])
            entries.append({"time": datetime.now().isoformat(timespec="seconds"),
                            "actor": actor or "-", "action": action, "detail": detail[:120]})
            storage.save_json(LOG_FILE, entries[-MAX_ENTRIES:])
    except storage.StorageError:
        pass


def list_logs(page: int = 1, per_page: int = 10, keyword: str = ""):
    """Terbaru dulu. Mengembalikan (daftar_halaman, total_halaman, total_cocok)."""
    entries = storage.load_json(LOG_FILE, [])
    kw = (keyword or "").strip().lower()
    per_page = max(1, per_page)
    skip = (max(1, page) - 1) * per_page
    matched, total = [], 0
    i = len(entries) - 1
    while i >= 0:                              # telusuri dari entri terbaru ke terlama
        e = entries[i]
        if not kw or kw in f"{e['action']} {e['actor']} {e['detail']}".lower():
            total += 1
            if total > skip and len(matched) < per_page:
                matched.append(e)
        i -= 1
    return matched, max(1, math.ceil(total / per_page)), total
