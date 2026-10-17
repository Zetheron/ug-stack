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
