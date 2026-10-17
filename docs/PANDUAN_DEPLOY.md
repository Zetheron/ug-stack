# Panduan: Menayangkan UG-Stack Online (Render + Neon, dengan alamat Vercel opsional)

## Kenapa tidak bisa langsung di Vercel?
UG-Stack dibuat dengan Flet. Flet menjalankan **server yang hidup terus** dan berkomunikasi lewat **WebSocket**.
Vercel hanya menjalankan fungsi serverless singkat (tanpa WebSocket dan tanpa penyimpanan berkas permanen), sehingga aplikasi ini
tidak dapat berjalan di sana. Solusinya: server dijalankan di Render (gratis), data disimpan di Neon (PostgreSQL gratis),
dan jika Anda ingin alamat `*.vercel.app`, Vercel cukup dipakai untuk **mengalihkan** ke alamat Render.

Alur: `Pengguna -> (opsional) xxx.vercel.app -> Render (server Flet) -> Neon (data)`

## Langkah 1 - Siapkan database di Neon (sekitar 3 menit)
1. Buka Neon Console -> **New Project** (nama bebas, mis. `ug-stack`).
2. Di dashboard proyek klik **Connect**, salin **Connection string** berbentuk
   `postgresql://USER:PASSWORD@ep-xxxx.region.aws.neon.tech/neondb?sslmode=require`.
3. Simpan, jangan ditempel di GitHub atau chat. Tabel dibuat otomatis oleh aplikasi saat pertama berjalan.

## Langkah 2 - Unggah kode ke GitHub
Sudah Anda lakukan (repo `ug-stack`). Setelah mengubah kode: `git add . && git commit -m "pesan" && git push`.

## Langkah 3 - Buat layanan di Render
1. Buka render.com -> **New +** -> **Web Service** -> hubungkan akun GitHub -> pilih repo `ug-stack`.
2. **Runtime/Language: Docker** (Dockerfile sudah tersedia). Instance type: **Free**.
3. Buka **Environment** dan tambahkan:
   | Key | Isi |
   |---|---|
   | `DATABASE_URL` | connection string Neon dari Langkah 1 |
   | `UG_ADMIN_KEY` | kunci rahasia login admin (teks acak min. 20 karakter); lihat `docs/PANDUAN_ADMIN_KODE.md` |
4. Klik **Create Web Service**. Build pertama sekitar 3-6 menit. Setelah status **Live**, buka alamat `https://nama-anda.onrender.com`.
5. Login admin: buka halaman Login, ketuk judul kartu 7 kali, masukkan kode dari `tools/admin_generator.html` (kunci = `UG_ADMIN_KEY`). Panel Admin -> **Buat Akun** untuk membuat akun dosen/mahasiswa.

Catatan paket gratis Render: layanan **tidur setelah ~15 menit tanpa pengunjung**; akses pertama setelah itu butuh sekitar 30-60 detik.
Data aman karena disimpan di Neon, bukan di server Render. Buka alamat itu sebelum presentasi agar sudah "bangun".

## Langkah 4 (opsional) - Alamat Vercel yang mengalihkan ke Render
1. Salin folder `deploy/vercel-redirect` ke repositori baru (atau folder terpisah) dan ganti `GANTI-DENGAN-URL-RENDER.onrender.com` pada `vercel.json` dengan alamat Render Anda.
2. Di Vercel: **Add New -> Project** -> pilih repositori itu -> **Framework Preset: Other** -> Deploy.
3. Alamat `https://nama-proyek.vercel.app` kini mengalihkan ke aplikasi Anda.
Alamat yang tampil di browser akan berubah ke alamat Render setelah pengalihan; itu normal.

## Keamanan sebelum dibuka untuk umum
- Gunakan `UG_ADMIN_KEY` yang acak dan panjang, dan **jangan membagikan kunci atau kode admin di chat/screenshot**. Jika pernah terbagi, ganti nilainya di Render.
- Jika kampus hanya ingin akun yang dibuat dosen/admin, matikan pendaftaran mandiri: Panel Admin -> Pengguna -> saklar *Pendaftaran mandiri*.
- Render menyediakan HTTPS otomatis. Jangan menaruh `DATABASE_URL` di kode.
- Cadangkan data: Panel Admin -> Data -> **Buat backup** (disimpan di database).

## Menguji secara lokal dengan database
```
pip install -r requirements-server.txt
set DATABASE_URL=postgresql://...      (PowerShell: $env:DATABASE_URL="postgresql://...")
python main.py
```
Tanpa `DATABASE_URL`, data disimpan di berkas `data/*.json` (lokal) atau penyimpanan perangkat (APK).

## Jika deployment gagal
Salin 30 baris terakhir log Render ("Logs") dan kirim ke asisten. Kesalahan umum: `DATABASE_URL` salah ketik (cek `?sslmode=require`), atau
build kehabisan waktu pada paket gratis (coba **Manual Deploy -> Clear build cache & deploy**).
