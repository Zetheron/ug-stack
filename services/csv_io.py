"""Ekspor dan impor modul dalam format CSV (dengan validasi tiap baris)."""
import csv
import io
import os
from datetime import datetime

from . import audit, modules, storage
from .roles import can_manage_content
from .storage import StorageError
from .validators import validate_module

FIELDS = ["id", "judul", "bahasa", "level", "durasi", "deskripsi"]
REQUIRED = ["judul", "bahasa", "level", "durasi"]
MAX_ROWS = 500
MAX_CHARS = 200_000


def export_modules_csv() -> str:
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=FIELDS, extrasaction="ignore")
    writer.writeheader()
    for m in modules.list_modules():
        writer.writerow(m)
    return buf.getvalue()


def export_to_file():
    """Simpan CSV ke folder data/exports (hanya backend berkas). Mengembalikan (ok, pesan_atau_path)."""
    if storage.backend_label() != "berkas":
        return False, "Penyimpanan ini tidak memakai berkas; isi CSV disalin ke clipboard."
    try:
        folder = os.path.join(storage.get_data_dir(), "exports")
        os.makedirs(folder, exist_ok=True)
        path = os.path.join(folder, f"modul_{datetime.now():%Y%m%d_%H%M%S}.csv")
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(export_modules_csv())
        return True, path
    except (OSError, StorageError) as e:
        return False, f"Gagal menulis file CSV: {e}"


def import_modules_csv(user, text: str):
    """Mengembalikan (ok, pesan, laporan). Baris tidak valid dilewati dan dilaporkan."""
    if not can_manage_content(user):
        return False, "Hanya admin atau dosen yang boleh mengimpor data.", None
    if not (text or "").strip():
        return False, "Teks CSV kosong.", None
    if len(text) > MAX_CHARS:
        return False, "CSV terlalu besar (maks. 200.000 karakter).", None
    reader = csv.DictReader(io.StringIO(text.strip()))
    header = [h.strip().lower() for h in (reader.fieldnames or [])]
    missing = [c for c in REQUIRED if c not in header]
    if missing:
        return False, f"Kolom wajib tidak ada: {', '.join(missing)}.", None
    reader.fieldnames = header
    added, skipped = 0, []
    try:
        with storage.LOCK:
            current = modules.list_modules()
            seen = {(m["judul"].lower(), m["bahasa"]) for m in current}
            next_id = max([m["id"] for m in current], default=0) + 1
            for line, row in enumerate(reader, start=2):
                if line - 1 > MAX_ROWS:
                    skipped.append((line, f"melebihi batas {MAX_ROWS} baris"))
                    break
                ok, msg, clean = validate_module({k: row.get(k) for k in FIELDS})
                if not ok:
                    skipped.append((line, msg))
                    continue
                ident = (clean["judul"].lower(), clean["bahasa"])
                if ident in seen:
                    skipped.append((line, "duplikat (judul dan bahasa sudah ada)"))
                    continue
                seen.add(ident)
                clean["id"] = next_id
                next_id += 1
                current.append(clean)
                added += 1
            if added:
                storage.save_json(modules.MODULES_FILE, current)
    except StorageError as e:
        return False, str(e), None
    audit.log(user["username"], "IMPOR_CSV", f"{added} ditambah, {len(skipped)} dilewati")
    report = {"added": added, "skipped": skipped}
    return True, f"Impor selesai: {added} modul ditambahkan, {len(skipped)} baris dilewati.", report
