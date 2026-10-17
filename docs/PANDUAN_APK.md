# Panduan: Memasang UG-Stack di HP (APK) dan Hal yang Perlu Disiapkan

Ada tiga jalur. Pilih sesuai kebutuhan; jalur A paling mudah untuk tugas kuliah.

| Jalur | Hasil | Perlu dipasang di komputer | Tingkat kesulitan |
|---|---|---|---|
| A. GitHub Actions (cloud) | file `.apk` | hanya Git + akun GitHub | mudah |
| B. Build di komputer sendiri | file `.apk` | Python, Flutter 3.22, JDK 17, Android SDK | sedang |
| C. Demo lewat Wi-Fi (tanpa APK) | web di browser HP | Python | sangat mudah |

> Catatan jujur: proyek ini memakai **Flet 0.23.1** (versi lama). Alur build di bawah belum saya jalankan sendiri
> karena lingkungan saya tidak punya Android SDK. Jika ada error, salin pesan error terakhir lalu minta bantuan.

> **Penting - nama paket Android:** nilai `--project` dan `--product` tidak boleh mengandung tanda hubung atau spasi
> (contoh yang GAGAL: `--product "UG-Stack"` menghasilkan paket `id.ac.gunadarma.UG-Stack` yang tidak valid).
> Pakai huruf/angka saja, mis. `--project ugstack --product "UGStack"`.

## Jalur A - Build otomatis di GitHub (disarankan)
1. Buat repositori baru di GitHub (boleh *private*), lalu unggah isi folder proyek (`.gitignore` sudah menyingkirkan data lokal).
   ```
   git init
   git add .
   git commit -m "UG-Stack"
   git branch -M main
   git remote add origin https://github.com/USERNAME/ug-stack.git
   git push -u origin main
   ```
2. Buka repositori di browser -> tab **Actions** -> pilih **Build APK** -> **Run workflow**.
3. Tunggu sekitar 10-25 menit. Setelah hijau, buka run tersebut -> bagian **Artifacts** -> unduh `ug-stack-apk` (zip berisi `.apk`).
4. Kirim `.apk` ke HP (kabel USB, Google Drive, atau WhatsApp ke diri sendiri).
5. Di HP: buka berkas `.apk` -> izinkan **Pasang aplikasi dari sumber tidak dikenal** untuk aplikasi yang dipakai (Chrome/Files) -> **Install**.
6. Jika Play Protect memperingatkan "aplikasi tidak dikenal", itu wajar untuk APK yang tidak berasal dari Play Store (APK ditandatangani kunci debug).

Berkas workflow ada di `.github/workflows/build-apk.yml`. Jika langkah *flet build* gagal karena versi Flutter, ubah angka
`flutter-version` sesuai pesan error (Flet 0.23.x memakai Flutter 3.22).

## Jalur B - Build di komputer sendiri
Yang perlu disiapkan:
1. **Python** (3.10-3.12) dan `pip install -r requirements.txt`.
2. **Flutter SDK 3.22.x** (flutter.dev) dan jalankan `flutter doctor`.
3. **JDK 17** dan **Android SDK** (cara termudah: pasang Android Studio, lalu setujui lisensi: `flutter doctor --android-licenses`).
4. **Windows**: aktifkan *Developer Mode* (Settings -> Privacy & security -> For developers) agar symlink bisa dibuat.
5. Ruang disk bebas minimal sekitar 10 GB dan koneksi internet (build pertama mengunduh banyak komponen).

Perintah (di folder proyek):
```
flet build apk --project ugstack --product "UGStack" --org id.ac.gunadarma
```
Hasil: `build/apk/app-release.apk`. Pasang lewat USB: aktifkan *USB debugging* di HP lalu `adb install build/apk/app-release.apk`,
atau salin berkas ke HP dan buka.

Dokumentasi resmi (versi terbaru; versi 0.23 bisa berbeda): https://flet.dev/docs/publish/android

## Jalur C - Demo cepat di HP tanpa APK
Berguna untuk screenshot tampilan HP dan cek responsif.
1. Laptop dan HP terhubung ke **Wi-Fi yang sama**.
2. Jalankan server agar bisa diakses jaringan:
   - Windows PowerShell: `$env:UG_HOST="0.0.0.0"; python main.py`
   - Linux/macOS: `UG_HOST=0.0.0.0 python main.py`
3. Cari IP laptop (`ipconfig` / `ifconfig`), mis. 192.168.1.10, lalu buka `http://192.168.1.10:8550` di browser HP.
4. Jika tidak terbuka, izinkan Python di **Windows Firewall** (jaringan privat).
5. Hentikan server setelah selesai (jangan dibiarkan terbuka di Wi-Fi umum).

## Daftar periksa sebelum mengumpulkan APK
- [ ] Aplikasi terbuka di HP dan tampilan memakai menu hamburger (layar sempit).
- [ ] Login admin, **ganti password bawaan**, lalu tambah/ubah/hapus modul.
- [ ] Ganti password admin, tambah modul, **tutup aplikasi sepenuhnya** (geser dari daftar aplikasi terbuka) lalu buka lagi: password baru dan modul masih ada.
- [ ] Buka halaman Tutorial dengan internet aktif (panel konten otomatis terisi), lalu matikan internet dan buka ulang: konten dari cache tampil.
- [ ] Ambil screenshot untuk bukti pengujian (lihat tabel M-xx di laporan).
- [ ] Simpan juga keluaran `python -m unittest` dan `python run_report.py` sebagai bukti.

## Jika tampilan HP bermasalah
- Teks terpotong/tabrakan: laporkan ukuran layar dan screenshot; layout memakai `ResponsiveRow` (breakpoint 576/768/992 px).
- Konten otomatis kosong di APK: pastikan izin INTERNET (aktif secara bawaan pada build Flet) dan koneksi tersedia.
- Data hilang setelah ditutup (Flet 0.23.1 belum menyediakan `FLET_APP_STORAGE_DATA`): sejak versi 5 aplikasi memakai **penyimpanan perangkat Flet** (SharedPreferences) pada APK, sehingga data awet. Pasang ulang APK terbaru; data dari APK lama tidak terbawa.
