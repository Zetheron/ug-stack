# Panduan: Login Admin dengan Kode 60 Detik

Admin **tidak** memakai password dan **tidak ada** pilihan admin di halaman login (hanya Mahasiswa dan Dosen).
Admin masuk dengan kode 16 karakter yang berganti setiap 60 detik dan hanya berlaku satu kali.

## Cara kerja
`kode = 16 karakter pertama dari HMAC-SHA256(kunci_rahasia, nomor_menit)` (nomor_menit = detik Unix dibagi 60).
Server menerima kode menit saat ini dan satu menit sebelum/sesudahnya (toleransi selisih jam), menolak kode yang sudah dipakai,
dan mengunci percobaan selama 120 detik setelah 5 kode salah. Generator di `tools/admin_generator.html` menghitung kode yang sama di peramban.

## 1. Menyiapkan kunci rahasia
| Lingkungan | Cara |
|---|---|
| Komputer sendiri (`python main.py`) | Saat pertama dijalankan, aplikasi membuat berkas `admin_key.txt` (diabaikan Git). Salin isinya. |
| Server Render | Environment variable `UG_ADMIN_KEY` = teks acak minimal 20 karakter (jangan dipakai di proyek lain). |
| APK (GitHub Actions) | GitHub -> Settings -> Secrets and variables -> Actions -> New secret `UG_ADMIN_KEY`. Workflow menuliskannya ke `admin_key.txt` saat build. |

> Peringatan: kunci yang ikut dikemas ke APK dapat diekstrak oleh siapa pun yang memiliki APK itu. Data APK juga hanya berada di satu HP.
> Untuk administrasi sungguhan gunakan **server web**; pada APK jalur admin cocok untuk demonstrasi.

## 2. Membuat kode
- Buka `tools/admin_generator.html` di peramban (klik dua kali), tempel kunci rahasia, isi alamat aplikasi bila ingin tautan. Kode dan tautan tampil dan berganti otomatis.
- Alternatif terminal: `python tools/admin_code.py` (membaca `UG_ADMIN_KEY` atau `admin_key.txt`).

## 3. Masuk sebagai admin
- **Aplikasi / APK / web:** buka halaman Login, **ketuk judul kartu ("Login Mahasiswa") 7 kali berturut-turut**. Dialog "Akses Khusus" muncul; isi username admin (bawaan `admin`) dan kode, lalu Masuk.
- **Web dengan tautan:** buka `https://alamat-anda/ruang-admin?key=KODE` (dari tombol "Salin tautan login" di generator). Jalur tautan ini bergantung pada penanganan rute Flet dan belum diuji; jika tidak berhasil, pakai ketukan 7 kali.
- **Konsol:** `python cli.py` -> pilih `3. Login Admin (kode)`.

## 4. Keamanan
- Jangan membagikan kunci rahasia atau kode di chat/screenshot. Jika kunci pernah tersebar, ganti `UG_ADMIN_KEY` (kode lama otomatis tidak berlaku).
- Berkas `generator.html` lama yang menanam kunci langsung di dalam HTML tidak aman karena siapa pun yang memegang berkasnya memegang kuncinya. Versi baru meminta kunci diketik dan tidak menyimpannya di berkas.
  Jika kunci lama itu juga dipakai di proyek lain (mis. situs lain), ganti kunci tersebut di sana.
- Akun admin tidak dapat login dengan password, sehingga password admin tidak lagi menjadi celah.
