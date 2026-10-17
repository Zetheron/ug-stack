"""Pengaturan aplikasi yang bisa diubah admin."""
from . import audit, storage
from .roles import is_admin
from .storage import StorageError

SETTINGS_FILE = "settings.json"
DEFAULTS = {"registration_open": True}


def get_settings() -> dict:
    data = storage.load_json(SETTINGS_FILE, {})
    return {**DEFAULTS, **(data if isinstance(data, dict) else {})}


def registration_open() -> bool:
    try:
        return bool(get_settings()["registration_open"])
    except StorageError:
        return True


def set_registration_open(actor, value: bool):
    if not is_admin(actor):
        return False, "Hanya admin yang boleh mengubah pengaturan."
    try:
        with storage.LOCK:
            data = get_settings()
            data["registration_open"] = bool(value)
            storage.save_json(SETTINGS_FILE, data)
    except StorageError as e:
        return False, str(e)
    audit.log(actor["username"], "PENGATURAN", f"pendaftaran mandiri {'dibuka' if value else 'ditutup'}")
    return True, "Pendaftaran mandiri " + ("dibuka." if value else "ditutup.")
