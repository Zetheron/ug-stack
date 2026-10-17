"""Soal quiz kustom yang dikelola admin (digabung dengan bank soal bawaan)."""
from content.languages import BY_KEY
from content.quizzes import QUIZZES

from . import audit, storage
from .roles import can_manage_content
from .storage import StorageError

CUSTOM_FILE = "quiz_custom.json"


def get_questions(lang_key: str) -> list:
    """Soal bawaan + soal kustom untuk satu bahasa."""
    custom = storage.load_json(CUSTOM_FILE, {}).get(lang_key, [])
    return list(QUIZZES.get(lang_key, [])) + custom


def list_custom() -> list:
    data = storage.load_json(CUSTOM_FILE, {})
    return [dict(q, lang=k) for k, qs in data.items() for q in qs]


def validate_question(data: dict):
    q = (data.get("q") or "").strip()
    if not 5 <= len(q) <= 200:
        return False, "Pertanyaan harus 5-200 karakter.", None
    options = [(o or "").strip() for o in (data.get("options") or [])]
    if len(options) != 4 or any(not o for o in options):
        return False, "Isi keempat opsi jawaban.", None
    if any(len(o) > 100 for o in options):
        return False, "Tiap opsi maksimal 100 karakter.", None
    if len(set(o.lower() for o in options)) != 4:
        return False, "Opsi jawaban tidak boleh ada yang sama.", None
    try:
        answer = int(data.get("answer"))
    except (TypeError, ValueError):
        return False, "Pilih jawaban yang benar.", None
    if answer not in range(4):
        return False, "Pilih jawaban yang benar.", None
    explain = (data.get("explain") or "").strip()
    if not explain or len(explain) > 200:
        return False, "Penjelasan wajib diisi (maks. 200 karakter).", None
    return True, "", {"q": q, "options": options, "answer": answer, "explain": explain}


def add_question(actor, lang_key: str, data: dict):
    if not can_manage_content(actor):
        return False, "Hanya admin atau dosen yang boleh mengelola soal."
    if lang_key not in BY_KEY:
        return False, "Bahasa tidak valid."
    ok, msg, clean = validate_question(data)
    if not ok:
        return False, msg
    try:
        with storage.LOCK:
            store = storage.load_json(CUSTOM_FILE, {})
            items = store.setdefault(lang_key, [])
            clean["id"] = max([x["id"] for x in items], default=0) + 1
            clean["custom"] = True
            items.append(clean)
            storage.save_json(CUSTOM_FILE, store)
    except StorageError as e:
        return False, str(e)
    audit.log(actor["username"], "SOAL_TAMBAH", f"{lang_key}: {clean['q'][:40]}")
    return True, "Soal ditambahkan."


def delete_question(actor, lang_key: str, qid: int):
    if not can_manage_content(actor):
        return False, "Hanya admin atau dosen yang boleh mengelola soal."
    try:
        with storage.LOCK:
            store = storage.load_json(CUSTOM_FILE, {})
            items = store.get(lang_key, [])
            remaining = [x for x in items if x["id"] != qid]
            if len(remaining) == len(items):
                return False, "Soal tidak ditemukan."
            store[lang_key] = remaining
            storage.save_json(CUSTOM_FILE, store)
    except StorageError as e:
        return False, str(e)
    audit.log(actor["username"], "SOAL_HAPUS", f"{lang_key} #{qid}")
    return True, "Soal dihapus."
