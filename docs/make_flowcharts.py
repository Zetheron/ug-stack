"""Membuat flowchart (DOT -> PNG) sesuai alur kode yang diimplementasikan."""
import subprocess, textwrap, os

SHAPES = {
    "T": dict(shape="ellipse", style="filled", fillcolor="#C8E6C9"),
    "P": dict(shape="box", style="filled", fillcolor="#FFFFFF"),
    "D": dict(shape="diamond", style="filled", fillcolor="#FFF4A3"),
    "IO": dict(shape="parallelogram", style="filled", fillcolor="#E1F5FE"),
}

def render(fname, title, nodes, edges):
    lines = ['digraph G {', 'graph [rankdir=TB, labelloc=t, fontsize=20, fontname="DejaVu Sans", nodesep=0.5, ranksep=0.45, pad=0.3, label="%s"];' % title,
             'node [fontname="DejaVu Sans", fontsize=12, penwidth=1.3];', 'edge [fontname="DejaVu Sans", fontsize=11];']
    for nid, (kind, label) in nodes.items():
        w = 20 if kind == "D" else 28
        lab = "\\n".join(textwrap.wrap(label, w))
        attrs = ", ".join(f'{k}="{v}"' for k, v in SHAPES[kind].items())
        lines.append(f'{nid} [label="{lab}", {attrs}];')
    for e in edges:
        a, b = e[0], e[1]
        lab = f' [label="{e[2]}"]' if len(e) > 2 else ""
        lines.append(f"{a} -> {b}{lab};")
    lines.append("}")
    dot = fname + ".dot"
    open(dot, "w", encoding="utf-8").write("\n".join(lines))
    subprocess.run(["dot", "-Tpng", "-Gdpi=120", dot, "-o", fname + ".png"], check=True)

# 1 -------------------------------------------------------------- alur utama
render("01_alur_utama", "Flowchart 1 - Alur Utama Aplikasi UG-Stack", {
    "s": ("T", "Mulai"), "i": ("P", "Inisialisasi data: buat file JSON dan akun admin bila belum ada"),
    "h": ("IO", "Tampilkan Beranda"), "d1": ("D", "Aksi yang dipilih?"),
    "t": ("P", "Buka halaman materi: Tutorial, Referensi, Quiz, Sertifikat, Roadmap, Pencarian, Try it (konten live: Flowchart 8; quiz: Flowchart 9)"),
    "d2": ("D", "Sudah login?"), "lg": ("P", "Proses Login atau Registrasi (Flowchart 2 dan 3)"),
    "d3": ("D", "Login berhasil?"), "dash": ("IO", "Tampilkan Dashboard sesuai peran"),
    "d4": ("D", "Peran pengguna?"),
    "pa": ("P", "Admin: kelola modul - tambah, ubah, hapus, cari (Flowchart 4, 5, 6)"),
    "pm": ("P", "Mahasiswa: cari modul, tandai selesai, hitung progres (Flowchart 5, 7)"),
    "d5": ("D", "Logout?"), "lo": ("P", "Hapus sesi pengguna"), "e": ("T", "Selesai"),
}, [("s","i"),("i","h"),("h","d1"),("d1","t","Halaman materi"),("t","h"),("d1","d2","Dashboard / Login"),
    ("d2","dash","Ya"),("d2","lg","Tidak"),("lg","d3"),("d3","dash","Ya"),("d3","lg","Tidak"),
    ("dash","d4"),("d4","pa","Admin"),("d4","pm","Mahasiswa"),("pa","d5"),("pm","d5"),
    ("d5","d4","Tidak"),("d5","lo","Ya"),("lo","h"),("d1","e","Keluar")])

# 2 -------------------------------------------------------------- login
render("02_login", "Flowchart 2 - Login", {
    "s": ("T", "Mulai"), "in": ("IO", "Input username dan password"),
    "d1": ("D", "Username atau password kosong?"), "d2": ("D", "Akun sedang terkunci? (baca lockouts.json)"),
    "p1": ("P", "Baca users.json"), "d3": ("D", "File berhasil dibaca?"),
    "p2": ("P", "Cari username; hash password (salt pengguna, atau salt tiruan bila username tidak ada)"),
    "d4": ("D", "Username ada dan hash cocok?"),
    "p3": ("P", "Reset hitungan gagal; catat LOGIN_OK; simpan pengguna di sesi"),
    "o1": ("IO", "Tampilkan Login berhasil; buka Dashboard (jika password sementara: wajib ganti, Flowchart 14)"),
    "p4": ("P", "Tambah hitungan gagal"), "d5": ("D", "Hitungan gagal >= 3?"),
    "p5": ("P", "Kunci akun 30 detik (simpan ke lockouts.json)"),
    "e1": ("IO", "Tampilkan: wajib diisi"), "e2": ("IO", "Tampilkan: akun terkunci, tunggu"),
    "e3": ("IO", "Tampilkan pesan kesalahan file"),
    "e4": ("IO", "Tampilkan: akun dikunci"), "e5": ("IO", "Tampilkan: salah, sisa percobaan"),
    "x": ("T", "Selesai"),
}, [("s","in"),("in","d1"),("d1","e1","Ya"),("d1","d2","Tidak"),("d2","e2","Ya"),("d2","p1","Tidak"),
    ("p1","d3"),("d3","e3","Tidak"),("d3","p2","Ya"),("p2","d4"),("d4","p3","Ya"),("p3","o1"),
    ("d4","p4","Tidak"),("p4","d5"),("d5","p5","Ya"),("p5","e4"),("d5","e5","Tidak"),
    ("o1","x"),("e1","x"),("e2","x"),("e3","x"),("e4","x"),("e5","x")])

# 3 -------------------------------------------------------------- registrasi
render("03_registrasi", "Flowchart 3 - Registrasi Akun", {
    "s": ("T", "Mulai"), "in": ("IO", "Input username, password, konfirmasi"),
    "d1": ("D", "Username valid? (4-20 karakter huruf/angka/_)"),
    "d2": ("D", "Password valid? (min 8, huruf dan angka)"),
    "d3": ("D", "Konfirmasi sama dengan password?"),
    "p1": ("P", "Baca users.json"), "d4": ("D", "Username sudah dipakai?"),
    "p2": ("P", "Hash password dengan salt acak; tambah pengguna (peran mahasiswa)"),
    "p3": ("P", "Simpan users.json"), "d5": ("D", "Penyimpanan berhasil?"),
    "o": ("IO", "Tampilkan Registrasi berhasil; buka halaman Login"),
    "err": ("IO", "Tampilkan pesan kesalahan"), "x": ("T", "Selesai"),
}, [("s","in"),("in","d1"),("d1","err","Tidak"),("d1","d2","Ya"),("d2","err","Tidak"),("d2","d3","Ya"),
    ("d3","err","Tidak"),("d3","p1","Ya"),("p1","d4"),("d4","err","Ya"),("d4","p2","Tidak"),("p2","p3"),
    ("p3","d5"),("d5","err","Tidak"),("d5","o","Ya"),("o","x"),("err","x")])

# 4 -------------------------------------------------------------- tambah / ubah
render("04_tambah_ubah_modul", "Flowchart 4 - Tambah dan Ubah Modul (Admin)", {
    "s": ("T", "Mulai"), "d0": ("D", "Pengguna adalah admin?"),
    "in": ("IO", "Input judul, bahasa, level, durasi, deskripsi"),
    "d1": ("D", "Data valid? (judul 3-60, bahasa dan level terdaftar, durasi 1-600, deskripsi <= 200)"),
    "d2": ("D", "Mode tambah?"),
    "p1": ("P", "ID baru = ID terbesar + 1; tambahkan ke daftar modul"),
    "p2": ("P", "Cari modul berdasarkan ID"), "d3": ("D", "Modul ditemukan?"),
    "p3": ("P", "Ganti data modul dengan data baru"),
    "p4": ("P", "Simpan modules.json"), "d4": ("D", "Penyimpanan berhasil?"),
    "o": ("IO", "Tampilkan berhasil; muat ulang daftar"),
    "e0": ("IO", "Tampilkan: hanya admin"), "e1": ("IO", "Tampilkan pesan validasi"),
    "e2": ("IO", "Tampilkan: modul tidak ditemukan"), "e3": ("IO", "Tampilkan pesan kesalahan file"),
    "x": ("T", "Selesai"),
}, [("s","d0"),("d0","e0","Tidak"),("d0","in","Ya"),("in","d1"),("d1","e1","Tidak"),("d1","d2","Ya"),
    ("d2","p1","Ya"),("d2","p2","Tidak"),("p2","d3"),("d3","e2","Tidak"),("d3","p3","Ya"),
    ("p1","p4"),("p3","p4"),("p4","d4"),("d4","e3","Tidak"),("d4","o","Ya"),
    ("o","x"),("e0","x"),("e1","x"),("e2","x"),("e3","x")])

# 5 -------------------------------------------------------------- hapus
render("05_hapus_modul", "Flowchart 5 - Hapus Modul (Admin)", {
    "s": ("T", "Mulai"), "d0": ("D", "Pengguna adalah admin?"),
    "in": ("IO", "Pilih modul; dialog konfirmasi hapus"), "d1": ("D", "Admin menekan Hapus?"),
    "p1": ("P", "Baca modules.json; buang modul ber-ID tersebut"),
    "d2": ("D", "Jumlah modul berkurang?"),
    "p2": ("P", "Simpan modules.json"),
    "p3": ("P", "Hapus ID modul dari progres semua mahasiswa; simpan progress.json"),
    "o": ("IO", "Tampilkan: modul dihapus; muat ulang daftar"),
    "e0": ("IO", "Tampilkan: hanya admin"), "e1": ("IO", "Tampilkan: modul tidak ditemukan"),
    "c": ("T", "Batal"), "x": ("T", "Selesai"),
}, [("s","d0"),("d0","e0","Tidak"),("d0","in","Ya"),("in","d1"),("d1","c","Batal"),("d1","p1","Ya"),
    ("p1","d2"),("d2","e1","Tidak"),("d2","p2","Ya"),("p2","p3"),("p3","o"),("o","x"),("e0","x"),("e1","x")])

# 6 -------------------------------------------------------------- cari/filter/sort
render("06_cari_filter_sort", "Flowchart 6 - Pencarian, Filter, dan Pengurutan", {
    "s": ("T", "Mulai"), "in": ("IO", "Input kata kunci, bahasa, kunci urut, naik/turun"),
    "p0": ("P", "hasil = daftar kosong"), "d1": ("D", "Masih ada modul berikutnya?"),
    "d2": ("D", "Bahasa bukan Semua dan bahasa modul tidak sama?"),
    "d3": ("D", "Kata kunci diisi dan tidak ada di judul atau deskripsi?"),
    "p1": ("P", "Tambahkan modul ke hasil"),
    "p2": ("P", "Urutkan hasil menurut judul / durasi / level, naik atau turun"),
    "o": ("IO", "Tampilkan kartu modul dan jumlahnya"), "x": ("T", "Selesai"),
}, [("s","in"),("in","p0"),("p0","d1"),("d1","d2","Ya"),("d2","d1","Ya (lewati)"),("d2","d3","Tidak"),
    ("d3","d1","Ya (lewati)"),("d3","p1","Tidak"),("p1","d1"),("d1","p2","Tidak"),("p2","o"),("o","x")])

# 7 -------------------------------------------------------------- progres
render("07_progres_belajar", "Flowchart 7 - Tandai Selesai dan Hitung Progres", {
    "s": ("T", "Mulai"), "in": ("IO", "Mahasiswa memilih modul"), "p1": ("P", "Baca progress.json"),
    "d1": ("D", "ID modul sudah ada di daftar selesai pengguna?"),
    "p2": ("P", "Hapus ID dari daftar selesai (batal selesai)"),
    "p3": ("P", "Tambahkan ID ke daftar selesai"),
    "p4": ("P", "Simpan progress.json"), "d2": ("D", "Penyimpanan berhasil?"),
    "e": ("IO", "Tampilkan pesan kesalahan file"),
    "d3": ("D", "Jumlah modul = 0?"), "z": ("P", "persen = 0"),
    "p5": ("P", "jumlah = 0; untuk setiap ID modul: jika ada di daftar selesai maka jumlah + 1"),
    "p6": ("P", "persen = jumlah x 100 / total modul"),
    "o": ("IO", "Tampilkan progress bar dan persentase"), "x": ("T", "Selesai"),
}, [("s","in"),("in","p1"),("p1","d1"),("d1","p2","Ya"),("d1","p3","Tidak"),("p2","p4"),("p3","p4"),
    ("p4","d2"),("d2","e","Tidak"),("d2","d3","Ya"),("d3","z","Ya"),("d3","p5","Tidak"),("p5","p6"),
    ("z","o"),("p6","o"),("o","x"),("e","x")])

# 8 -------------------------------------------------------------- konten otomatis
render("08_konten_otomatis", "Flowchart 8 - Pengambilan Konten Otomatis (dengan Cache)", {
    "s": ("T", "Mulai"), "in": ("IO", "Halaman memerlukan konten dari sumber (kunci cache, fungsi pengambil)"),
    "p1": ("P", "Baca file cache berdasarkan kunci"), "d1": ("D", "Cache ada dan umurnya < 24 jam?"),
    "o1": ("IO", "Tampilkan data dari cache"),
    "p2": ("P", "Panggil API sumber tepercaya (batas waktu 6 detik) di thread terpisah"),
    "d2": ("D", "Pemanggilan berhasil?"),
    "p3": ("P", "Simpan data dan waktu ke cache"), "o2": ("IO", "Tampilkan data terbaru dari web"),
    "d3": ("D", "Ada cache lama?"), "o3": ("IO", "Tampilkan cache lama (mode offline)"),
    "o4": ("IO", "Tampilkan pesan: tidak dapat memuat, periksa koneksi"), "x": ("T", "Selesai"),
}, [("s","in"),("in","p1"),("p1","d1"),("d1","o1","Ya"),("d1","p2","Tidak"),("p2","d2"),("d2","p3","Ya"),
    ("p3","o2"),("d2","d3","Tidak"),("d3","o3","Ya"),("d3","o4","Tidak"),
    ("o1","x"),("o2","x"),("o3","x"),("o4","x")])

# 9 -------------------------------------------------------------- quiz + sertifikat
render("09_quiz_sertifikat", "Flowchart 9 - Quiz dan Sertifikat", {
    "s": ("T", "Mulai"), "in": ("IO", "Pengguna memilih satu jawaban untuk tiap soal"),
    "d1": ("D", "Ada soal yang belum dijawab?"), "e": ("IO", "Tampilkan: jawab semua soal"),
    "p1": ("P", "benar = 0; untuk setiap soal: jika jawaban = kunci maka benar + 1"),
    "p2": ("P", "persen = benar x 100 / jumlah soal; lulus = persen >= 70"),
    "d3": ("D", "Pengguna sudah login?"),
    "p3": ("P", "Simpan skor terbaik (maks) dan tambah jumlah percobaan"),
    "d4": ("D", "Lulus dan belum punya tanggal lulus?"), "p4": ("P", "Catat tanggal lulus"),
    "d5": ("D", "Lulus?"),
    "o1": ("IO", "Tampilkan nilai, penjelasan, dan tombol sertifikat (kode = SHA-256 (pengguna, bahasa, tanggal), 10 karakter)"),
    "o2": ("IO", "Tampilkan nilai dan penjelasan; sarankan belajar ulang"),
    "o3": ("IO", "Tampilkan nilai dan ajakan login untuk menyimpan skor"), "x": ("T", "Selesai"),
}, [("s","in"),("in","d1"),("d1","e","Ya"),("d1","p1","Tidak"),("p1","p2"),("p2","d3"),("d3","o3","Tidak"),
    ("d3","p3","Ya"),("p3","d4"),("d4","p4","Ya"),("d4","d5","Tidak"),("p4","d5"),("d5","o1","Ya"),("d5","o2","Tidak"),
    ("e","x"),("o1","x"),("o2","x"),("o3","x")])

# 10 ------------------------------------------------------------- pencarian biner
render("10_pencarian_biner", "Flowchart 10 - Pencarian Biner (get_module)", {
    "s": ("T", "Mulai"), "in": ("IO", "Daftar modul terurut menurut ID, ID yang dicari"),
    "p1": ("P", "rendah = 0; tinggi = jumlah modul - 1"),
    "d1": ("D", "rendah <= tinggi? (while)"), "p2": ("P", "tengah = (rendah + tinggi) div 2"),
    "d2": ("D", "ID di tengah = ID dicari?"), "o1": ("IO", "Kembalikan modul pada indeks tengah"),
    "d3": ("D", "ID di tengah < ID dicari?"), "p3": ("P", "rendah = tengah + 1"), "p4": ("P", "tinggi = tengah - 1"),
    "d4": ("D", "Tidak ketemu: coba pencarian linear (jaga-jaga)?"),
    "o2": ("IO", "Kembalikan hasil linear atau 'tidak ditemukan'"), "x": ("T", "Selesai"),
}, [("s","in"),("in","p1"),("p1","d1"),("d1","p2","Ya"),("p2","d2"),("d2","o1","Ya"),("d2","d3","Tidak"),
    ("d3","p3","Ya"),("d3","p4","Tidak"),("p3","d1"),("p4","d1"),("d1","d4","Tidak"),("d4","o2","Ya"),
    ("o1","x"),("o2","x")])

# 11 ------------------------------------------------------------- merge sort
render("11_merge_sort", "Flowchart 11 - Merge Sort (urut stabil)", {
    "s": ("T", "Mulai"), "in": ("IO", "Daftar data, fungsi kunci, arah urut"),
    "d1": ("D", "Jumlah data <= 1?"), "o1": ("IO", "Kembalikan salinan data"),
    "p1": ("P", "Bagi dua: kiri dan kanan; urutkan masing-masing secara rekursif"),
    "p2": ("P", "i = 0; j = 0; hasil = daftar kosong"),
    "d2": ("D", "i < panjang kiri DAN j < panjang kanan? (while)"),
    "d3": ("D", "Kiri harus lebih dulu? (kunci kiri <= kanan; menurun: >=)"),
    "p3": ("P", "Tambahkan kiri[i] ke hasil; i + 1"), "p4": ("P", "Tambahkan kanan[j] ke hasil; j + 1"),
    "p5": ("P", "Tambahkan sisa kiri dan sisa kanan ke hasil"), "o2": ("IO", "Kembalikan hasil terurut"), "x": ("T", "Selesai"),
}, [("s","in"),("in","d1"),("d1","o1","Ya"),("d1","p1","Tidak"),("p1","p2"),("p2","d2"),("d2","d3","Ya"),
    ("d3","p3","Ya"),("d3","p4","Tidak"),("p3","d2"),("p4","d2"),("d2","p5","Tidak"),("p5","o2"),("o1","x"),("o2","x")])

# 12 ------------------------------------------------------------- menu konsol
render("12_menu_konsol", "Flowchart 12 - Menu Aplikasi Konsol (cli.py)", {
    "s": ("T", "Mulai"), "p0": ("P", "Inisialisasi data (auth.init_data)"),
    "m": ("IO", "Tampilkan menu awal: 1 Login, 2 Daftar, 0 Keluar"), "d1": ("D", "Pilihan?"),
    "l": ("P", "Login maksimal 3 kali (while): auth.login"), "d2": ("D", "Login berhasil?"),
    "g": ("P", "Jika password sementara: wajib ganti (Flowchart 14)"),
    "m2": ("IO", "Tampilkan menu sesuai peran (admin / mahasiswa)"), "d3": ("D", "Pilihan menu?"),
    "a": ("P", "Jalankan aksi: tampil, cari, tambah, ubah, hapus, ekspor, log, progres, ganti password"),
    "lo": ("P", "Logout: catat audit LOGOUT"), "r": ("P", "Proses registrasi (Flowchart 3)"),
    "e": ("T", "Selesai"),
}, [("s","p0"),("p0","m"),("m","d1"),("d1","l","1"),("d1","r","2"),("r","m"),("d1","e","0"),("l","d2"),
    ("d2","m","Tidak"),("d2","g","Ya"),("g","m2"),("m2","d3"),("d3","a","1-8"),("a","m2"),("d3","lo","9"),
    ("lo","m"),("d3","e","0")])

# 13 ------------------------------------------------------------- impor CSV
render("13_impor_csv", "Flowchart 13 - Impor Modul dari CSV", {
    "s": ("T", "Mulai"), "in": ("IO", "Admin menempel teks CSV"), "d0": ("D", "Pengguna admin?"),
    "d1": ("D", "Teks kosong atau > 200.000 karakter?"), "d2": ("D", "Kolom wajib (judul, bahasa, level, durasi) lengkap?"),
    "p1": ("P", "Baca modul saat ini; siapkan ID berikutnya"),
    "d3": ("D", "Masih ada baris berikutnya? (for)"), "d4": ("D", "Baris valid? (validate_module)"),
    "d5": ("D", "Judul dan bahasa sudah ada?"), "p2": ("P", "Tambahkan modul dengan ID baru; jumlah ditambah + 1"),
    "p3": ("P", "Catat baris dilewati beserta alasan"),
    "p4": ("P", "Simpan modules.json sekali; catat audit IMPOR_CSV"),
    "o": ("IO", "Tampilkan ringkasan: ditambah dan dilewati (nomor baris + alasan)"),
    "e": ("IO", "Tampilkan pesan kesalahan"), "x": ("T", "Selesai"),
}, [("s","in"),("in","d0"),("d0","e","Tidak"),("d0","d1","Ya"),("d1","e","Ya"),("d1","d2","Tidak"),("d2","e","Tidak"),
    ("d2","p1","Ya"),("p1","d3"),("d3","d4","Ya"),("d4","p3","Tidak"),("d4","d5","Ya"),("d5","p3","Ya"),("d5","p2","Tidak"),
    ("p2","d3"),("p3","d3"),("d3","p4","Tidak"),("p4","o"),("o","x"),("e","x")])

# 14 ------------------------------------------------------------- ganti password
render("14_ganti_password", "Flowchart 14 - Ganti Password (termasuk wajib ganti)", {
    "s": ("T", "Mulai"), "d0": ("D", "Login membawa tanda password sementara/bawaan?"),
    "w": ("IO", "Tampilkan dialog wajib ganti (tidak bisa ditutup)"), "in": ("IO", "Input password lama, baru, ulangi baru"),
    "d1": ("D", "Password baru valid? (min 8, huruf dan angka)"), "d2": ("D", "Konfirmasi sama?"),
    "d3": ("D", "Password lama benar?"), "d4": ("D", "Password baru berbeda dari lama?"),
    "p1": ("P", "Buat salt baru; hash password baru; hapus tanda wajib ganti; simpan; catat GANTI_PASSWORD"),
    "o": ("IO", "Tampilkan: password berhasil diubah"), "e": ("IO", "Tampilkan pesan kesalahan (dialog tetap terbuka)"),
    "x": ("T", "Selesai"),
}, [("s","d0"),("d0","w","Ya"),("d0","in","Tidak (ganti manual)"),("w","in"),("in","d1"),("d1","e","Tidak"),("d1","d2","Ya"),
    ("d2","e","Tidak"),("d2","d3","Ya"),("d3","e","Tidak"),("d3","d4","Ya"),("d4","e","Tidak"),("d4","p1","Ya"),
    ("p1","o"),("o","x"),("e","in")])

# 15 ------------------------------------------------------------- admin membuat akun
render("15_buat_akun_admin", "Flowchart 15 - Admin Membuat Akun (Mahasiswa / Dosen / Admin)", {
    "s": ("T", "Mulai"), "in": ("IO", "Input username, peran, password sementara (boleh kosong)"),
    "d0": ("D", "Pengguna adalah admin?"), "d1": ("D", "Peran valid? (admin, dosen, mahasiswa)"),
    "d2": ("D", "Username valid? (4-20 huruf/angka/_)"), "d3": ("D", "Password sementara kosong?"),
    "p1": ("P", "Buat password acak 12 karakter (huruf besar, kecil, angka)"),
    "d4": ("D", "Password valid? (min 8, huruf dan angka)"), "p2": ("P", "Baca users.json"),
    "d5": ("D", "Username sudah dipakai?"),
    "p3": ("P", "Hash password dengan salt acak; simpan akun dengan tanda wajib ganti; catat BUAT_AKUN"),
    "o": ("IO", "Tampilkan password sementara untuk diberikan ke pengguna (tombol salin)"),
    "e": ("IO", "Tampilkan pesan kesalahan"), "x": ("T", "Selesai"),
}, [("s","in"),("in","d0"),("d0","e","Tidak"),("d0","d1","Ya"),("d1","e","Tidak"),("d1","d2","Ya"),("d2","e","Tidak"),
    ("d2","d3","Ya"),("d3","p1","Ya"),("d3","d4","Tidak"),("p1","d4"),("d4","e","Tidak"),("d4","p2","Ya"),("p2","d5"),
    ("d5","e","Ya"),("d5","p3","Tidak"),("p3","o"),("o","x"),("e","x")])

# 16 ------------------------------------------------------------- pemilihan penyimpanan
render("16_pemilihan_penyimpanan", "Flowchart 16 - Pemilihan Penyimpanan dan Pembacaan Data", {
    "s": ("T", "Mulai (aplikasi dibuka)"), "d1": ("D", "Variabel DATABASE_URL ada?"),
    "pg": ("P", "Pakai backend PostgreSQL (server online, data di Neon)"),
    "d2": ("D", "Berjalan sebagai aplikasi Android/iOS (bukan web)?"),
    "cs": ("P", "Pakai backend penyimpanan perangkat (SharedPreferences) agar data awet"),
    "fb": ("P", "Pakai backend berkas JSON (folder data)"),
    "p1": ("P", "load_json(nama, bawaan): baca teks dari backend"), "d3": ("D", "Data ada?"),
    "p2": ("P", "Simpan data bawaan"), "d4": ("D", "Isi data berupa JSON valid?"),
    "p3": ("P", "Simpan salinan nama.corrupt; simpan data bawaan"), "o": ("IO", "Kembalikan data ke program"),
    "x": ("T", "Selesai"),
}, [("s","d1"),("d1","pg","Ya"),("d1","d2","Tidak"),("d2","cs","Ya"),("d2","fb","Tidak"),("pg","p1"),("cs","p1"),("fb","p1"),
    ("p1","d3"),("d3","p2","Tidak"),("d3","d4","Ya"),("p2","o"),("d4","o","Ya"),("d4","p3","Tidak"),("p3","o"),("o","x")])

# 17 ------------------------------------------------------------- login berdasarkan peran
render("17_login_peran", "Flowchart 17 - Login dengan Pilihan Peran (Mahasiswa / Dosen / Admin)", {
    "s": ("T", "Mulai (halaman login)"), "r": ("IO", "Pilih peran: Mahasiswa (NPM/username), Dosen (username/NIDN), atau Admin"),
    "d0": ("D", "Peran mahasiswa?"), "reg": ("P", "Tampilkan tautan Daftar (jika pendaftaran mandiri dibuka)"),
    "nr": ("P", "Dosen/Admin: tanpa pendaftaran mandiri; akun dibuat admin"),
    "in": ("IO", "Input NPM/username dan password"), "a": ("P", "auth.login(username, password, peran_dipilih) - Flowchart 2"),
    "d1": ("D", "Username dan password benar?"), "e1": ("IO", "Tampilkan pesan gagal (hitung percobaan, kunci akun)"),
    "d2": ("D", "Peran akun sama dengan peran yang dipilih?"),
    "e2": ("IO", "Tampilkan: akun terdaftar sebagai peran lain; catat LOGIN_PERAN_SALAH (bukan percobaan gagal)"),
    "d3": ("D", "Wajib ganti password?"), "w": ("IO", "Tampilkan dialog wajib ganti password (Flowchart 14)"),
    "o": ("IO", "Buka Dashboard sesuai peran"), "x": ("T", "Selesai"),
}, [("s","r"),("r","d0"),("d0","reg","Ya"),("d0","nr","Tidak"),("reg","in"),("nr","in"),("in","a"),("a","d1"),("d1","e1","Tidak"),
    ("d1","d2","Ya"),("d2","e2","Tidak"),("d2","d3","Ya"),("d3","w","Ya"),("d3","o","Tidak"),("w","o"),("o","x"),("e1","x"),("e2","x")])

# 18 ------------------------------------------------------------- tema dan bahasa
render("18_tema_bahasa", "Flowchart 18 - Tema Gelap/Terang dan Bahasa Indonesia/Inggris", {
    "s": ("T", "Mulai (aplikasi dibuka)"), "p1": ("P", "Baca preferensi tema dan bahasa dari penyimpanan perangkat"),
    "d1": ("D", "Tema pernah dipilih?"), "p2": ("P", "Ikuti tema perangkat (terang/gelap)"), "p3": ("P", "Pakai tema tersimpan"),
    "p4": ("P", "Bahasa = tersimpan atau Indonesia (bawaan)"), "r": ("P", "Bangun tampilan; terjemahkan seluruh pohon kontrol sebelum ditampilkan"),
    "t": ("IO", "Tampilkan halaman"), "d2": ("D", "Pengguna menekan tombol tema atau bahasa?"),
    "a": ("P", "Balik tema (terang/gelap) atau bahasa (ID/EN); simpan preferensi ke perangkat"), "x": ("T", "Selesai"),
}, [("s","p1"),("p1","d1"),("d1","p3","Ya"),("d1","p2","Tidak"),("p2","p4"),("p3","p4"),("p4","r"),("r","t"),("t","d2"),
    ("d2","a","Ya"),("a","r"),("d2","x","Tidak")])

# 19 ------------------------------------------------------------- login admin dengan kode
render("19_login_admin_kode", "Flowchart 19 - Login Admin dengan Kode Berputar 60 Detik", {
    "s": ("T", "Mulai (halaman login)"), "t": ("P", "Ketuk judul kartu 7 kali (atau buka tautan ?key=KODE); tidak ada tombol admin"),
    "in": ("IO", "Input username admin dan kode 16 karakter"), "d0": ("D", "Kunci admin terkonfigurasi?"),
    "d1": ("D", "Sedang terkunci? (5 kode salah -> 120 detik)"), "p1": ("P", "Ambil kode (dari URL bila ada) dan ubah ke huruf kecil"),
    "d2": ("D", "16 hex dan sama dengan HMAC-SHA256(kunci, menit) untuk menit -1, 0, atau +1?"),
    "p2": ("P", "Hitung percobaan gagal; kunci 120 detik bila 5; catat ADMIN_KODE_GAGAL"),
    "d3": ("D", "Kode sudah pernah dipakai?"), "p3": ("P", "Simpan kode sebagai terpakai (sekali pakai); hapus catatan gagal"),
    "d4": ("D", "Akun admin dengan username itu ada?"), "o": ("IO", "Catat LOGIN_ADMIN_KODE; buka Panel Admin"),
    "e": ("IO", "Tampilkan pesan kesalahan"), "x": ("T", "Selesai"),
}, [("s","t"),("t","in"),("in","d0"),("d0","e","Tidak"),("d0","d1","Ya"),("d1","e","Ya"),("d1","p1","Tidak"),("p1","d2"),
    ("d2","p2","Tidak"),("p2","e"),("d2","d3","Ya"),("d3","e","Ya"),("d3","p3","Tidak"),("p3","d4"),("d4","e","Tidak"),
    ("d4","o","Ya"),("o","x"),("e","x")])

# 20 ------------------------------------------------------------- laporan mahasiswa
render("20_laporan_mahasiswa", "Flowchart 20 - Laporan Mahasiswa untuk Dosen dan Admin", {
    "s": ("T", "Mulai"), "in": ("IO", "Input kata kunci nama, kunci urut, naik/turun"), "d0": ("D", "Pengguna admin atau dosen?"),
    "e": ("IO", "Kembalikan daftar kosong"), "p1": ("P", "Baca users, progres, skor, langganan; daftar modul"),
    "p2": ("P", "baris = daftar kosong; i = 0"), "d1": ("D", "Masih ada pengguna berikutnya? (while)"),
    "d2": ("D", "Peran mahasiswa dan nama cocok kata kunci?"),
    "p3": ("P", "Hitung persen modul selesai, jumlah sertifikat, rata-rata skor terbaik; tambahkan ke baris"),
    "p4": ("P", "Urutkan baris dengan merge sort buatan sendiri menurut kunci dan arah"),
    "o": ("IO", "Tampilkan kartu mahasiswa (progres, sertifikat, skor, paket, kursus)"), "x": ("T", "Selesai"),
}, [("s","in"),("in","d0"),("d0","e","Tidak"),("d0","p1","Ya"),("p1","p2"),("p2","d1"),("d1","d2","Ya"),("d2","p3","Ya"),
    ("d2","d1","Tidak"),("p3","d1"),("d1","p4","Tidak"),("p4","o"),("o","x"),("e","x")])
print("selesai")
