# LAPORAN TUGAS - ALGORITMA DAN PEMROGRAMAN 3

Nama: [isi]  |  NPM: [isi]  |  Kelas: [isi]  |  Dosen: [isi]

---

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

# BAB II - ALGORITMA DAN PSEUDOCODE

Algoritma umum: **Input -> Validasi -> Proses data (baca/ubah) -> Simpan -> Output pesan/tampilan.**

## 2.1 Login (`auth.login`)
```
FUNCTION login(username, password)
    username <- trim(username)
    IF username kosong ATAU password kosong THEN RETURN gagal("wajib diisi")
    (jumlah_gagal, waktu_buka) <- baca lockouts.json [username]     // tersimpan di file
    IF waktu_buka > sekarang THEN RETURN gagal("akun terkunci, tunggu N detik")
    TRY
        users <- baca users.json
    CATCH kesalahan file THEN RETURN gagal(pesan kesalahan)
    user <- cari username di users (pencarian linear)
    IF user ditemukan THEN hash <- PBKDF2(password, user.salt)
    ELSE hash <- PBKDF2(password, salt_tiruan)           // samakan waktu proses
    valid <- user ada DAN (hash = user.password_hash)
    IF valid THEN
        hapus catatan gagal; catat audit LOGIN_OK
        RETURN berhasil(username, role, wajib_ganti)
    jumlah_gagal <- jumlah_gagal + 1
    IF jumlah_gagal >= 3 THEN
        percobaan[username] <- (0, sekarang + 30 detik)
        RETURN gagal("akun dikunci 30 detik")
    percobaan[username] <- (jumlah_gagal, 0)
    RETURN gagal("salah, sisa percobaan = 3 - jumlah_gagal")
END FUNCTION
```

## 2.2 Registrasi (`auth.register`)
```
FUNCTION register(username, password, konfirmasi)
    IF username tidak valid (4-20 huruf/angka/_) THEN RETURN gagal
    IF password tidak valid (min 8, ada huruf dan angka) THEN RETURN gagal
    IF password <> konfirmasi THEN RETURN gagal
    TRY
        users <- baca users.json
        IF username sudah ada di users THEN RETURN gagal("sudah dipakai")
        salt <- acak 16 byte; hash <- PBKDF2(password, salt)
        tambahkan {username, salt, hash, role="mahasiswa"} ke users
        simpan users.json
    CATCH kesalahan file THEN RETURN gagal(pesan)
    RETURN berhasil
END FUNCTION
```

## 2.3 Tambah / Ubah Modul (`modules.add_module`, `modules.update_module`)
```
FUNCTION simpan_modul(user, data, id_modul = KOSONG)
    IF user bukan admin THEN RETURN gagal("hanya admin")
    IF NOT valid(data) THEN RETURN gagal(pesan validasi)
    TRY
        daftar <- baca modules.json
        IF id_modul KOSONG THEN                      // mode tambah
            data.id <- (ID terbesar di daftar) + 1
            tambahkan data ke daftar
        ELSE                                         // mode ubah
            FOR setiap modul DI daftar
                IF modul.id = id_modul THEN ganti dengan data; tandai ditemukan
            IF tidak ditemukan THEN RETURN gagal("modul tidak ditemukan")
        simpan modules.json
    CATCH kesalahan file THEN RETURN gagal(pesan)
    RETURN berhasil
END FUNCTION
```

## 2.4 Hapus Modul (`modules.delete_module`)
```
FUNCTION hapus_modul(user, id_modul)
    IF user bukan admin THEN RETURN gagal
    TRY
        daftar <- baca modules.json
        sisa <- semua modul yang id-nya <> id_modul
        IF panjang(sisa) = panjang(daftar) THEN RETURN gagal("tidak ditemukan")
        simpan sisa ke modules.json
        buang id_modul dari progres semua mahasiswa; simpan progress.json
    CATCH kesalahan file THEN RETURN gagal(pesan)
    RETURN berhasil
END FUNCTION
```

## 2.5 Cari, Filter, Urut (`modules.search_modules`)
```
FUNCTION cari(daftar, kata_kunci, bahasa, kunci_urut, menurun)
    hasil <- []
    FOR setiap modul DI daftar
        IF bahasa <> "Semua" DAN modul.bahasa <> bahasa THEN LANJUT
        IF kata_kunci tidak kosong DAN kata_kunci tidak ada di judul/deskripsi THEN LANJUT
        tambahkan modul ke hasil
    urutkan hasil menurut kunci_urut (judul | durasi | level), arah menurun/naik
    RETURN hasil
END FUNCTION
```

## 2.6 Progres Belajar (`progress.toggle_done`, `progress.percent`)
```
FUNCTION toggle(username, id_modul)
    data <- baca progress.json
    IF id_modul ADA di data[username] THEN hapus id_modul   // batal selesai
    ELSE tambahkan id_modul                                  // selesai
    simpan progress.json

FUNCTION persen(daftar_selesai, daftar_id_modul)
    IF daftar_id_modul kosong THEN RETURN 0
    jumlah <- 0
    FOR setiap id DI daftar_id_modul
        IF id ADA di daftar_selesai THEN jumlah <- jumlah + 1
    RETURN jumlah * 100 / panjang(daftar_id_modul)
```

## 2.7 Baca / Simpan Data (`storage.load_json`, `storage.save_json`)
```
FUNCTION load_json(nama, bawaan)
    IF file tidak ada THEN simpan bawaan; RETURN bawaan
    TRY RETURN isi file sebagai JSON
    CATCH JSON rusak THEN ganti nama file menjadi .corrupt; simpan bawaan; RETURN bawaan
    CATCH kesalahan OS THEN lempar StorageError

FUNCTION save_json(nama, data)
    tulis ke file sementara; ganti file asli dengan file sementara   // tulis atomik
```

## 2.8 Konten Otomatis dengan Cache (`web_sources.cached`)
```
FUNCTION ambil_konten(kunci, pengambil, umur_maks = 24 jam)
    entri <- baca file cache[kunci]
    IF entri ada DAN (sekarang - entri.waktu) < umur_maks THEN
        RETURN (entri.data, "cache")
    TRY
        data <- pengambil()                 // panggil API sumber, batas waktu 6 detik
    CATCH kesalahan jaringan/parsing
        IF entri ada THEN RETURN (entri.data, "stale")   // offline: pakai cache lama
        LEMPAR kesalahan                                  // UI menampilkan pesan ramah
    simpan {waktu = sekarang, data} ke cache[kunci]
    RETURN (data, "live")
END FUNCTION
```

## 2.9 Penilaian Quiz dan Sertifikat (`quiz.grade`, `quiz.save_result`, `quiz.certificate`)
```
FUNCTION nilai(bahasa, jawaban)
    benar <- 0
    FOR setiap soal ke-i DI bank_soal[bahasa]
        IF jawaban[i] = soal.kunci THEN benar <- benar + 1
    persen <- benar * 100 / jumlah_soal
    RETURN (benar, persen, lulus = persen >= 70)

FUNCTION simpan_hasil(pengguna, bahasa, hasil)
    rekam <- skor[pengguna][bahasa]  (bawaan: terbaik 0, percobaan 0, tanggal_lulus KOSONG)
    rekam.percobaan <- rekam.percobaan + 1
    rekam.terbaik <- MAX(rekam.terbaik, persen)
    IF hasil.lulus DAN rekam.tanggal_lulus KOSONG THEN rekam.tanggal_lulus <- sekarang
    simpan scores.json

FUNCTION sertifikat(pengguna, bahasa)
    IF tanggal_lulus KOSONG THEN RETURN KOSONG
    kode <- 10 karakter pertama SHA-256(pengguna | bahasa | tanggal_lulus), huruf besar
    RETURN {pengguna, bahasa, nilai terbaik, tanggal, kode}

FUNCTION verifikasi(kode)
    FOR setiap pengguna, bahasa DI scores
        IF kode sama dengan kode sertifikat(pengguna, bahasa) THEN RETURN sertifikat itu
    RETURN KOSONG
```

## 2.10 Pencarian Materi (`content_search.search_content`)
```
FUNCTION cari_materi(kata_kunci)
    IF panjang(kata_kunci) < 2 THEN RETURN hasil kosong
    FOR setiap bahasa: jika nama atau tagline memuat kata_kunci, tambahkan
    FOR setiap pelajaran: jika judul/isi/kode memuat kata_kunci, tambahkan
    FOR setiap entri cheat sheet: jika sintaks/penjelasan memuat kata_kunci, tambahkan
    RETURN tiga daftar hasil
```

## 2.11 Pencarian Biner (`algorithms.binary_search`, dipakai `modules.get_module`)
```
FUNCTION cari_biner(data_terurut, target, kunci)
    rendah <- 0; tinggi <- panjang(data_terurut) - 1
    WHILE rendah <= tinggi
        tengah <- (rendah + tinggi) DIV 2
        IF kunci(data[tengah]) = target THEN RETURN tengah
        IF kunci(data[tengah]) < target THEN rendah <- tengah + 1
        ELSE tinggi <- tengah - 1
    RETURN -1
```

## 2.12 Merge Sort (`algorithms.merge_sort`, dipakai `modules.search_modules`)
```
FUNCTION merge_sort(data, kunci, menurun)
    IF panjang(data) <= 1 THEN RETURN salinan data
    kiri <- merge_sort(paruh pertama); kanan <- merge_sort(paruh kedua)
    hasil <- []; i <- 0; j <- 0
    WHILE i < panjang(kiri) DAN j < panjang(kanan)
        kiri_dulu <- (kunci(kiri[i]) <= kunci(kanan[j]))   // menurun: >=
        IF kiri_dulu THEN tambah kiri[i]; i <- i + 1 ELSE tambah kanan[j]; j <- j + 1
    tambahkan sisa kiri dan sisa kanan; RETURN hasil
```

## 2.13 Impor CSV (`csv_io.import_modules_csv`)
```
FUNCTION impor_csv(user, teks)
    IF user bukan admin THEN RETURN gagal
    IF teks kosong ATAU terlalu besar THEN RETURN gagal
    IF kolom wajib tidak lengkap THEN RETURN gagal
    tambah <- 0; lewati <- []
    FOR setiap baris DI csv
        IF baris tidak valid THEN catat (nomor, alasan); LANJUT
        IF (judul, bahasa) sudah ada THEN catat duplikat; LANJUT
        beri ID baru; tambahkan ke daftar; tambah <- tambah + 1
    IF tambah > 0 THEN simpan modules.json
    catat audit; RETURN (tambah, lewati)
```

## 2.14 Ganti Password (`auth.change_password`)
```
FUNCTION ganti_password(username, lama, baru, ulang)
    IF baru tidak valid THEN RETURN gagal; IF baru <> ulang THEN RETURN gagal
    IF hash(lama) <> hash tersimpan THEN RETURN gagal("password lama salah")
    IF lama = baru THEN RETURN gagal
    buat salt baru; simpan hash(baru); hapus tanda wajib_ganti; catat audit
```

## 2.15 Kelola Pengguna (admin) dan Log Aktivitas
```
FUNCTION hapus_pengguna(admin, target)
    IF admin bukan admin THEN RETURN gagal
    IF target = admin sendiri THEN RETURN gagal
    IF target adalah admin terakhir THEN RETURN gagal
    hapus pengguna, progres, dan skornya; catat audit

FUNCTION daftar_log(halaman, per_halaman, kata)
    i <- panjang(log) - 1; total <- 0; hasil <- []
    WHILE i >= 0                                  // dari terbaru ke terlama
        IF entri[i] cocok kata THEN
            total <- total + 1
            IF total > (halaman - 1) * per_halaman DAN panjang(hasil) < per_halaman THEN tambah entri[i]
        i <- i - 1
    RETURN (hasil, ceil(total / per_halaman), total)
```

## 2.16 Menu Konsol (`cli.run`)
```
init_data
WHILE benar
    tampilkan menu awal; baca pilihan
    IF pilihan = 1 THEN login (maks. 3 kali); IF berhasil THEN wajib ganti password bila perlu; menu_pengguna
    ELSE IF pilihan = 2 THEN registrasi
    ELSE IF pilihan = 0 THEN KELUAR
    ELSE tampilkan "pilihan tidak dikenal"

FUNCTION menu_pengguna(user)
    WHILE benar
        tampilkan menu sesuai peran; baca pilihan
        IF 9 THEN catat LOGOUT; RETURN logout
        IF 0 THEN RETURN keluar
        IF 1..n THEN jalankan aksi (tampil, cari, tambah, ubah, hapus, ekspor, log, progres, ganti password)
```

## 2.17 Admin Membuat Akun (`auth.create_user`, `auth.import_users_csv`)
```
FUNCTION buat_akun(admin, username, peran, password_sementara)
    IF admin bukan admin THEN RETURN gagal
    IF peran tidak ada di (admin, dosen, mahasiswa) THEN RETURN gagal
    IF username tidak valid THEN RETURN gagal
    IF password_sementara kosong THEN password <- acak 12 karakter (huruf besar, kecil, angka)
    IF password tidak valid THEN RETURN gagal
    IF username sudah ada THEN RETURN gagal
    simpan akun {username, peran, hash(password + salt acak), wajib_ganti = benar}; catat audit
    RETURN (berhasil, password)

FUNCTION impor_akun(admin, teks_csv)
    cek admin, teks tidak kosong, kolom username ada
    FOR setiap baris DI csv (maksimum 100)
        peran <- kolom role, atau "mahasiswa" bila kosong
        IF username tidak valid ATAU peran tidak valid ATAU sudah ada THEN catat (nomor baris, alasan); LANJUT
        buat password acak; tambahkan akun dengan wajib_ganti = benar
    simpan sekali; RETURN (daftar akun + password sementara, daftar baris dilewati)
```

## 2.18 Pemilihan Penyimpanan (`storage.get_backend`)
```
IF variabel DATABASE_URL ada THEN backend <- PostgreSQL
ELSE IF berjalan sebagai aplikasi Android/iOS (bukan web) THEN backend <- penyimpanan perangkat Flet
ELSE backend <- berkas JSON di folder data

FUNCTION load_json(nama, bawaan)
    teks <- backend.baca(nama)
    IF teks KOSONG THEN simpan bawaan; RETURN bawaan
    TRY RETURN json(teks)
    CATCH JSON rusak THEN backend.tulis(nama + ".corrupt", teks); simpan bawaan; RETURN bawaan
```

## 2.19 Pendaftaran Mandiri dan Paket/Kursus
```
FUNCTION register(...)
    IF pengaturan.pendaftaran_dibuka = salah THEN RETURN gagal("hubungi admin")
    ... (lanjut seperti 2.2)

FUNCTION daftar_kursus(pengguna, bahasa)
    IF bahasa tidak dikenal THEN RETURN gagal
    IF bahasa sudah ada di kursus pengguna THEN RETURN gagal("sudah terdaftar")
    tambahkan bahasa ke kursus pengguna; simpan; catat audit
```

## 2.20 Login Berdasarkan Peran (`auth.login` dengan `expected_role`)
```
FUNCTION login(username, password, peran_dipilih)
    ... cek kosong, kunci akun, baca data, verifikasi hash (lihat 2.1) ...
    IF verifikasi berhasil THEN
        IF peran_dipilih ADA DAN peran_akun <> peran_dipilih THEN
            catat audit LOGIN_PERAN_SALAH            // password benar: BUKAN percobaan gagal
            RETURN gagal("akun terdaftar sebagai " + peran_akun)
        catat audit LOGIN_OK; RETURN berhasil(username, peran, wajib_ganti)
    ... (password salah: hitung percobaan dan kunci akun seperti 2.1) ...
```
Pendaftaran mandiri hanya membuat peran **mahasiswa**; akun dosen dan admin hanya dibuat admin (2.17).

## 2.21 Terjemahan Antarmuka (`services/i18n.translate`)
```
FUNCTION terjemahkan(teks, bahasa)
    IF teks kosong ATAU bahasa tidak dikenal THEN RETURN teks
    IF (bahasa, teks) ada di cache THEN RETURN cache
    hasil <- kamus[bahasa][teks]
    IF hasil KOSONG THEN
        FOR setiap pola DI daftar_pola (paling spesifik dulu)
            IF teks cocok pola THEN isi templat dengan bagian-bagian yang cocok (diterjemahkan lewat kamus); BERHENTI
    IF hasil KOSONG THEN hasil <- teks            // tidak dikenal: dibiarkan
    simpan ke cache; RETURN hasil

PROSEDUR terjemahkan_pohon(kontrol, bahasa)
    tumpukan <- [kontrol]
    WHILE tumpukan tidak kosong
        c <- ambil dari tumpukan
        terjemahkan atribut teks c (value/label/hint/text/tooltip); tambahkan anak-anak c ke tumpukan
```

## 2.22 Login Admin dengan Kode Berputar (`admin_code.verify`, `auth.login_admin`)
```
FUNCTION kode_untuk_menit(kunci, menit)
    RETURN 16 karakter hex pertama dari HMAC-SHA256(kunci, teks(menit))

FUNCTION verifikasi(teks_kode)
    IF kunci admin tidak ada THEN RETURN gagal("belum dikonfigurasi")
    menit <- lantai(waktu_sekarang / 60)
    IF terkunci THEN RETURN gagal("coba lagi dalam N detik")
    kode <- ambil kode dari teks (parameter key= bila berupa URL), huruf kecil
    cocok <- KOSONG
    IF kode terdiri dari 16 hex THEN
        FOR m DARI menit-1 SAMPAI menit+1
            IF kode = kode_untuk_menit(kunci, m) (perbandingan waktu-konstan) THEN cocok <- m
    IF cocok ADA THEN
        IF kode sudah ada di daftar terpakai THEN RETURN gagal("sudah dipakai")
        simpan kode ke daftar terpakai; hapus catatan gagal; RETURN berhasil
    gagal <- gagal + 1
    IF gagal >= 5 THEN kunci 120 detik
    catat audit ADMIN_KODE_GAGAL; RETURN gagal("kode salah atau kedaluwarsa")

FUNCTION login_admin(username, teks_kode)
    hasil <- verifikasi(teks_kode); IF gagal THEN RETURN hasil
    akun <- cari username (bawaan "admin") dengan peran admin
    IF akun KOSONG THEN RETURN gagal("akun admin tidak ditemukan")
    catat LOGIN_ADMIN_KODE; RETURN berhasil(akun)
```
`auth.login` (password) menolak akun berperan admin, sehingga admin hanya bisa masuk lewat `login_admin`.

## 2.23 Laporan Mahasiswa (`reports.student_overview`)
```
FUNCTION laporan(pengguna, kata, kunci, menurun)
    IF pengguna bukan admin/dosen THEN RETURN []
    modul <- semua ID modul; baris <- []; i <- 0
    WHILE i < jumlah pengguna
        IF peran[i] = mahasiswa DAN nama[i] memuat kata THEN
            persen <- selesai / jumlah modul * 100
            sertifikat <- jumlah bahasa yang lulus quiz; rata <- rata skor terbaik
            tambahkan {nama, persen, sertifikat, rata, paket, kursus} ke baris
        i <- i + 1
    RETURN merge_sort(baris, kunci, menurun)
```

# BAB III - FLOWCHART

Flowchart dibuat mengikuti alur fungsi yang benar-benar diimplementasikan (lihat tabel pemetaan di Bab VI). Berkas sumber `.dot` ada di `docs/flowchart/`.

![Flowchart 1](flowchart/01_alur_utama.png)

![Flowchart 2](flowchart/02_login.png)

![Flowchart 3](flowchart/03_registrasi.png)

![Flowchart 4](flowchart/04_tambah_ubah_modul.png)

![Flowchart 5](flowchart/05_hapus_modul.png)

![Flowchart 6](flowchart/06_cari_filter_sort.png)

![Flowchart 7](flowchart/07_progres_belajar.png)

![Flowchart 8](flowchart/08_konten_otomatis.png)

![Flowchart 9](flowchart/09_quiz_sertifikat.png)

![Flowchart 10](flowchart/10_pencarian_biner.png)

![Flowchart 11](flowchart/11_merge_sort.png)

![Flowchart 12](flowchart/12_menu_konsol.png)

![Flowchart 13](flowchart/13_impor_csv.png)

![Flowchart 14](flowchart/14_ganti_password.png)

![Flowchart 15](flowchart/15_buat_akun_admin.png)

![Flowchart 16](flowchart/16_pemilihan_penyimpanan.png)

![Flowchart 17](flowchart/17_login_peran.png)

![Flowchart 18](flowchart/18_tema_bahasa.png)

![Flowchart 19](flowchart/19_login_admin_kode.png)

![Flowchart 20](flowchart/20_laporan_mahasiswa.png)

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

# BAB VI - ANALISIS PROGRAM

## 6.1 Hubungan Algoritma dan Implementasi
| Rancangan | Implementasi |
|---|---|
| Pseudocode 2.1 / Flowchart 2 (Login) | `services/auth.py` -> `login()` |
| Pseudocode 2.2 / Flowchart 3 (Registrasi) | `services/auth.py` -> `register()` dan `validators.py` |
| Pseudocode 2.3 / Flowchart 4 (Tambah/Ubah) | `services/modules.py` -> `add_module()`, `update_module()` |
| Pseudocode 2.4 / Flowchart 5 (Hapus) | `services/modules.py` -> `delete_module()`, `progress.remove_module()` |
| Pseudocode 2.5 / Flowchart 6 (Cari/Filter/Urut) | `services/modules.py` -> `search_modules()` |
| Pseudocode 2.6 / Flowchart 7 (Progres) | `services/progress.py` -> `toggle_done()`, `percent()` |
| Pseudocode 2.7 (Penyimpanan) | `services/storage.py` -> `load_json()`, `save_json()` |
| Pseudocode 2.8 / Flowchart 8 (Konten otomatis) | `services/web_sources.py` -> `cached()`, `components/live.py` -> `source_panel()` |
| Pseudocode 2.9 / Flowchart 9 (Quiz, sertifikat) | `services/quiz.py` -> `grade()`, `save_result()`, `certificate()`, `verify_certificate()` |
| Pseudocode 2.10 (Pencarian materi) | `services/content_search.py` -> `search_content()` |
| Pseudocode 2.11 / Flowchart 10 (Pencarian biner) | `services/algorithms.py` -> `binary_search()`, dipakai `modules.get_module()` |
| Pseudocode 2.12 / Flowchart 11 (Merge sort) | `services/algorithms.py` -> `merge_sort()`, dipakai `modules.search_modules()` |
| Pseudocode 2.13 / Flowchart 13 (Impor CSV) | `services/csv_io.py` -> `import_modules_csv()` |
| Pseudocode 2.14 / Flowchart 14 (Ganti password) | `services/auth.py` -> `change_password()`; `views/account.py` |
| Pseudocode 2.15 (Kelola pengguna, log) | `services/auth.py`, `services/audit.py` |
| Pseudocode 2.16 / Flowchart 12 (Menu konsol) | `cli.py` -> `run()`, `menu_pengguna()` |
| Pseudocode 2.17 / Flowchart 15 (Buat akun) | `services/auth.py` -> `create_user()`, `import_users_csv()`, `generate_password()` |
| Pseudocode 2.18 / Flowchart 16 (Penyimpanan) | `services/storage.py` -> `get_backend()`, `load_json()`; `main.py` memilih backend APK |
| Pseudocode 2.19 (Pendaftaran, kursus) | `services/settings.py`, `services/enrollment.py` |
| Pseudocode 2.20 / Flowchart 17 (Login per peran) | `services/auth.py` -> `login(expected_role)`; `views/auth_view.py` |
| Pseudocode 2.21 / Flowchart 18 (Tema, bahasa) | `services/i18n.py`, `components/i18n_ui.py`; `main.py` (preferensi) |
| Pseudocode 2.22 / Flowchart 19 (Login admin berkode) | `services/admin_code.py`, `auth.login_admin()`; `views/auth_view.py` (jalur tersembunyi) |
| Pseudocode 2.23 / Flowchart 20 (Laporan mahasiswa) | `services/reports.py` -> `student_overview()`, `system_stats()`, `student_summary()` |
| Flowchart 1 (Alur utama) | `main.py` -> `render()`, `go()`, kontrol akses `PROTECTED_VIEWS` |

## 6.2 Cara Kerja, Modularitas, Pengolahan Data
- Logika dipisah dari tampilan (`services/` vs `views/`), sehingga logika bisa diuji tanpa UI dan mudah dikembangkan.
- Setiap function mengembalikan pasangan `(ok, pesan)` sehingga UI cukup menampilkan pesan tanpa mengulang validasi.
- Pencarian memakai penelusuran linear O(n); cukup untuk puluhan hingga ribuan modul. Pengurutan memakai `sorted()` dengan fungsi kunci (O(n log n)).

## 6.2a Analisis Kompleksitas dan Hasil Pengukuran
| Algoritma | Waktu terbaik | Rata-rata | Terburuk | Catatan |
|---|---|---|---|---|
| Pencarian linear | O(1) | O(n) | O(n) | tidak butuh data terurut |
| Pencarian biner | O(1) | O(log n) | O(log n) | data harus terurut; dipakai pada daftar modul yang tersimpan menurut ID |
| Insertion sort | O(n) | O(n^2) | O(n^2) | sederhana, cocok data kecil/hampir terurut |
| Merge sort | O(n log n) | O(n log n) | O(n log n) | stabil, butuh memori tambahan O(n); dipakai di aplikasi |

Hasil pengukuran (`python benchmark.py`, waktu dalam milidetik, data acak):

| n | insertion sort (ms) | merge sort (ms) | sorted() bawaan (ms) | linear search (ms) | binary search (ms) |
|---|---|---|---|---|---|
| 100 | 0.210 | 0.096 | 0.003 | 0.0030 | 0.00049 |
| 1000 | 26.794 | 1.076 | 0.064 | 0.0266 | 0.00090 |
| 5000 | 642.260 | 8.568 | 0.549 | 0.1752 | 0.00114 |

Pada 5.000 data, insertion sort (sekitar 640 ms) jauh lebih lambat daripada merge sort (sekitar 9 ms), sesuai teori O(n^2) vs O(n log n). `sorted()` bawaan Python tetap tercepat karena ditulis dalam bahasa C. Pencarian biner kira-kira 150 kali lebih cepat daripada pencarian linear pada 5.000 data. Aplikasi memakai merge sort buatan sendiri untuk menunjukkan penerapan algoritma; untuk data sangat besar `sorted()` lebih tepat.

## 6.3 Validasi dan Keamanan
- Semua input divalidasi di layer service, bukan hanya di tampilan.
- Password tidak disimpan polos: PBKDF2-SHA256 (100.000 iterasi) dengan salt acak per pengguna; pembandingan memakai `hmac.compare_digest`.
- Pesan login gagal tidak membedakan "username salah" dan "password salah"; akun dikunci 30 detik setelah 3 kegagalan.
- Otorisasi diperiksa di service (`is_admin`), jadi mahasiswa tetap tidak bisa mengubah data walau tombol dimanipulasi.

## 6.4 Keterbatasan
- Penyimpanan file JSON cocok untuk skala tugas. `threading.RLock` mencegah bentrok antarsesi dalam satu proses, tetapi bila dijalankan sebagai beberapa proses server sekaligus diperlukan database.
- Sesi login hilang saat halaman dimuat ulang. Batas waktu sesi (15 menit) diperiksa saat pengguna berpindah halaman, bukan oleh pewaktu latar belakang.
- Penayangan online memerlukan server yang mendukung WebSocket (Render, dll.); Vercel serverless tidak mendukung Flet. Paket gratis Render tidur saat sepi.
- Penyimpanan perangkat pada APK bersifat lokal per HP: akun di APK tidak dibagi dengan versi server online.
- Materi tambahan dari web (Wikipedia, Stack Overflow, dst.) tidak diterjemahkan; pencarian materi bawaan memakai kata kunci bahasa Indonesia.
- Editor "Try it" bersifat simulasi tampilan, bukan eksekusi kode sungguhan (menjalankan kode pengguna memerlukan sandbox demi keamanan).
- Konten dari web bergantung pada ketersediaan dan batas pemakaian API publik (mis. Stack Exchange dan GitHub membatasi permintaan tanpa kunci); cache 24 jam mengurangi risiko ini.
- Materi bawaan baru 4 pelajaran per bahasa; dapat ditambah di `content/lessons.py` tanpa mengubah kode lain.

# BAB VII - KESIMPULAN
Aplikasi UG-Stack berhasil dikembangkan menjadi aplikasi Python yang memenuhi spesifikasi: perancangan, algoritma, pseudocode, flowchart, implementasi modular, pengolahan dan penyimpanan data JSON, validasi serta penanganan kesalahan, keamanan akses berbasis login dan peran, konten materi dan quiz yang diperkaya otomatis dari sumber tepercaya, serta pengujian (27 pengujian otomatis lulus). Aplikasi dapat dijalankan sebagai web responsif dan dikemas menjadi APK Android.


# LAMPIRAN - MATRIKS KETERLACAKAN KETENTUAN DOSEN

| No | Ketentuan | Bukti pada proyek | Dokumen | Tes |
|---|---|---|---|---|
| 1 | Perancangan aplikasi | Bab I | `01_perancangan.md` | - |
| 2 | Perancangan algoritma | Pseudocode 2.1-2.16 | `02_pseudocode.md` | - |
| 3 | Pseudocode | Bab II | `02_pseudocode.md` | - |
| 4 | Flowchart sesuai program | 14 flowchart dari `make_flowcharts.py` | `03_flowchart.md` | - |
| 5 | Konsep dasar (variabel, operator, I/O, if/elif/else, for/while, struktur data, function) | seluruh `services/`, `cli.py` (I/O konsol dan `while`) | Bab IV 4.2 | T01-T68 |
| 6 | Function dan modularitas | `services/` (satu fungsi satu tugas) | Bab IV 4.1 | T01-T68 |
| 7 | Pengolahan data (CRUD, filter, sort, hitung) | `modules.py`, `algorithms.py`, `progress.py`, `quiz.py`, `csv_io.py` | Bab IV | T09-T14, T28-T29, T36 |
| 8 | Penyimpanan data | `storage.py`, `backup.py`, `csv_io.py` | Bab IV | T15-T17, T36, T37 |
| 9 | Validasi dan penanganan kesalahan | `validators.py`, `StorageError`, `try/except` | Bab IV 4.2 | T07, T08, T16, T17, T35, T39 |
| 10 | Keamanan akses | `auth.py`, `roles.py`, `audit.py`, peran admin/dosen/mahasiswa | Bab IV 4.6, 4.8 | T01-T06, T31-T34, T44-T49, T60-T65 |
| 11 | Pengujian minimal | 68 unittest + `run_report.py` (11 skenario) | Bab V, `hasil_pengujian.md` | semua |
| 12 | Analisis program | Bab VI, kompleksitas, benchmark | Bab VI | - |
