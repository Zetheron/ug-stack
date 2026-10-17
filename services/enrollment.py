"""Langganan paket dan pendaftaran kursus (mode demo kampus: tanpa pembayaran)."""
from content.languages import BY_KEY

from . import audit, storage
from .storage import StorageError

ENROLL_FILE = "enrollments.json"
PLANS = {"basic": "Basic", "pro": "Pro Plus", "lifetime": "Lifetime"}


def get_info(username: str) -> dict:
    data = storage.load_json(ENROLL_FILE, {})
    rec = data.get(username, {})
    return {"plan": rec.get("plan"), "courses": list(rec.get("courses", []))}


def set_plan(username: str, plan: str):
    if plan not in PLANS:
        return False, "Paket tidak dikenal."
    try:
        with storage.LOCK:
            data = storage.load_json(ENROLL_FILE, {})
            rec = data.setdefault(username, {"plan": None, "courses": []})
            if rec.get("plan") == plan:
                return False, f"Anda sudah berlangganan paket {PLANS[plan]}."
            rec["plan"] = plan
            storage.save_json(ENROLL_FILE, data)
    except StorageError as e:
        return False, str(e)
    audit.log(username, "PAKET", PLANS[plan])
    return True, f"Paket {PLANS[plan]} aktif (mode demo, tanpa pembayaran)."


def enroll(username: str, lang_key: str):
    if lang_key not in BY_KEY:
        return False, "Kursus tidak ditemukan."
    try:
        with storage.LOCK:
            data = storage.load_json(ENROLL_FILE, {})
            rec = data.setdefault(username, {"plan": None, "courses": []})
            if lang_key in rec["courses"]:
                return False, "Anda sudah terdaftar di kursus ini."
            rec["courses"].append(lang_key)
            storage.save_json(ENROLL_FILE, data)
    except StorageError as e:
        return False, str(e)
    audit.log(username, "DAFTAR_KURSUS", lang_key)
    return True, f"Terdaftar di kursus {BY_KEY[lang_key]['name']}."


def remove_user(username: str) -> None:
    with storage.LOCK:
        data = storage.load_json(ENROLL_FILE, {})
        if username in data:
            del data[username]
            storage.save_json(ENROLL_FILE, data)
