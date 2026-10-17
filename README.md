# UG-Stack (Flet, Python)

Aplikasi web responsif + APK Android untuk pengelolaan modul belajar dan progres mahasiswa.

## Menjalankan (web)
```
pip install -r requirements.txt
python main.py          # buka http://127.0.0.1:8550
```
Akun admin bawaan: `admin` / `Admin123`. Mahasiswa mendaftar sendiri lewat halaman Daftar.

## Menjalankan versi konsol
```
python cli.py
```

## Fitur halaman
Tutorial (12 bahasa x 4 pelajaran), Referensi (cheat sheet), Latihan/Quiz, Sertifikat (kode verifikasi), Roadmap,
Pencarian, Try it, Dashboard (login, CRUD modul, progres), plus konten otomatis dari Wikipedia, MDN, Stack Overflow,
DEV Community, dan GitHub (cache 24 jam; butuh internet pada pemakaian pertama).

## Menambah materi
Edit `content/lessons.py`, `content/reference.py`, `content/quizzes.py` (format sudah ada di berkas), lalu jalankan pengujian.

## Pengujian otomatis
```
python -m unittest tests.test_services tests.test_content tests.test_lanjutan -v
python run_report.py     # bukti 11 skenario minimal -> docs/hasil_pengujian.md
python benchmark.py      # waktu algoritma -> docs/benchmark_algoritma.md
```

## Membuat APK / membuka di HP
Lihat **docs/PANDUAN_APK.md** (jalur GitHub Actions, build lokal, dan demo lewat Wi-Fi). Singkatnya:
`flet build apk --project ugstack --product "UGStack" --org id.ac.gunadarma`, atau jalankan workflow
`.github/workflows/build-apk.yml` di GitHub tanpa memasang apa pun di komputer.

## Menayangkan online
Lihat **docs/PANDUAN_DEPLOY.md**: server Flet di Render (Docker), data di Neon (PostgreSQL), dan alamat Vercel opsional lewat pengalihan.
Aplikasi memilih penyimpanan otomatis: `DATABASE_URL` -> PostgreSQL; APK -> penyimpanan perangkat; selain itu berkas JSON.

## Login, tema, dan bahasa
- Halaman login hanya menampilkan **Mahasiswa** (NPM/username + password) dan **Dosen** (username/NIDN + password). **Admin tidak ditampilkan**: admin masuk dengan kode 60 detik dari `tools/admin_generator.html` (lihat `docs/PANDUAN_ADMIN_KODE.md`).
  Dosen tidak bisa mendaftar sendiri: akunnya dibuat admin (Panel Admin -> Buat Akun).
- Tombol bulan/matahari di header = tema gelap/terang; tombol **EN/ID** = bahasa Inggris/Indonesia. Pilihan tersimpan per perangkat.

## Peran pengguna
`admin` (kelola akun, soal, modul, data), `dosen` (kelola modul dan soal quiz), `mahasiswa` (belajar, quiz, sertifikat).
Admin membuat akun tunggal atau massal (CSV) di Panel Admin -> Buat Akun; password sementara dibuat otomatis dan wajib diganti saat login pertama.

## Dokumen
`docs/` berisi perancangan, pseudocode, flowchart (`flowchart/*.png`), implementasi, pengujian,
analisis, dan `LAPORAN_LENGKAP.md` (gabungan semua bab).

## Catatan
- `vercel.json` bawaan tidak dipakai: Flet butuh server dengan koneksi websocket, tidak cocok untuk Vercel serverless.
