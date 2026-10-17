# BAB V - PENGUJIAN PROGRAM

## 5.1 Pengujian Otomatis (logika program)
Dijalankan dengan `python -m unittest tests.test_services tests.test_content tests.test_lanjutan tests.test_akun_server tests.test_i18n_login tests.test_admin_kode -v`. Hasil lengkap: `docs/hasil_unittest.txt` (**68 pengujian di enam berkas, semua OK**).

| ID | Skenario | Input | Proses | Output yang diharapkan | Hasil |
|---|---|---|---|---|---|
| T01 | Login berhasil | admin / Admin123 | cocokkan hash | login sukses, peran admin | OK |
| T02 | Login gagal | admin / salah123 | hash tidak cocok | gagal, "Sisa percobaan: 2" | OK |
| T03 | Input kosong | (kosong) | validasi | "wajib diisi" | OK |
| T04 | Akun terkunci | 3x password salah | hitung gagal | akun dikunci, login benar pun ditolak | OK |
| T05 | Password tidak polos | - | periksa users.json | password asli tidak ada di file | OK |
| T06 | Registrasi valid / ganda | siti_01 dua kali | cek username | pertama berhasil, kedua "sudah dipakai" | OK |
| T07 | Validasi registrasi | username kosong/pendek, password lemah, konfirmasi beda | validasi | semua ditolak | OK |
| T08 | Validasi modul | judul kosong, bahasa/level tidak valid, durasi huruf/0 | validasi | semua ditolak | OK |
| T09 | Tambah data | modul valid (admin) | tambah | jumlah modul +1 | OK |
| T10 | Otorisasi | tambah/ubah/hapus oleh mahasiswa | cek peran | ditolak | OK |
| T11 | Cari, filter, sort | kata kunci, bahasa, urut durasi | filter + sort | hasil sesuai; kata tak ada -> kosong | OK |
| T12 | Ubah data | ubah modul 1; ID 999 | update | berubah; ID 999 gagal | OK |
| T13 | Hapus data | hapus modul 2 | hapus + bersihkan progres | modul dan progres terkait hilang; hapus ulang gagal | OK |
| T14 | Progres | tandai/batal selesai | hitung persen | persen benar; daftar kosong -> 0 | OK |
| T15 | Simpan dan baca data | tambah modul lalu baca | tulis/baca JSON | data tersimpan dan terbaca | OK |
| T16 | File JSON rusak | isi file tidak valid | pulihkan | data bawaan dimuat, file `.corrupt` dibuat | OK |
| T17 | Folder tidak bisa ditulis | path tidak valid | tangani error | tidak crash, pesan kesalahan | OK |
| T18 | Kelengkapan konten | 12 bahasa | periksa pelajaran, referensi, soal (8 per bahasa) | tiap bahasa >= 4 pelajaran, >= 6 referensi, 8 soal | OK |
| T19 | Validitas soal quiz | semua soal | periksa opsi dan kunci | 4 opsi, kunci 0-3, ada penjelasan | OK |
| T20 | Pengenalan nama bahasa | "Python Tutorial", "C++", "JS Reference", "Rust" | normalisasi nama | bahasa benar; "Rust" -> tidak ada | OK |
| T21 | Penilaian quiz | semua benar / kosong / salah / 3 dari 4 | bandingkan dengan kunci | 100% lulus; 0% gagal; 75% lulus | OK |
| T22 | Skor dan sertifikat | gagal lalu lulus lalu gagal lagi | simpan skor terbaik | sertifikat baru ada setelah lulus; skor terbaik tidak turun | OK |
| T23 | Verifikasi sertifikat | kode asli (huruf kecil), kode palsu, kosong | cocokkan kode SHA-256 | asli valid; lainnya ditolak | OK |
| T24 | Pencarian materi | "flexbox", "python", "zzzxqj", "a" | cari bahasa/pelajaran/referensi | hasil sesuai; tak ada -> kosong; terlalu pendek -> kosong | OK |
| T25 | Parser sumber konten | contoh respons 6 sumber, respons kosong | ubah ke format internal | field benar, HTML di-unescape, tidak crash | OK |
| T26 | Cache segar | dua panggilan berturut-turut | baca cache | panggilan kedua dari cache, tanpa jaringan | OK |
| T27 | Offline | cache kedaluwarsa + jaringan mati; tanpa cache | fallback | cache lama dipakai; tanpa cache error diteruskan | OK |
| T28 | Algoritma buatan sendiri | data acak 0/1/2/17/200 elemen, naik dan turun | merge sort, insertion sort, pencarian biner/linear | sama persis dengan `sorted()` (termasuk stabil); biner menemukan indeks benar, -1 bila tak ada | OK |
| T29 | Modul memakai algoritma sendiri | sort judul/durasi/level; `get_module(5)`, `get_module(999)` | merge sort + pencarian biner | hasil benar; 999 -> tidak ditemukan | OK |
| T30 | Audit log | 12 entri, filter, halaman 1 dan 3; login gagal dengan password rahasia | paginasi `while` | 5/halaman, 3 halaman, terbaru dulu; password tidak ada di log | OK |
| T31 | Kunci akun persisten | 3x password salah | tulis `lockouts.json` | file ada; login benar pun ditolak saat terkunci | OK |
| T32 | Wajib ganti password admin bawaan | login admin/Admin123; ganti dengan data salah/lemah/beda/sama | `change_password` | semua ditolak kecuali yang valid; flag wajib ganti hilang; password lama tak berlaku | OK |
| T33 | Admin lama berpassword bawaan | users.json tanpa flag | `init_data` | flag `must_change` ditambahkan | OK |
| T34 | Manajemen pengguna | reset password, ubah peran, hapus; oleh mahasiswa dan admin | otorisasi + perlindungan admin terakhir | mahasiswa ditolak; admin terakhir dan akun sendiri dilindungi; progres/skor ikut terhapus | OK |
| T35 | Soal quiz kustom | tambah soal valid/tidak valid, hapus, nilai quiz | `quiz_admin` | validasi menolak data rusak; soal tergabung; total soal bertambah | OK |
| T36 | Ekspor/impor CSV | CSV hasil ekspor, kolom hilang, baris rusak/duplikat | `csv_io` | ringkasan dan nomor baris yang dilewati benar; non-admin ditolak | OK |
| T37 | Backup/restore | buat backup, ubah data, pulihkan; nama berbahaya; backup rusak | `backup` | data kembali; path traversal dan backup rusak ditolak tanpa mengubah data | OK |
| T38 | Konsol: alur admin | skrip input: login, ganti password, tambah, tampil, cari, ubah, hapus, log, logout | `cli.run` | semua pesan berhasil muncul; entri LOGOUT tercatat | OK |
| T39 | Konsol: mahasiswa dan input salah | daftar, 3x login salah, ID salah/tak ada, pilihan tak dikenal | `cli.run` | pesan kesalahan ramah; tidak crash | OK |
| T40 | Penulisan bersamaan | 15 thread registrasi serentak | `storage.LOCK` | 16 akun tersimpan, tidak ada data hilang | OK |
| T41 | Penyimpanan perangkat (APK) | register, tambah modul, "tutup" lalu "buka" aplikasi | `ClientStorageBackend` | data dan akun tetap ada; data rusak dipulihkan | OK |
| T42 | Penyimpanan PostgreSQL | koneksi pertama putus | `PostgresBackend` | koneksi diulang otomatis; baca/tulis/hapus benar | OK |
| T43 | `DATABASE_URL` | URL valid/tidak valid | `from_url`, `get_backend` | URL salah ditolak; backend database dipilih | OK |
| T44 | Admin membuat akun | dosen/mahasiswa; duplikat, username pendek, peran salah, password lemah, oleh non-admin | `create_user` | akun bisa login dengan password sementara; semua kasus salah ditolak | OK |
| T45 | Impor akun massal | CSV 6 baris campuran; 105 baris | `import_users_csv` | akun valid dibuat; baris salah dilaporkan; maks. 100 | OK |
| T46 | Hak dosen | dosen mengelola modul/soal; mencoba kelola akun/backup | otorisasi | konten boleh; akun, backup, pengaturan ditolak | OK |
| T47 | Ubah peran ke dosen | admin ubah peran mahasiswa | `set_role` | peran berubah; tidak lagi dihitung mahasiswa | OK |
| T48 | Pendaftaran mandiri | tutup/buka saklar | `settings` | saat ditutup registrasi ditolak, admin tetap bisa membuat akun | OK |
| T49 | Password admin dari server | `UG_ADMIN_PASSWORD` kuat/lemah | `init_data` | kuat dipakai tanpa paksa ganti; lemah kembali ke bawaan | OK |
| T50 | Paket dan kursus | pilih paket, daftar kursus, duplikat, tidak dikenal | `enrollment` | tersimpan; duplikat ditolak; ikut terhapus saat akun dihapus | OK |
| T51 | Backup lengkap | backup, ubah, pulihkan, >10 backup | `backup` | semua data (termasuk paket dan pengaturan) kembali; hanya 10 backup disimpan | OK |
| T52 | Konsol dosen | login dosen, wajib ganti password, tambah modul | `cli.run` | menu dosen tanpa log/ekspor; modul tersimpan | OK |
| T53 | Terjemahan dua arah dan pola | teks ID/EN, teks dinamis, teks tak dikenal, None, bahasa tak dikenal | `i18n.translate` | benar kedua arah; tak dikenal dibiarkan; tidak error | OK |
| T54 | Seluruh materi punya terjemahan | 48 pelajaran, 96 soal, 108 referensi | kamus dari `i18n_content_en` | setiap judul/paragraf/soal/penjelasan diterjemahkan | OK |
| T55 | Terjemahan pohon kontrol | kontrol tiruan (Text, tombol, field, dropdown) | `translate_tree` | label/tooltip berubah; isi pengguna, kunci data, dan kode tidak berubah | OK |
| T56 | Kelengkapan terjemahan di kode | semua teks tampilan hasil ekstraksi AST | cek ke kamus | tidak ada teks tanpa terjemahan (kecuali daftar merek/teknis) | OK |
| T57 | Login sesuai peran | NPM sebagai username; peran benar/salah untuk mahasiswa, dosen, admin | `login(expected_role)` | peran benar masuk; peran salah ditolak dengan pesan jelas | OK |
| T58 | Salah peran bukan percobaan gagal | 5x peran salah lalu 3x password salah | kunci akun | hanya password salah yang menghitung dan mengunci | OK |
| T59 | Registrasi mandiri = mahasiswa | daftar lewat `register` | peran akun | selalu mahasiswa; dosen/admin hanya lewat admin | OK |
| T60 | Kode admin HMAC-SHA256 | kunci uji, menit tertentu | `code_for_minute` | sama dengan HMAC independen (16 hex); berganti tiap menit; juga cocok dengan implementasi JavaScript generator | OK |
| T61 | Verifikasi kode | menit -1, 0, +1, +-2; dipakai ulang | `admin_code.verify` | diterima untuk menit -1..+1; kedaluwarsa ditolak; kode sekali pakai | OK |
| T62 | Format kode dan URL | kode polos, huruf besar, URL `?key=`, kode pendek/non-hex | `extract_code` | URL dan huruf besar diterima; format salah ditolak | OK |
| T63 | Kunci setelah 5 kode salah | 5 kode salah lalu kode benar | penghitung gagal | kode benar pun ditolak saat terkunci; diterima setelah 120 detik | OK |
| T64 | Tanpa kunci / kunci lokal otomatis | tanpa UG_ADMIN_KEY | `ensure_secret` | login admin nonaktif dengan pesan; kunci dibuat sekali di admin_key.txt | OK |
| T65 | Admin hanya lewat kode | password admin benar; kode benar; kode dipakai ulang; username bukan admin | `login`, `login_admin` | password admin ditolak; kode valid masuk; kode kedua dan non-admin ditolak | OK |
| T66 | Laporan mahasiswa | 3 mahasiswa dengan progres, skor, paket; oleh dosen, admin, mahasiswa | `student_overview` | terurut benar, filter nama, mahasiswa ditolak | OK |
| T67 | Statistik sistem | data campuran | `system_stats` | hitungan peran, sertifikat, percobaan, paket benar; hanya admin | OK |
| T68 | Ringkasan pribadi mahasiswa | progres dan skor | `student_summary` | modul berikutnya dan bahasa yang perlu diulang benar | OK |

## 5.2 Pengujian Manual pada Tampilan (isi screenshot sendiri)
Jalankan `python main.py`, lalu ambil screenshot setiap langkah.

| ID | Skenario | Langkah | Hasil yang diharapkan | Screenshot |
|---|---|---|---|---|
| M01 | Login berhasil | Login admin / Admin123 | masuk Dashboard, muncul nama dan peran | [tempel] |
| M02 | Login gagal | password salah | pesan merah "Sisa percobaan" | [tempel] |
| M03 | Input dan validasi | Tambah Modul dengan judul kosong | pesan validasi di dialog | [tempel] |
| M04 | Tambah data | isi form valid | modul baru muncul di daftar | [tempel] |
| M05 | Cari data | ketik "python" | hanya modul yang cocok | [tempel] |
| M06 | Ubah data | ikon pensil, ubah durasi | kartu menampilkan durasi baru | [tempel] |
| M07 | Hapus data | ikon tempat sampah, konfirmasi | kartu hilang | [tempel] |
| M08 | Simpan dan baca | tutup aplikasi, buka lagi, login | data terakhir masih ada | [tempel] |
| M09 | Logout | tombol Logout | kembali ke Beranda; Dashboard butuh login lagi | [tempel] |
| M10 | Responsif | kecilkan jendela < 768 px | menu hamburger, kartu 1 kolom | [tempel] |
| M11 | APK | pasang APK di HP | tampilan HP dan login berfungsi | [tempel] |
| M12 | Halaman tiap tombol | klik Tutorials, References, Exercises, Certificates, Roadmap, Upgrade, Paid Courses | tiap tombol membuka halaman sendiri | [tempel] |
| M13 | Pelajaran dan Try it | buka Python Tutorial, tekan Try it Yourself | kode pelajaran muncul di editor | [tempel] |
| M14 | Konten otomatis | buka halaman pelajaran dengan internet aktif | panel Wikipedia, Stack Overflow, DEV, GitHub (dan MDN untuk web) terisi | [tempel] |
| M15 | Mode offline | matikan internet, buka pelajaran yang pernah dibuka | konten tampil dari cache ("Offline - memakai cache lama") | [tempel] |
| M16 | Quiz dan sertifikat | login, jawab quiz benar semua, buka sertifikat | nilai 100%, sertifikat dengan kode verifikasi | [tempel] |
| M17 | Verifikasi kode | tempel kode ke kolom Verifikasi | "Valid: ..." | [tempel] |
| M18 | Pencarian | cari "flexbox" | hasil pelajaran/cheat sheet + panel web | [tempel] |
| M19 | Panel admin | login admin -> Dashboard -> Panel Admin: tab Pengguna, Soal Quiz, Log Aktivitas, Data | tiap tab tampil dan berfungsi | [tempel] |
| M20 | Wajib ganti password | login admin/Admin123 (data baru) | dialog ganti password tidak bisa ditutup sebelum berhasil | [tempel] |
| M21 | Ekspor/impor CSV dan backup | tab Data: ekspor, impor CSV dengan 1 baris salah, buat backup, pulihkan | pesan ringkasan sesuai | [tempel] |
| M22 | Versi konsol | `python cli.py`: login, tambah, cari, hapus, logout | menu `while` berjalan, pesan jelas | [tempel] |
| M23 | Tampilan HP | buka di HP (Jalur C panduan APK) atau lebar jendela 360 px | menu hamburger, kartu 1 kolom, dropdown pelajaran | [tempel] |
| M24 | APK | pasang APK; tutup dan buka lagi | login dan data tetap ada | [tempel] |
| M25 | Akun oleh admin | Panel Admin -> Buat Akun: buat dosen dan mahasiswa; salin password sementara | akun muncul di tab Pengguna; login pertama memaksa ganti password | [tempel] |
| M26 | Impor akun massal | tempel CSV 3 baris | daftar password sementara tampil dan bisa disalin | [tempel] |
| M27 | Login dosen | login akun dosen | Dashboard dengan tombol Kelola Soal Quiz; tidak ada Panel Admin | [tempel] |
| M28 | Paket dan kursus | login mahasiswa -> Upgrade -> Pilih paket; Paid Courses -> Daftar kursus | status "Paket aktif"/"Terdaftar" dan tampil di Dashboard | [tempel] |
| M29 | Data awet di APK | ganti password, tambah modul, tutup aplikasi sepenuhnya, buka lagi | password baru dan modul masih ada | [tempel] |
| M30 | Server online | buka alamat Render/Vercel, login admin, buat akun | berfungsi; data bertahan setelah layanan "tidur" lalu bangun | [tempel] |
| M31 | Pilihan peran di login | buka halaman Login; pilih Mahasiswa lalu Dosen; coba masuk dengan akun peran lain | form berubah (label NPM / NIDN); akun peran lain ditolak | [tempel] |
| M32 | Login dengan NPM | daftar dengan NPM 8 digit, login sebagai Mahasiswa | masuk Dashboard | [tempel] |
| M33 | Tema gelap | tekan ikon bulan di header; buka beranda, tutorial, dashboard, quiz, panel admin | semua teks terbaca; ikon berubah menjadi matahari | [tempel] |
| M34 | Tema tersimpan | pilih tema gelap, tutup dan buka aplikasi | tema tetap gelap | [tempel] |
| M35 | Bahasa Inggris | tekan tombol EN di header; buka tutorial, quiz, sertifikat, roadmap, dashboard | antarmuka dan materi berbahasa Inggris | [tempel] |
| M36 | Bahasa tersimpan | pilih EN, tutup dan buka aplikasi | tetap Inggris; tombol menampilkan ID | [tempel] |
| M37 | Halaman login tanpa admin | buka Login | hanya tombol Mahasiswa dan Dosen yang terlihat; tidak ada tautan admin | [tempel] |
| M38 | Masuk admin tersembunyi | ketuk judul kartu 7 kali; isi kode dari generator | dialog "Akses Khusus" muncul; kode benar masuk Panel Admin; kode lama/salah ditolak | [tempel] |
| M39 | Generator kode | buka tools/admin_generator.html, tempel kunci | kode berganti tiap 60 detik; kode sama dengan `python tools/admin_code.py` | [tempel] |
| M40 | Panel Dosen | login dosen -> Panel Dosen | tab Mahasiswa (progres, sertifikat, skor) dan Soal Quiz | [tempel] |
| M41 | Panel Admin | masuk admin | tab Ringkasan, Mahasiswa, Pengguna, Buat Akun, Soal, Log, Data berfungsi | [tempel] |
| M42 | Dashboard mahasiswa | login mahasiswa | progres, sertifikat, paket, tombol "Lanjutkan belajar" dan "Ulangi quiz" | [tempel] |
| M43 | Konten terisi di HP | buka tutorial dalam mode offline | ringkasan bawaan dan Sumber Belajar Pilihan tampil | [tempel] |

## 5.3 Bukti Pengujian Otomatis 11 Skenario Minimal
Berkas `docs/hasil_pengujian.md` dihasilkan oleh `python run_report.py` (input, output diharapkan, output aktual, status). Pemetaan ke ketentuan:

| Ketentuan dosen | Skenario di `run_report.py` | Tes unittest |
|---|---|---|
| Login berhasil | 1 | T01, T32 |
| Login gagal | 2 | T02, T04, T31 |
| Input data | 3 | T08, T09 |
| Validasi input | 4 | T07, T08, T35, T36 |
| Penambahan data | 5 | T09, T36 |
| Pencarian data | 6 | T11, T24, T28, T29 |
| Perubahan data | 7 | T12 |
| Penghapusan data | 8 | T13 |
| Penyimpanan data | 9 | T15, T37 |
| Pembacaan data | 10 | T15, T16 |
| Logout | 11 | T38 (konsol), M09 (tampilan) |
