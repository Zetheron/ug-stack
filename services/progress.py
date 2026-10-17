"""Progres belajar mahasiswa."""
from . import storage

PROGRESS_FILE = "progress.json"


def get_done(username: str) -> list:
    data = storage.load_json(PROGRESS_FILE, {})
    return list(data.get(username, []))


def toggle_done(username: str, module_id: int):
    """Tandai/batalkan selesai. Mengembalikan (ok, pesan, status_selesai)."""
    try:
        with storage.LOCK:
            data = storage.load_json(PROGRESS_FILE, {})
            done = data.get(username, [])
            if module_id in done:
                done.remove(module_id)
                status = False
            else:
                done.append(module_id)
                status = True
            data[username] = done
            storage.save_json(PROGRESS_FILE, data)
    except storage.StorageError as e:
        return False, str(e), None
    return True, ("Modul ditandai selesai." if status else "Penanda selesai dibatalkan."), status


def percent(done_ids: list, module_ids: list) -> float:
    """Persentase modul selesai terhadap modul yang masih ada."""
    if not module_ids:
        return 0.0
    count = 0
    for mid in module_ids:
        if mid in done_ids:
            count += 1
    return count * 100.0 / len(module_ids)


def remove_module(module_id: int) -> None:
    with storage.LOCK:
        data = storage.load_json(PROGRESS_FILE, {})
        for username in data:
            data[username] = [m for m in data[username] if m != module_id]
        storage.save_json(PROGRESS_FILE, data)


def remove_user(username: str) -> None:
    with storage.LOCK:
        data = storage.load_json(PROGRESS_FILE, {})
        if username in data:
            del data[username]
            storage.save_json(PROGRESS_FILE, data)


def ranking(usernames: list, module_ids: list) -> list:
    """Daftar (username, jumlah_selesai, persen) terurut persen menurun."""
    data = storage.load_json(PROGRESS_FILE, {})
    rows = []
    for name in usernames:
        done = data.get(name, [])
        rows.append((name, len([m for m in module_ids if m in done]), percent(done, module_ids)))
    rows.sort(key=lambda r: r[2], reverse=True)
    return rows
