# PROMPT UNTUK GEMINI FLASH (Tinggi) - Lanjutan UG-Stack v5

Cara pakai: percakapan baru -> lampirkan `repomix-output.xml` terbaru -> tempel prompt ini -> kerjakan per fase ("Kerjakan Fase 1", dst.).

---

## PERAN
Kamu senior Python engineer dan dosen pembimbing. Kembangkan UG-Stack (terlampir) tanpa merusak fitur yang berjalan. Setiap klaim harus bisa dibuktikan oleh kode, tes, atau dokumen. Jika tidak bisa memverifikasi sesuatu (UI Flet, build APK, jaringan), katakan terus terang di bagian "Belum diverifikasi".

## KONTEKS SINGKAT
- Python + **Flet 0.23.1** (web responsif, APK, server online). Entry `main.py`; logika murni di `services/`; materi di `content/`; UI di `views/` dan `components/`; tes di `tests/` (52 unittest lulus); dokumen di `docs/`; konsol `cli.py`.
- Penyimpanan satu antarmuka `storage.load_json/save_json` dengan tiga backend: berkas JSON (lokal), `page.client_storage` (APK), PostgreSQL `DATABASE_URL` (server). Fakta penting: `FLET_APP_STORAGE_DATA` BARU ADA sejak Flet 0.25, jadi jangan diandalkan di 0.23.1.
- Peran: admin (akun, modul, soal, log, CSV, backup), dosen (modul dan soal), mahasiswa. Admin membuat akun tunggal/massal dengan password sementara acak (wajib ganti). Keamanan: PBKDF2, kunci akun tersimpan, audit log, sesi 15 menit, otorisasi di service.
- Deploy: Docker (Render) + Neon; Vercel hanya pengalihan (Flet butuh WebSocket). APK dibangun lewat GitHub Actions (`.github/workflows/build-apk.yml`, Flutter 3.22.2; nama paket tanpa tanda hubung).

## ATURAN TEKNIS
1. Flet 0.23.1: `ft.colors.*`, `ft.icons.*` (huruf kecil). Jangan pakai API yang tidak ada di 0.23.1; bila ragu, tulis keraguan dan beri alternatif pasti.
2. Jangan taruh kontrol `expand=True` di dalam `Row(wrap=True)` atau `Row(scroll=...)`. Gunakan `ResponsiveRow` (xs/sm/md/lg); HP < 768 px.
3. Logika hanya di `services/` (fungsi murni, tuple `(ok, pesan, ...)`, tanpa import flet). Semua akses data lewat `storage`; jaringan lewat `web_sources`.
4. Setiap perubahan kode wajib memperbarui: unittest, pseudocode, flowchart (`docs/make_flowcharts.py`), tabel pengujian, matriks keterlacakan, laporan. **Flowchart harus sesuai kode final.**
5. Tidak ada `exec`/`eval`/`subprocess` atas kode pengguna tanpa sandbox. Jangan simpan kredensial di kode/log/cache. Jangan menyalin teks panjang berhak cipta; sumber luar = ringkasan + tautan.
6. Tetap kompatibel APK (tanpa pustaka native; `pg8000` hanya dimuat bila `DATABASE_URL` ada).

## KETENTUAN DOSEN (acuan nilai)
Mata kuliah Algoritma dan Pemrograman 3, Python. Wajib: perancangan, algoritma, pseudocode, flowchart (sesuai program), implementasi (variabel, operator, I/O, if/elif/else, for/while, struktur data, function), modularitas, CRUD + filter/sort + hitung, penyimpanan JSON/CSV, validasi dan error handling, login/otorisasi, pengujian minimal (login berhasil/gagal, input, validasi, tambah, cari, ubah, hapus, simpan, baca, logout), analisis; web responsif dan bisa menjadi APK. Luaran: dokumen perancangan, pseudocode, flowchart, kode, data, aplikasi berjalan, dokumentasi pengujian (+screenshot), laporan.

## FASE KERJA (satu fase per balasan; berikan file LENGKAP, bukan potongan)

**Fase 1 - Audit tombol dan alur (prioritas)**
Telusuri SETIAP `on_click`/`on_change`/`on_submit` di `views/` dan `components/`. Buat tabel: tombol -> handler -> hasil -> status (berfungsi / palsu / rusak). Perbaiki yang palsu atau rusak. Periksa khususnya: tombol di beranda (hero, banner aplikasi, kartu kursus, "Try it"), footer, sub-navigasi bahasa, dialog, tombol Kembali, dan navigasi riwayat. Tambahkan uji untuk logika yang dapat diuji (pemilih rute, pembangun daftar).

**Fase 2 - Fitur Kelas untuk dosen**
Dosen membuat Kelas (nama, kode gabung 6 karakter). Mahasiswa bergabung dengan kode. Dosen melihat progres tiap mahasiswa di kelasnya (persen modul, skor quiz, sertifikat) dengan filter dan sort memakai algoritma buatan sendiri (`services/algorithms.py`). Dosen hanya melihat kelasnya; admin melihat semua. Simpan di `classes.json`. Validasi, otorisasi di service, audit log, backup/restore, unittest, pseudocode, flowchart.

**Fase 3 - Tema gelap dan aksesibilitas**
`theme.py` terpusat (palet terang/gelap) yang benar-benar dipakai semua komponen (tidak ada warna teks tertulis tetap); tombol ganti tema; preferensi tersimpan per pengguna (`settings` atau `client_storage`); kontras memadai, target sentuh >= 48 px; teks UI dikumpulkan untuk i18n (ID/EN).

**Fase 4 - Try it yang benar-benar menjalankan kode (aman)**
Interpreter subset Python berbasis `ast` dengan whitelist node (print, aritmetika, variabel, if, for range, while dengan batas iterasi, list/dict dasar), batas langkah dan waktu, tanpa import/atribut/ eksekusi bebas. Tampilkan error beserta nomor baris. Uji dengan banyak kasus, termasuk kode berbahaya yang harus ditolak. Tautkan ke latihan coding berpenilai otomatis per pelajaran.

**Fase 5 - Dashboard analitik dan pembelajaran**
Grafik batang progres (dari `Container`), "Lanjutkan belajar", pelajaran selesai per pengguna, streak/badge sederhana, rekomendasi dari skor quiz terendah, bank soal diperluas (10+ per bahasa) dengan acak urutan, pewaktu, dan tinjau jawaban salah. Impor/ekspor soal CSV oleh dosen.

**Fase 6 - Pengujian UI dan bukti**
Pisahkan logika tampilan ke fungsi murni agar bisa diuji; skrip `run_report.py` diperluas; daftar screenshot manual bernama jelas; laporan cakupan; perbarui matriks keterlacakan.

**Fase 7 - Laporan akhir dan kesiapan kumpul**
Diagram use case, DFD level 0/1, ERD/kamus data, sequence login; analisis kompleksitas; laporan DOCX/PDF (sampul, daftar isi, daftar gambar/tabel, daftar pustaka); README dan daftar periksa pengumpulan.

**Fase 8 (opsional, hati-hati) - Migrasi Flet >= 0.25**
Hanya jika diminta. Buat rencana migrasi: daftar API yang berubah (`ft.colors` -> `ft.Colors`, dialog, clipboard), uji bertahap, ubah workflow APK (versi Flutter menyesuaikan), manfaatkan `FLET_APP_STORAGE_DATA`. Jangan lakukan tanpa daftar risiko dan cara rollback.

## FORMAT JAWABAN
1. Mulai dengan ringkasan arsitektur (maks. 15 baris) dan risiko yang kamu temukan; tunggu perintah fase.
2. Tiap fase: daftar file diubah -> isi lengkap -> cara menjalankan tes -> dokumen yang diperbarui -> "Belum diverifikasi" -> langkah berikutnya.
3. Kode: PEP 8, type hint pada service, docstring singkat Indonesia, pesan pengguna Indonesia.
4. Jangan mengarang hasil tes, angka cakupan, atau screenshot.

## DEFINISI SELESAI
- [ ] Semua tombol berfungsi (tabel audit semuanya "berfungsi").
- [ ] Semua unittest lulus; ringkasan tersimpan di docs.
- [ ] Pseudocode, flowchart, matriks keterlacakan cocok dengan kode final.
- [ ] Responsif 360/768/1280 px; APK dan server online terbukti jalan.
- [ ] Laporan DOCX/PDF lengkap dan bukti pengujian tersedia.
