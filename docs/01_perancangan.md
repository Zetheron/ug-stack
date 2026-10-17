# BAB I - PERANCANGAN APLIKASI

## 1.1 Latar Belakang / Permasalahan
Mahasiswa yang belajar pemrograman web sering kesulitan memantau modul mana yang sudah dipelajari, sedangkan pengelola materi (dosen/asisten) membutuhkan cara untuk mengatur daftar modul dan melihat perkembangan mahasiswa. Pencatatan manual rawan salah, tidak aman, dan sulit dicari.

UG-Stack dikembangkan menjadi platform belajar berbasis Python (Flet) dengan fitur login, pengelolaan modul, dan pelacakan progres belajar. Aplikasi berjalan sebagai **web responsif** dan dapat dibuat menjadi **APK Android**.

## 1.2 Tujuan Aplikasi
1. Mengelola data modul pembelajaran (tambah, tampil, cari, ubah, hapus, filter, urut).
2. Mencatat dan menghitung progres belajar tiap mahasiswa.
3. Membatasi akses data dengan autentikasi (login) dan otorisasi peran (admin / mahasiswa).
4. Menyimpan data secara permanen dalam file JSON.

## 1.3 Cara Kerja Aplikasi
Pengguna membuka Beranda dan dapat langsung menjelajahi halaman materi (Tutorial, Referensi, Latihan/Quiz, Sertifikat, Roadmap, Pencarian). Untuk menyimpan skor, mendapat sertifikat, dan membuka Dashboard, pengguna login atau mendaftar. Setelah login, Dashboard menampilkan modul sesuai peran:
- **Admin**: Panel Admin (ringkasan sistem, laporan mahasiswa, akun, soal quiz, log aktivitas, CSV, backup). Admin tidak muncul di halaman login dan hanya masuk dengan kode 60 detik.
- **Dosen**: Panel Dosen (laporan progres, sertifikat, dan skor tiap mahasiswa; mengelola modul dan soal quiz).
- **Mahasiswa**: mencari/memfilter/mengurutkan modul, menandai modul selesai, dan melihat persentase progres.

## 1.4 Data Input, Proses, dan Output
| Fitur | Input | Proses | Output |
|---|---|---|---|
| Registrasi | username, password, konfirmasi | validasi, hash PBKDF2 + salt, simpan | pesan berhasil / gagal |
| Login | username, password | cek kunci akun, cocokkan hash, hitung percobaan gagal | sesi pengguna, masuk Dashboard |
| Tambah/Ubah modul | judul, bahasa, level, durasi, deskripsi | cek peran admin, validasi, simpan | daftar modul diperbarui |
| Hapus modul | pilihan modul + konfirmasi | hapus modul dan progres terkait | daftar modul diperbarui |
| Cari/Filter/Urut | kata kunci, bahasa, kunci urut, arah | penyaringan linear + pengurutan | kartu modul + jumlah |
| Progres | pilihan modul | toggle selesai, hitung persen | progress bar + persentase |
| Tutorial / Referensi | pilihan bahasa dan pelajaran, kata filter | tampilkan materi bawaan, filter cheat sheet | pelajaran, contoh kode, tabel referensi |
| Konten otomatis | bahasa yang dibuka | ambil dari API tepercaya (cache 24 jam) | ringkasan Wikipedia, referensi MDN, pertanyaan Stack Overflow, artikel DEV, repositori GitHub |
| Quiz | jawaban pilihan ganda | nilai, bandingkan dengan kunci, simpan skor terbaik | nilai, penjelasan, status lulus |
| Sertifikat | hasil quiz lulus (>= 70%) / kode verifikasi | buat kode SHA-256, cocokkan kode | sertifikat dan hasil verifikasi |
| Pencarian | kata kunci | cari di bahasa, pelajaran, cheat sheet + web | daftar hasil bawaan dan dari web |
| Ganti password | password lama, baru, ulangi | verifikasi hash, validasi, hash baru | pesan berhasil / gagal; admin bawaan wajib ganti |
| Kelola pengguna (admin) | pilihan pengguna, password sementara, peran | reset, ubah peran, hapus (admin terakhir dilindungi) | daftar pengguna terbarui |
| Soal quiz kustom (admin) | bahasa, pertanyaan, 4 opsi, jawaban, penjelasan | validasi dan simpan | soal tambahan pada quiz |
| Log aktivitas (admin) | filter, nomor halaman | telusuri log dari terbaru (paginasi) | daftar kejadian |
| Ekspor/impor CSV, backup (admin) | teks CSV / pilihan backup | validasi tiap baris; salin dan pulihkan berkas | ringkasan baris berhasil/dilewati |
| Buat akun (admin) | username, peran (mahasiswa/dosen/admin), password sementara | validasi, password acak, hash, tanda wajib ganti | kredensial sementara untuk diberikan ke pengguna |
| Impor akun massal (admin) | CSV username,role | validasi tiap baris, buat password acak | daftar akun + password sementara |
| Pengaturan pendaftaran | saklar buka/tutup | simpan pengaturan | pendaftaran mandiri dibuka/ditutup |
| Paket dan kursus | pilihan paket / kursus | simpan langganan per pengguna | status paket/kursus di Dashboard |
| Login admin (kode berputar) | username admin + kode 16 karakter dari generator | HMAC-SHA256 per menit, sekali pakai, kunci akun 5x gagal | Panel Admin |
| Laporan mahasiswa / ringkasan sistem | kata kunci, kunci urut (dosen/admin) | gabung data progres, skor, paket; urut merge sort | kartu mahasiswa; statistik sistem |
| Login berdasarkan peran | pilihan peran (Mahasiswa/Dosen/Admin), NPM atau username, password | verifikasi hash + cek kecocokan peran | Dashboard sesuai peran |
| Tema dan bahasa | tombol tema (terang/gelap), tombol bahasa (ID/EN) | simpan preferensi per perangkat; terjemahkan tampilan | seluruh antarmuka dan materi dalam bahasa terpilih |
| Aplikasi konsol (`cli.py`) | angka menu dan isian lewat `input()` | memakai service yang sama | teks hasil lewat `print()` |

## 1.5 Struktur Data
Data disimpan lewat satu antarmuka (`load_json`/`save_json`) dengan tiga backend: **berkas JSON** (lokal), **penyimpanan perangkat Flet** (APK) dan **PostgreSQL** (server online). Tabel berikut menunjukkan nama dokumen data:
| File | Isi |
|---|---|
| `users.json` | daftar `{username, salt, password_hash, role, created_at}` |
| `modules.json` | daftar `{id, judul, bahasa, level, durasi, deskripsi}` |
| `progress.json` | kamus `{username: [id_modul_selesai, ...]}` |
| `scores.json` | `{username: {bahasa: {best, attempts, last, passed_at}}}` hasil quiz |
| `quiz_custom.json`, `lockouts.json`, `activity_log.json` | soal kustom, penghitung kunci akun, log aktivitas |
| `enrollments.json`, `settings.json` | paket/kursus per pengguna, pengaturan pendaftaran |
| `cache_*.json` | cache konten web `{ts, data}` (dibuat otomatis, berlaku 24 jam) |
| `content/*.py` | materi bawaan: 12 bahasa x 4 pelajaran, cheat sheet, bank soal quiz, roadmap, halaman info |

Akun admin bawaan dibuat otomatis saat pertama kali dijalankan: `admin` / `Admin123`.

## 1.6 Sumber Konten Otomatis
| Sumber | Data yang diambil | Kegunaan |
|---|---|---|
| Wikipedia (REST API) | ringkasan artikel, hasil pencarian | pengantar bahasa, pencarian umum |
| MDN Web Docs (API pencarian) | dokumen referensi | referensi HTML, CSS, JavaScript |
| Stack Overflow (Stack Exchange API) | pertanyaan terpopuler / hasil pencarian | masalah nyata yang sering dijumpai |
| DEV Community (Forem API) | artikel populer per topik | bacaan lanjutan dari komunitas |
| GitHub (Search API) | repositori berbintang terbanyak | contoh proyek nyata |

Semua tampil dengan tautan ke sumber aslinya dan hanya berupa ringkasan; konten berlisensi CC BY-SA tetap milik penulis aslinya.
