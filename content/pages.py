"""Konten halaman statis: roadmap belajar dan halaman informasi."""

ROADMAP = [
    dict(title="Front-End Developer", icon="🎨", desc="Membangun tampilan web yang interaktif dan responsif.",
         steps=[("html", "Mulai dari struktur halaman."), ("css", "Percantik dan buat responsif."),
                ("javascript", "Tambahkan interaksi."), ("react", "Bangun UI berbasis komponen.")]),
    dict(title="Back-End Developer", icon="🛠️", desc="Membuat logika server dan menyimpan data.",
         steps=[("python", "Kuasai dasar pemrograman."), ("sql", "Kelola data dengan query."),
                ("php", "Bangun situs dinamis sisi server."), ("mysql", "Rancang basis data yang efisien.")]),
    dict(title="Software Engineer", icon="⚙️", desc="Memahami fondasi komputer dan aplikasi skala besar.",
         steps=[("c", "Pahami memori dan pointer."), ("cpp", "Tambah OOP dan STL."),
                ("java", "Bangun aplikasi berorientasi objek."), ("csharp", "Jelajahi .NET dan game Unity.")]),
    dict(title="Data dan Otomasi", icon="📊", desc="Mengolah data dan mengotomasi pekerjaan.",
         steps=[("python", "Bahasa utama untuk data dan AI."), ("sql", "Ambil dan ringkas data."),
                ("mysql", "Kelola basis data relasional.")]),
]

INFO = {
    "tentang": dict(title="Tentang UG-Stack", sections=[
        ("Apa itu UG-Stack?", "UG-Stack adalah platform belajar pemrograman berbasis Python (Flet) yang berjalan di web dan Android. Materi pelajaran, cheat sheet, dan quiz disusun sendiri, lalu diperkaya otomatis dengan konten dari sumber tepercaya."),
        ("Sumber konten otomatis", "Wikipedia (ringkasan), MDN Web Docs (referensi web), Stack Overflow (pertanyaan terpopuler), DEV Community (artikel komunitas), dan GitHub (repositori populer). Semua diambil lewat API publik, selalu menampilkan tautan ke sumber aslinya, dan di-cache 24 jam agar tetap bisa dibuka saat offline."),
        ("Lisensi konten", "Teks dari Wikipedia, MDN, dan Stack Overflow berlisensi CC BY-SA milik penulis aslinya. UG-Stack hanya menampilkan ringkasan dan tautan, bukan menyalin artikel utuh."),
    ]),
    "komunitas": dict(title="Komunitas dan Kontak", sections=[
        ("Bergabung", "Ikuti pembaruan UG-Stack, bertanya, dan berbagi proyek bersama sesama pelajar. Tautan resmi komunitas dapat ditambahkan oleh pengelola di berkas content/pages.py."),
        ("Butuh bantuan?", "Mulai dari halaman Roadmap atau Tutorial. Untuk pertanyaan spesifik, gunakan fitur Pencarian: ia menampilkan pertanyaan terkait dari Stack Overflow."),
    ]),
    "aplikasi": dict(title="Pasang Aplikasi UG-Stack", sections=[
        ("Web", "Jalankan python main.py lalu buka http://127.0.0.1:8550 di browser. Tampilan otomatis menyesuaikan lebar layar."),
        ("Android (APK)", "Pasang Flutter SDK, JDK 17, dan Android SDK, lalu jalankan flet build apk di folder proyek. Salin berkas .apk dari folder build/apk ke HP dan pasang. Rincian ada di README."),
        ("Data di aplikasi", "Pada APK, data pengguna dan cache konten disimpan di folder khusus aplikasi sehingga tetap ada setelah aplikasi ditutup."),
    ]),
    "spaces": dict(title="UG-Stack Spaces", sections=[
        ("Ruang eksperimen kode", "Gunakan Try it Editor untuk mencoba contoh kode dari setiap pelajaran. Buka pelajaran, lalu tekan tombol Try it Yourself untuk memuat kode ke editor."),
        ("Segera hadir", "Penyimpanan proyek pribadi dan berbagi tautan hasil kode."),
    ]),
}
