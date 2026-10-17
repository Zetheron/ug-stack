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
