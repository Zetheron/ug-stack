# BAB IV - IMPLEMENTASI PROGRAM

## 4.1 Struktur Proyek
```
main.py                  titik masuk web/APK, navigasi, kontrol akses, sesi kedaluwarsa, tampilan responsif
cli.py                   versi konsol (input/print, menu while)
run_report.py, benchmark.py   pembuat bukti pengujian dan pengukur waktu algoritma
services/                logika program (tanpa UI)
  storage.py             baca/tulis JSON + penanganan kesalahan
  validators.py          validasi input
  auth.py                registrasi, login (PBKDF2), kunci akun, peran
  modules.py             CRUD modul, cari/filter/urut
  progress.py            progres belajar dan perhitungan persen
  enrollment.py, settings.py   paket/kursus per pengguna, pengaturan pendaftaran
  algorithms.py          pencarian linear/biner, insertion sort, merge sort (buatan sendiri)
  audit.py               log aktivitas (paginasi dengan while)
  csv_io.py, backup.py   ekspor/impor CSV, backup dan pemulihan
  quiz_admin.py, roles.py   soal kustom, pemeriksaan peran
  web_sources.py         konten otomatis dari API tepercaya + cache 24 jam
  quiz.py                penilaian quiz, skor, sertifikat, verifikasi
  content_search.py      pencarian di materi bawaan
content/                 materi bawaan: languages, lessons, reference, quizzes, pages
views/ components/       tampilan Flet (beranda, tutorial, pelajaran, referensi, quiz, sertifikat, pencarian, roadmap, info, login, dashboard)
data/                    users.json, modules.json, progress.json (dibuat otomatis)
tests/test_services.py   pengujian otomatis (unittest)
```

## 4.2 Penerapan Konsep Dasar Pemrograman
| Konsep | Contoh penerapan |
|---|---|
| Variabel dan tipe data | `str` (username), `int` (durasi), `float` (persen), `bool` (valid) |
| Operator | aritmetika (`count * 100.0 / len(...)`), perbandingan, logika (`and`, `or`, `not`) |
| Input dan output | `TextField`, `Dropdown` (web/APK); `input()` dan `print()` (`cli.py`); `Text`, `SnackBar`, kartu modul sebagai output |
| Percabangan | `if/elif/else` pada login, validasi, peran admin/mahasiswa |
| Perulangan | `for` pada filter dan validasi; **`while`** pada pencarian biner, merge sort, paginasi log, dan menu konsol (`cli.py`) |
| Struktur data | `list` modul, `dict` progres dan modul, `tuple` hasil `(ok, pesan)` |
| Function / modularitas | satu function satu tugas: `login`, `register`, `add_module`, `search_modules`, `percent` |
| Pengolahan data | tambah, tampil, cari, ubah, hapus, filter, sort, perhitungan persen |
| Penyimpanan data | file JSON (`storage.py`) |
| Validasi dan error handling | `validators.py`; `try/except` untuk `StorageError`, `JSONDecodeError`, `OSError` |
| Keamanan akses | hash PBKDF2-SHA256 + salt acak, kunci akun 3x gagal, kontrol peran di layer service |

## 4.3 Tampilan Responsif dan APK
- **Responsif**: `ResponsiveRow` dengan breakpoint (`xs`, `sm`, `md`, `lg`). Layar < 768 px dianggap HP: menu atas dilipat menjadi tombol hamburger, kartu menjadi satu kolom, padding dikecilkan. Tampilan dirender ulang hanya saat berpindah antara layar HP dan desktop.
- **APK**: dibuat dengan `flet build apk` (lihat `docs/PANDUAN_APK.md`). Karena Flet 0.23.1 belum menyediakan `FLET_APP_STORAGE_DATA` (baru ada sejak 0.25) dan folder aplikasi dibuat ulang saat dibuka, data pada APK disimpan lewat **penyimpanan perangkat Flet** (`page.client_storage`, SharedPreferences) agar tetap ada setelah aplikasi ditutup.

## 4.4 Halaman-Halaman Aplikasi
| Tombol / menu | Halaman |
|---|---|
| Tutorials, kartu bahasa, sub-nav bahasa | Katalog Tutorial dan halaman Pelajaran (sidebar, kode, Try it, panel konten live) |
| References | Cheat sheet per bahasa + filter + pencarian MDN / Stack Overflow |
| Exercises | Daftar quiz dan halaman Quiz |
| Certificates | Daftar sertifikat, detail sertifikat, verifikasi kode |
| Roadmap, "Not Sure Where To Begin?" | Jalur belajar (Front-End, Back-End, Software Engineer, Data) |
| Ikon cari, kolom cari beranda | Halaman Pencarian |
| Upgrade, Paid Courses | Halaman paket dan kursus berbayar |
| Link footer, banner aplikasi, UG-Stack Spaces | Halaman Informasi |
| Login, Daftar, nama pengguna | Halaman autentikasi dan Dashboard |
| Beranda | Hero, Kode Hari Ini (berganti tiap hari), Sedang Ramai di Komunitas (live) |

## 4.5 Konten Otomatis dan Kinerja
Pemuatan dari web dijalankan di thread terpisah sehingga halaman langsung tampil dengan indikator memuat. Hasil disimpan di cache 24 jam (`cache_*.json`); saat offline, cache lama tetap dipakai. Parser tiap sumber berupa fungsi murni sehingga dapat diuji tanpa jaringan.

## 4.6 Keamanan Berlapis
| Mekanisme | Lokasi |
|---|---|
| Hash PBKDF2-SHA256 100.000 iterasi + salt acak, `hmac.compare_digest` | `auth.hash_password`, `auth._verify` |
| Kunci akun 3 kali gagal (30 detik), **disimpan di `lockouts.json`** sehingga tetap berlaku setelah restart | `auth.login` |
| Hash tiruan untuk username tak dikenal (waktu respons seragam) | `auth._verify` |
| Admin bawaan wajib ganti password (juga untuk data lama yang masih memakai password bawaan) | `auth.init_data`, `views/account.py` |
| Sesi berakhir otomatis setelah 15 menit tanpa navigasi | `main.check_session` |
| Otorisasi peran di service (admin-only) dan di router (`ADMIN_VIEWS`) | `services/roles.py`, `main.render` |
| Admin terakhir tidak bisa dihapus/diturunkan; tidak bisa menghapus akun sendiri | `auth.set_role`, `auth.delete_user` |
| Audit log (tanpa password) | `services/audit.py` |
| Kunci tulis `threading.RLock` untuk operasi baca-ubah-tulis | `storage.LOCK` |
| Backup divalidasi sebelum dipulihkan; nama backup dibersihkan dari path traversal | `services/backup.py` |

## 4.7 Penyimpanan Multi-Backend dan Penayangan Online
| Lingkungan | Backend | Pemilihan |
|---|---|---|
| Komputer / pengembangan | berkas JSON (`data/`) | bawaan |
| APK Android/iOS | penyimpanan perangkat Flet | `main.py` mendeteksi bukan web + platform Android/iOS |
| Server online (Render + Neon) | tabel `ug_kv` di PostgreSQL | variabel `DATABASE_URL` |

Semua service tetap memakai `load_json`/`save_json`, sehingga logika tidak berubah. Panduan penayangan ada di `docs/PANDUAN_DEPLOY.md`
(Flet memerlukan server dengan WebSocket sehingga tidak dapat berjalan langsung di Vercel serverless).

## 4.8 Peran dan Pengelolaan Akun
| Peran | Hak akses |
|---|---|
| admin | semua: akun (buat, ubah peran, reset, hapus), modul, soal quiz, log, CSV, backup, pengaturan pendaftaran |
| dosen | modul dan soal quiz, melihat ringkasan progres mahasiswa |
| mahasiswa | belajar, quiz, sertifikat, progres, paket/kursus |

Akun dibuat admin (tunggal atau massal CSV) dengan password sementara acak dan wajib diganti saat login pertama. `UG_ADMIN_PASSWORD` menentukan password awal admin di server.

## 4.9 Login Berdasarkan Peran, Tema, dan Bahasa
- **Login**: halaman login memiliki pilihan **Mahasiswa** (NPM/username + password) dan **Dosen** (username/NIDN + password), serta tautan "Masuk sebagai Admin". `auth.login(..., expected_role)` menolak akun yang perannya berbeda dari yang dipilih. Pendaftaran mandiri hanya untuk mahasiswa; akun dosen dibuat admin dengan password sementara yang wajib diganti (alasan keamanan: mencegah orang mengaku dosen).
- **Tema terang/gelap**: warna komponen memakai token Material (`ON_SURFACE`, `SURFACE`, `PRIMARY_CONTAINER`, dst.), sehingga mengikuti `page.theme_mode` tanpa menyimpan keadaan global. Tombol tema ada di header; pilihan disimpan di `page.client_storage` (per perangkat) dan, bila belum pernah memilih, mengikuti tema perangkat.
- **Bahasa Indonesia/Inggris**: `services/i18n.py` (kamus dua arah + pola untuk teks dinamis, tanpa dependensi UI) dan `components/i18n_ui.py` (menerjemahkan pohon kontrol Flet). Seluruh teks antarmuka, pelajaran, quiz, cheat sheet, roadmap, dan halaman info tersedia dalam dua bahasa; materi tambahan dari web (Wikipedia, Stack Overflow, dst.) tetap dalam bahasa aslinya. Teks yang belum ada terjemahannya dibiarkan, dan uji T56 memastikan teks baru di kode selalu didaftarkan.

## 4.10 Login Admin Berkode, Panel per Peran, dan Konten
- **Admin berkode**: `services/admin_code.py` (HMAC-SHA256 per menit, sekali pakai, toleransi 1 menit, kunci akun) dan `auth.login_admin`. Halaman login hanya menampilkan **Mahasiswa** dan **Dosen**; jalur admin tersembunyi (ketuk judul kartu 7 kali atau tautan `?key=`). Kunci rahasia dari `UG_ADMIN_KEY`/`admin_key.txt`; generator `tools/admin_generator.html` tidak menyimpan kunci di berkasnya.
- **Tiga panel**: Mahasiswa (Dashboard: progres, modul, sertifikat, paket, "lanjutkan belajar", ulangi quiz), Dosen (Panel Dosen: laporan mahasiswa + soal quiz; modul dari Dashboard), Admin (Ringkasan sistem, laporan, pengguna, buat akun, soal, log, data).
- **Konten terisi**: 12 bahasa x 4 pelajaran, 8 soal quiz per bahasa (96 soal), 108 entri cheat sheet, dan panel web yang selalu berisi karena ada ringkasan dan "Sumber Belajar Pilihan" bawaan saat offline; semuanya tersedia dalam Indonesia dan Inggris.
