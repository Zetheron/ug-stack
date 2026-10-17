"""Bank soal quiz (pilihan ganda). Tiap soal: pertanyaan, 4 opsi, indeks jawaban benar, penjelasan."""

PASS_PERCENT = 70


def Q(q, options, answer, explain):
    return {"q": q, "options": options, "answer": answer, "explain": explain}


QUIZZES = {
"html": [
 Q("Singkatan HTML adalah...", ["HyperText Markup Language", "High Tech Modern Language", "Hyperlink Text Mode Logic", "Home Tool Markup Language"], 0, "HTML = HyperText Markup Language."),
 Q("Tag yang benar untuk judul terbesar?", ["<head>", "<h1>", "<title>", "<big>"], 1, "<h1> adalah judul tingkat tertinggi."),
 Q("Atribut yang memberi teks alternatif pada gambar?", ["title", "src", "alt", "href"], 2, "alt dibaca pembaca layar dan tampil bila gambar gagal dimuat."),
 Q("Elemen untuk daftar bernomor?", ["<ul>", "<ol>", "<li>", "<dl>"], 1, "<ol> = ordered list; <ul> berpoin."),
],
"css": [
 Q("CSS dipakai untuk...", ["Mengatur tampilan halaman", "Menyimpan data", "Membuat basis data", "Menjalankan server"], 0, "CSS mengatur tampilan elemen HTML."),
 Q("Selector untuk kelas bernama kartu?", ["#kartu", ".kartu", "kartu", "*kartu"], 1, "Kelas memakai titik, id memakai #."),
 Q("Properti untuk ruang DI DALAM border elemen?", ["margin", "padding", "gap", "outline"], 1, "padding = ruang dalam; margin = ruang luar."),
 Q("Nilai display untuk tata letak fleksibel?", ["block", "inline", "flex", "static"], 2, "display: flex mengaktifkan Flexbox."),
],
"javascript": [
 Q("Kata kunci untuk konstanta yang tak boleh ditetapkan ulang?", ["var", "let", "const", "static"], 2, "const mencegah penetapan ulang variabel."),
 Q("Hasil dari typeof \"halo\"?", ["text", "string", "char", "object"], 1, "typeof \"halo\" menghasilkan \"string\"."),
 Q("Metode array untuk menyaring elemen?", ["map", "filter", "push", "join"], 1, "filter mengembalikan elemen yang memenuhi syarat."),
 Q("Cara memilih elemen dengan id=\"judul\"?", ["document.querySelector(\"#judul\")", "document.get(\"judul\")", "page.select(\"judul\")", "html.find(\".judul\")"], 0, "querySelector memakai selector CSS; id diawali #."),
],
"python": [
 Q("Output dari print(2 ** 3)?", ["6", "8", "9", "23"], 1, "** adalah operator pangkat: 2 pangkat 3 = 8."),
 Q("Struktur data pasangan kunci-nilai?", ["list", "tuple", "dict", "set"], 2, "dict menyimpan pasangan kunci dan nilai."),
 Q("Kata kunci untuk mendefinisikan function?", ["func", "def", "function", "lambda saja"], 1, "Function dibuat dengan def."),
 Q("Hasil len([1, 2, 3, 4])?", ["3", "4", "5", "Error"], 1, "len menghitung jumlah elemen: 4."),
],
"sql": [
 Q("Perintah untuk membaca data?", ["GET", "SELECT", "READ", "OPEN"], 1, "SELECT memilih data dari tabel."),
 Q("Klausa untuk menyaring baris?", ["FILTER", "HAVING saja", "WHERE", "ORDER BY"], 2, "WHERE menyaring baris sebelum dikelompokkan."),
 Q("Mengurutkan dari terbesar ke terkecil?", ["ORDER BY kolom DESC", "SORT kolom DOWN", "ORDER kolom MAX", "GROUP BY kolom DESC"], 0, "DESC = descending (menurun)."),
 Q("JOIN digunakan untuk...", ["Menghapus tabel", "Menggabungkan baris dari dua tabel", "Membuat index", "Menyalin database"], 1, "JOIN menggabungkan tabel berdasarkan kolom yang berhubungan."),
],
"java": [
 Q("Titik masuk program Java?", ["start()", "run()", "main()", "init()"], 2, "Eksekusi dimulai dari public static void main."),
 Q("Tipe data untuk teks?", ["char[] saja", "String", "text", "Str"], 1, "String adalah kelas untuk teks."),
 Q("Kata kunci untuk membuat objek?", ["make", "create", "new", "object"], 2, "new Kelas() membuat objek."),
 Q("Java dijalankan di...", ["JVM", "CLR", "Interpreter Python", "Browser"], 0, "Bytecode Java dijalankan oleh Java Virtual Machine."),
],
"php": [
 Q("Variabel PHP diawali dengan...", ["#", "$", "@", "&"], 1, "Contoh: $nama."),
 Q("Perintah untuk menampilkan teks?", ["echo", "show", "display", "write"], 0, "echo menampilkan keluaran."),
 Q("Variabel superglobal data formulir method POST?", ["$_FORM", "$_GET", "$_POST", "$_DATA"], 2, "$_POST berisi data formulir POST."),
 Q("Fungsi untuk mencegah XSS saat menampilkan input?", ["strip()", "htmlspecialchars()", "clean()", "escape_all()"], 1, "htmlspecialchars mengubah karakter HTML khusus."),
],
"c": [
 Q("Fungsi untuk mencetak ke layar di C?", ["print()", "cout", "printf()", "echo"], 2, "printf dari stdio.h."),
 Q("Format printf untuk bilangan bulat?", ["%f", "%d", "%s", "%c"], 1, "%d = int; %f = float; %s = string; %c = char."),
 Q("Operator untuk mengambil alamat variabel?", ["*", "&", "#", "@"], 1, "& mengambil alamat; * mengakses nilai pointer."),
 Q("Indeks pertama sebuah array di C?", ["0", "1", "-1", "Tergantung"], 0, "Indeks array dimulai dari 0."),
],
"cpp": [
 Q("Objek keluaran standar di C++?", ["printf", "cout", "echo", "System.out"], 1, "cout dari <iostream>."),
 Q("Array dinamis di STL?", ["vector", "stack saja", "map", "pair"], 0, "std::vector ukurannya bisa berubah."),
 Q("Fungsi STL untuk mengurutkan?", ["order()", "sort()", "arrange()", "rank()"], 1, "sort(begin, end) dari <algorithm>."),
 Q("Modifier agar anggota hanya bisa diakses di dalam kelas?", ["public", "private", "static", "const"], 1, "private membatasi akses ke dalam kelas."),
],
"csharp": [
 Q("Perintah mencetak teks ke konsol?", ["print()", "Console.WriteLine()", "echo", "System.out.println()"], 1, "Console.WriteLine dari namespace System."),
 Q("Untuk apa var di C#?", ["Tipe dinamis", "Inferensi tipe saat kompilasi", "Variabel global", "Konstanta"], 1, "var membuat kompilator menyimpulkan tipe; tetap bertipe statis."),
 Q("LINQ digunakan untuk...", ["Menggambar UI", "Mengolah dan menyaring koleksi", "Menjalankan SQL server", "Membuat kelas"], 1, "LINQ = Language Integrated Query."),
 Q("Sintaks properti otomatis?", ["{ get; set; }", "<get,set>", "(get)(set)", "[get set]"], 0, "Contoh: public string Nama { get; set; }."),
],
"react": [
 Q("Komponen React harus diawali huruf...", ["Kapital", "Kecil", "Angka", "Garis bawah"], 0, "Huruf kapital membedakannya dari tag HTML biasa."),
 Q("Hook untuk menyimpan state lokal?", ["useEffect", "useState", "useRef", "useMemo"], 1, "useState mengembalikan [nilai, fungsiUbah]."),
 Q("Data yang dikirim dari induk ke anak disebut...", ["state", "props", "hook", "ref"], 1, "Props bersifat hanya-baca."),
 Q("Properti wajib saat merender daftar dengan map?", ["id", "key", "index", "name"], 1, "key membantu React melacak item daftar."),
],
"mysql": [
 Q("Perintah membuat tabel baru?", ["NEW TABLE", "MAKE TABLE", "CREATE TABLE", "ADD TABLE"], 2, "CREATE TABLE nama (...)."),
 Q("Atribut nilai otomatis bertambah?", ["AUTO_INCREMENT", "AUTO_NUMBER", "SERIAL_ID", "INCREMENT"], 0, "AUTO_INCREMENT umum dipakai pada primary key."),
 Q("Fungsi agregat untuk menghitung jumlah baris?", ["SUM", "COUNT", "TOTAL", "LEN"], 1, "COUNT(*) menghitung baris."),
 Q("Untuk melihat rencana eksekusi query?", ["SHOW PLAN", "EXPLAIN", "ANALYZE ALL", "DEBUG"], 1, "EXPLAIN SELECT ... menampilkan rencana eksekusi."),
],
}


# ---------------------------------------------------------------- soal tambahan (total 8 per bahasa)
QUIZZES["html"].extend([
 Q("Elemen yang dipakai untuk membuat tautan?", ["<link>", "<a>", "<href>", "<url>"], 1, "<a> dengan atribut href membuat tautan."),
 Q("Tag penutup yang benar untuk paragraf?", ["</p>", "<p/>", "</paragraph>", "<end p>"], 0, "Setiap <p> ditutup dengan </p>."),
 Q("Atribut agar kolom formulir wajib diisi?", ["mandatory", "required", "needed", "must"], 1, "Atribut required membuat browser memvalidasi kolom."),
 Q("Elemen semantik untuk navigasi utama?", ["<nav>", "<menu-div>", "<top>", "<links>"], 0, "<nav> menandai kelompok tautan navigasi."),
])
QUIZZES["css"].extend([
 Q("Properti untuk mengubah warna teks?", ["font-color", "text-color", "color", "foreground"], 2, "Properti color mengatur warna teks."),
 Q("Satuan yang relatif terhadap lebar layar?", ["px", "vw", "pt", "cm"], 1, "vw = 1% dari lebar viewport."),
 Q("Pengaturan flex untuk memusatkan item pada sumbu utama?", ["justify-content: center", "align-text: center", "flex-center: true", "margin: flex"], 0, "justify-content mengatur perataan pada sumbu utama."),
 Q("Selector yang berlaku saat kursor berada di atas tombol?", ["button:active", "button:hover", "button:focus-only", "button:over"], 1, ":hover berlaku saat kursor berada di atas elemen."),
])
QUIZZES["javascript"].extend([
 Q("Hasil dari 2 + \"2\" di JavaScript?", ["4", "\"22\"", "22 (angka)", "Error"], 1, "Operator + menggabungkan string, jadi hasilnya \"22\"."),
 Q("Cara mengubah teks sebuah elemen?", ["el.textContent = \"Halo\"", "el.text(\"Halo\")", "el.write(\"Halo\")", "el.set(\"Halo\")"], 0, "textContent mengubah teks elemen."),
 Q("Metode array untuk menambah elemen di akhir?", ["push", "append", "add", "insertEnd"], 0, "push menambahkan elemen di akhir array."),
 Q("Operator yang membandingkan nilai dan tipe?", ["==", "=", "===", "!="], 2, "=== membandingkan nilai sekaligus tipe."),
])
QUIZZES["python"].extend([
 Q("Cara menulis komentar satu baris di Python?", ["// komentar", "# komentar", "-- komentar", "/* komentar */"], 1, "Komentar diawali tanda #."),
 Q("Hasil dari 7 // 2?", ["3.5", "3", "4", "2"], 1, "// adalah pembagian bulat: 7 // 2 = 3."),
 Q("Kata kunci untuk menangani kesalahan?", ["catch", "except", "error", "handle"], 1, "try ... except menangkap kesalahan."),
 Q("Tipe data yang tidak bisa diubah (immutable)?", ["list", "dict", "tuple", "set"], 2, "tuple tidak bisa diubah setelah dibuat."),
])
QUIZZES["sql"].extend([
 Q("Fungsi agregat untuk rata-rata?", ["MEAN", "AVG", "AVERAGE", "MID"], 1, "AVG menghitung rata-rata."),
 Q("Klausa untuk mengelompokkan baris?", ["GROUP BY", "SORT BY", "COLLECT", "CLUSTER"], 0, "GROUP BY mengelompokkan baris."),
 Q("Perintah untuk menghapus baris tertentu?", ["REMOVE", "DELETE", "DROP ROW", "CUT"], 1, "DELETE FROM ... WHERE menghapus baris."),
 Q("Kunci yang menghubungkan dua tabel?", ["Primary key", "Foreign key", "Unique index", "Check key"], 1, "Foreign key merujuk primary key tabel lain."),
])
QUIZZES["java"].extend([
 Q("Tipe data untuk bilangan desimal?", ["int", "double", "char", "boolean"], 1, "double menyimpan bilangan desimal."),
 Q("Koleksi dengan ukuran dinamis?", ["int[]", "ArrayList", "char", "Math"], 1, "ArrayList ukurannya dapat berubah."),
 Q("Kata kunci untuk pewarisan?", ["implements", "extends", "inherits", "super only"], 1, "extends membuat kelas turunan."),
 Q("Method yang berjalan otomatis saat objek dibuat?", ["Destruktor", "Konstruktor", "main", "finalize"], 1, "Konstruktor menginisialisasi objek baru."),
])
QUIZZES["php"].extend([
 Q("Operator penggabung string di PHP?", ["+", ".", "&", "||"], 1, "Titik (.) menggabungkan string."),
 Q("Fungsi untuk menghitung jumlah elemen array?", ["length()", "count()", "size()", "sizeof only"], 1, "count() menghitung elemen array."),
 Q("Superglobal untuk data dari URL?", ["$_POST", "$_GET", "$_URL", "$_QUERY"], 1, "$_GET berisi parameter URL."),
 Q("Cara menyertakan berkas lain?", ["include", "import", "using", "load"], 0, "include menyertakan berkas PHP lain."),
])
QUIZZES["c"].extend([
 Q("Tipe data untuk karakter tunggal?", ["char", "string", "text", "byte only"], 0, "char menyimpan satu karakter."),
 Q("Fungsi untuk alokasi memori dinamis?", ["new", "malloc", "alloc()", "create"], 1, "malloc mengalokasikan memori di heap."),
 Q("Hasil dari 10 % 3?", ["3", "1", "0", "3.33"], 1, "% adalah sisa pembagian: 10 % 3 = 1."),
 Q("Penanda akhir string di C?", ["\\n", "\\0", "EOF", "NULL string"], 1, "String berakhir dengan karakter null '\\0'."),
])
QUIZZES["cpp"].extend([
 Q("Operator untuk membuat objek di heap?", ["malloc", "new", "create", "alloc"], 1, "new mengalokasikan objek dinamis."),
 Q("Simbol untuk mendeklarasikan referensi (alias) variabel?", ["&", "*", "#", "@"], 0, "int &r = x; membuat referensi (alias)."),
 Q("Container yang menyimpan pasangan kunci-nilai?", ["vector", "map", "stack", "array"], 1, "std::map menyimpan pasangan kunci-nilai."),
 Q("Penulisan pewarisan publik?", ["class B : public A", "class B extends A", "class B inherits A", "class B -> A"], 0, "Pewarisan memakai titik dua dan penentu akses."),
])
QUIZZES["csharp"].extend([
 Q("Cara membuat daftar string?", ["List<string>", "string[] only", "ListString", "Array.new"], 0, "List<T> adalah daftar generik."),
 Q("Kata kunci untuk konstanta?", ["final", "const", "static only", "readonly-const"], 1, "const mendeklarasikan konstanta."),
 Q("Operator ?. dipakai untuk...", ["Pengecekan null yang aman", "Perulangan", "Pembagian", "Perbandingan string"], 0, "Null-conditional mencegah NullReferenceException."),
 Q("Perintah untuk menangkap kesalahan?", ["try/catch", "try/except", "on error", "rescue"], 0, "try/catch menangani pengecualian."),
])
QUIZZES["react"].extend([
 Q("Hook untuk efek samping seperti memuat data?", ["useState", "useEffect", "useProps", "useData"], 1, "useEffect berjalan setelah render."),
 Q("Sintaks JSX untuk menampilkan variabel nama?", ["{nama}", "${nama}", "<nama>", "[nama]"], 0, "Kurung kurawal menyisipkan ekspresi JavaScript."),
 Q("Penulisan atribut kelas CSS di JSX?", ["class", "className", "cssClass", "styleClass"], 1, "JSX memakai className."),
 Q("State sebaiknya diubah dengan...", ["Fungsi setter dari useState", "Langsung mengubah variabelnya", "document.getElementById", "window.state"], 0, "Gunakan fungsi setter agar React merender ulang."),
])
QUIZZES["mysql"].extend([
 Q("Perintah untuk menambah kolom ke tabel?", ["ALTER TABLE ... ADD", "UPDATE TABLE", "INSERT COLUMN", "MODIFY DB"], 0, "ALTER TABLE ... ADD COLUMN menambah kolom."),
 Q("Tipe data untuk tanggal?", ["DATE", "DAYTEXT", "TIMESTR", "CAL"], 0, "DATE menyimpan tanggal."),
 Q("Klausa untuk membatasi jumlah baris?", ["LIMIT", "TOP only", "MAX ROWS", "FETCH ALL"], 0, "LIMIT n membatasi jumlah baris."),
 Q("Fungsi untuk menggabungkan teks?", ["CONCAT", "JOINSTR", "MERGE", "APPEND"], 0, "CONCAT menggabungkan string."),
])
