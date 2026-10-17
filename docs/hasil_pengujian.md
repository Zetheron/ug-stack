# Hasil Pengujian 11 Skenario Minimal

Dijalankan otomatis oleh `run_report.py` pada 2026-10-16 10:56:29.

| No | Pengujian | Input | Proses | Output diharapkan | Output aktual | Status |
|---|---|---|---|---|---|---|
| 1 | Login berhasil | NPM 12345678 / Rahasia123 (peran Mahasiswa) | cocokkan hash PBKDF2 + cek peran | ok=True, peran mahasiswa | ok=True, peran=mahasiswa, pesan='Login berhasil.' | LULUS |
| 2 | Login gagal | 12345678 / salah1234 | hash tidak cocok, hitung percobaan | ok=False, sisa percobaan 2 | ok=False, pesan='Username atau password salah. Sisa percobaan: 2.' | LULUS |
| 3 | Input data | judul, bahasa, level, durasi, deskripsi valid | validasi, buat ID baru | data diterima | ok=True, pesan='Modul berhasil ditambahkan.' | LULUS |
| 4 | Validasi input | judul kosong; durasi 'abc' | validate_module | kedua input ditolak dengan pesan | 'Judul tidak boleh kosong.' / 'Durasi harus berupa angka bulat (menit).' | LULUS |
| 5 | Penambahan data | 8 modul sebelum | append + simpan JSON | jumlah modul 9 | jumlah modul sekarang 9 | LULUS |
| 6 | Pencarian data | kata kunci 'laporan', filter Python | filter + merge sort | 1 modul 'Modul Laporan' | 1 hasil: ['Modul Laporan'] | LULUS |
| 7 | Perubahan data | ubah durasi modul 9 menjadi 60 | update + simpan | durasi menjadi 60 | ok=True, durasi=60 | LULUS |
| 8 | Penghapusan data | hapus modul 9 | hapus + bersihkan progres | modul hilang | ok=True, get_module=None | LULUS |
| 9 | Penyimpanan data | tambah 'Modul Simpan' | tulis modules.json atomik | file modules.json ada | file ada=True, ukuran=1633 byte | LULUS |
| 10 | Pembacaan data | baca ulang dari file | load_json | 'Modul Simpan' terbaca | 9 modul terbaca, 'Modul Simpan' ada=True | LULUS |
| 11 | Logout | tombol/menu logout | hapus sesi + catat audit | entri LOGOUT di log | entri terbaru: LOGOUT oleh 12345678 | LULUS |

**Ringkasan: 11 dari 11 skenario LULUS.**
