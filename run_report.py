"""Menjalankan 11 skenario pengujian minimal dan menulis docs/hasil_pengujian.md (bukti output aktual).

Jalankan: python run_report.py
"""
import os
import shutil
import tempfile
from datetime import datetime

from services import audit, auth, csv_io, modules, progress, storage

ADMIN = {"username": "admin", "role": "admin"}


def main() -> None:
    tmp = tempfile.mkdtemp()
    os.environ["FLET_APP_STORAGE_DATA"] = tmp          # data uji terpisah dari data asli
    storage.reset_backend()
    rows = []

    def catat(no, nama, masukan, proses, harapan, aktual, lulus):
        rows.append((no, nama, masukan, proses, harapan, str(aktual).replace("\n", " ").replace("|", "/"),
                     "LULUS" if lulus else "GAGAL"))

    try:
        auth.init_data()
        auth.reset_lock()

        auth.register("12345678", "Rahasia123", "Rahasia123")                       # mahasiswa dengan NPM sebagai username
        ok, msg, user = auth.login("12345678", "Rahasia123", expected_role="mahasiswa")
        catat(1, "Login berhasil", "NPM 12345678 / Rahasia123 (peran Mahasiswa)", "cocokkan hash PBKDF2 + cek peran",
              "ok=True, peran mahasiswa", f"ok={ok}, peran={user and user['role']}, pesan='{msg}'", ok and user["role"] == "mahasiswa")

        ok, msg, user = auth.login("12345678", "salah1234", expected_role="mahasiswa")
        catat(2, "Login gagal", "12345678 / salah1234", "hash tidak cocok, hitung percobaan", "ok=False, sisa percobaan 2",
              f"ok={ok}, pesan='{msg}'", (not ok) and "Sisa percobaan: 2" in msg)

        ok, msg = modules.add_module(ADMIN, {"judul": "", "bahasa": "Python", "level": "Beginner", "durasi": "30"})
        ok2, msg2 = modules.add_module(ADMIN, {"judul": "Uji", "bahasa": "Python", "level": "Beginner", "durasi": "abc"})
        catat(4, "Validasi input", "judul kosong; durasi 'abc'", "validate_module", "kedua input ditolak dengan pesan",
              f"'{msg}' | '{msg2}'", (not ok) and (not ok2))

        data = {"judul": "Modul Laporan", "bahasa": "Python", "level": "Intermediate", "durasi": "45", "deskripsi": "uji"}
        awal = len(modules.list_modules())
        ok, msg = modules.add_module(ADMIN, data)
        akhir = len(modules.list_modules())
        catat(3, "Input data", "judul, bahasa, level, durasi, deskripsi valid", "validasi, buat ID baru", "data diterima",
              f"ok={ok}, pesan='{msg}'", ok)
        catat(5, "Penambahan data", f"{awal} modul sebelum", "append + simpan JSON", f"jumlah modul {awal + 1}",
              f"jumlah modul sekarang {akhir}", ok and akhir == awal + 1)

        hasil = modules.search_modules(modules.list_modules(), "laporan", "Python", "judul", False)
        catat(6, "Pencarian data", "kata kunci 'laporan', filter Python", "filter + merge sort",
              "1 modul 'Modul Laporan'", f"{len(hasil)} hasil: {[m['judul'] for m in hasil]}",
              len(hasil) == 1 and hasil[0]["judul"] == "Modul Laporan")

        mid = hasil[0]["id"]
        ok, msg = modules.update_module(ADMIN, mid, dict(data, durasi="60"))
        catat(7, "Perubahan data", f"ubah durasi modul {mid} menjadi 60", "update + simpan", "durasi menjadi 60",
              f"ok={ok}, durasi={modules.get_module(mid)['durasi']}", ok and modules.get_module(mid)["durasi"] == 60)

        ok, msg = modules.delete_module(ADMIN, mid)
        catat(8, "Penghapusan data", f"hapus modul {mid}", "hapus + bersihkan progres", "modul hilang",
              f"ok={ok}, get_module={modules.get_module(mid)}", ok and modules.get_module(mid) is None)

        ok, _ = modules.add_module(ADMIN, dict(data, judul="Modul Simpan"))
        cek = os.path.exists(os.path.join(tmp, "modules.json"))
        catat(9, "Penyimpanan data", "tambah 'Modul Simpan'", "tulis modules.json atomik", "file modules.json ada",
              f"file ada={cek}, ukuran={os.path.getsize(os.path.join(tmp, 'modules.json'))} byte", ok and cek)

        judul = [m["judul"] for m in modules.list_modules()]
        catat(10, "Pembacaan data", "baca ulang dari file", "load_json", "'Modul Simpan' terbaca",
              f"{len(judul)} modul terbaca, 'Modul Simpan' ada={'Modul Simpan' in judul}", "Modul Simpan" in judul)

        auth.log_logout("12345678")
        log, _, _ = audit.list_logs(1, 3, "LOGOUT")
        catat(11, "Logout", "tombol/menu logout", "hapus sesi + catat audit", "entri LOGOUT di log",
              f"entri terbaru: {log[0]['action']} oleh {log[0]['actor']}" if log else "tidak ada", bool(log))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
        os.environ.pop("FLET_APP_STORAGE_DATA", None)

    rows.sort(key=lambda r: r[0])
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = ["# Hasil Pengujian 11 Skenario Minimal", "", f"Dijalankan otomatis oleh `run_report.py` pada {waktu}.", "",
             "| No | Pengujian | Input | Proses | Output diharapkan | Output aktual | Status |", "|---|---|---|---|---|---|---|"]
    lines += ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    lulus = sum(1 for r in rows if r[-1] == "LULUS")
    lines += ["", f"**Ringkasan: {lulus} dari {len(rows)} skenario LULUS.**"]
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs", "hasil_pengujian.md")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
