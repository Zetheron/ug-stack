"""Materi pelajaran asli UG-Stack (4 pelajaran per bahasa). Setiap contoh kode bisa dibuka di editor Try it."""


def L(title, body, code):
    return {"title": title, "body": body.strip(), "code": code.strip("\n")}


LESSONS = {
"html": [
 L("Pengenalan HTML",
   "HTML (HyperText Markup Language) adalah bahasa markup untuk menyusun struktur halaman web. Browser membaca tag seperti <h1> dan <p>, lalu menampilkannya sebagai judul dan paragraf.\n\nDokumen HTML diawali <!DOCTYPE html>, berisi <head> untuk informasi halaman dan <body> untuk isi yang terlihat.",
   r'''<!DOCTYPE html>
<html>
  <head>
    <title>Halaman Pertamaku</title>
  </head>
  <body>
    <h1>Halo, UG-Stack!</h1>
    <p>Ini paragraf pertama saya.</p>
  </body>
</html>'''),
 L("Elemen, Atribut, dan Tautan",
   "Elemen terdiri dari tag pembuka, isi, dan tag penutup. Atribut memberi informasi tambahan pada elemen, misalnya href pada tautan atau src dan alt pada gambar.\n\nSelalu isi atribut alt pada gambar agar halaman bisa dipahami pembaca layar dan tetap bermakna bila gambar gagal dimuat.",
   r'''<h2>Sumber Belajar</h2>
<a href="https://developer.mozilla.org" target="_blank">Kunjungi MDN</a>
<img src="logo.png" alt="Logo UG-Stack" width="120">'''),
 L("Daftar dan Tabel",
   "Gunakan <ul> untuk daftar berpoin, <ol> untuk daftar bernomor, dan <li> untuk tiap itemnya. Data berbentuk baris dan kolom disusun dengan <table>, <tr> (baris), <th> (judul kolom), dan <td> (sel).",
   r'''<ol>
  <li>Belajar HTML</li>
  <li>Belajar CSS</li>
</ol>
<table border="1">
  <tr><th>Bahasa</th><th>Fungsi</th></tr>
  <tr><td>HTML</td><td>Struktur</td></tr>
  <tr><td>CSS</td><td>Tampilan</td></tr>
</table>'''),
 L("Formulir (Form)",
   "Formulir mengumpulkan input pengguna. Elemen <input> punya banyak tipe (text, email, password, number), dan <label> menjelaskan fungsi tiap kolom. Atribut required membuat browser memvalidasi kolom yang wajib diisi.",
   r'''<form action="/kirim" method="post">
  <label>Nama: <input type="text" name="nama" required></label><br>
  <label>Email: <input type="email" name="email"></label><br>
  <button type="submit">Kirim</button>
</form>'''),
],
"css": [
 L("Pengenalan CSS dan Selector",
   "CSS (Cascading Style Sheets) mengatur tampilan elemen HTML. Aturan CSS terdiri dari selector (siapa yang diubah) dan blok deklarasi (properti: nilai).\n\nSelector umum: nama elemen (p), kelas (.kartu), dan id (#header).",
   r'''h1 {
  color: #04AA6D;
  text-align: center;
}
.kartu {
  background: #f1f1f1;
  padding: 16px;
}'''),
 L("Warna dan Box Model",
   "Setiap elemen adalah kotak berlapis: content, padding (ruang dalam), border, dan margin (ruang luar). Memahami box model membantu mengatur jarak dan ukuran dengan tepat.\n\nGunakan box-sizing: border-box agar lebar elemen sudah termasuk padding dan border.",
   r'''* { box-sizing: border-box; }
.kotak {
  width: 200px;
  padding: 20px;
  border: 2px solid #282A35;
  margin: 10px;
  background-color: #E7F9F0;
}'''),
 L("Tata Letak dengan Flexbox",
   "Flexbox menyusun elemen dalam satu baris atau kolom dengan mudah. Setel display: flex pada wadah, lalu atur arah (flex-direction), perataan (justify-content, align-items), dan jarak (gap).",
   r'''.menu {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
}'''),
 L("Desain Responsif dengan Media Query",
   "Media query menerapkan aturan CSS hanya pada kondisi tertentu, misalnya lebar layar. Pendekatan mobile-first: tulis gaya dasar untuk HP, lalu tambahkan aturan untuk layar yang lebih lebar.",
   r'''.grid { display: grid; grid-template-columns: 1fr; gap: 12px; }

@media (min-width: 768px) {
  .grid { grid-template-columns: repeat(3, 1fr); }
}'''),
],
"javascript": [
 L("Variabel dan Tipe Data",
   "JavaScript membuat halaman web interaktif. Gunakan const untuk nilai yang tidak berubah dan let untuk yang berubah; hindari var. Tipe dasar: string, number, boolean, null, undefined.",
   r'''const nama = "Dina";
let umur = 20;
umur = umur + 1;
console.log(`${nama} berumur ${umur} tahun`);'''),
 L("Fungsi",
   "Fungsi membungkus langkah-langkah agar bisa dipakai ulang. Arrow function adalah penulisan ringkas yang sangat umum dipakai di JavaScript modern.",
   r'''function tambah(a, b) {
  return a + b;
}
const kali = (a, b) => a * b;
console.log(tambah(2, 3), kali(4, 5));'''),
 L("Array dan Perulangan",
   "Array menyimpan banyak nilai berurutan. Metode seperti map, filter, dan reduce mengolah array tanpa menulis perulangan manual.",
   r'''const nilai = [70, 85, 90, 55];
const lulus = nilai.filter(n => n >= 70);
const rata = nilai.reduce((a, b) => a + b, 0) / nilai.length;
console.log(lulus, rata);'''),
 L("DOM dan Event",
   "DOM adalah representasi halaman HTML yang bisa diubah lewat JavaScript. Pilih elemen dengan querySelector, lalu pasang event listener untuk merespons klik, input, dan lainnya.",
   r'''<button id="tombol">Klik saya</button>
<p id="pesan"></p>
<script>
  document.querySelector("#tombol").addEventListener("click", () => {
    document.querySelector("#pesan").textContent = "Halo dari JavaScript!";
  });
</script>'''),
],
"python": [
 L("Halo Python: Variabel dan Input/Output",
   "Python terkenal dengan sintaks yang bersih. Variabel dibuat langsung dengan tanda =, tanpa deklarasi tipe. Gunakan print() untuk menampilkan dan input() untuk membaca masukan pengguna.",
   r'''nama = "Dina"
umur = 20
print(f"Halo {nama}, umur kamu {umur} tahun")
tahun_depan = umur + 1
print("Tahun depan:", tahun_depan)'''),
 L("Percabangan dan Perulangan",
   "if/elif/else memilih jalur program berdasarkan kondisi. for mengulang atas urutan data, sedangkan while mengulang selama kondisi benar. Perhatikan indentasi: ia menandai blok kode.",
   r'''nilai = 78
if nilai >= 85:
    print("A")
elif nilai >= 70:
    print("B")
else:
    print("C")

for i in range(1, 4):
    print("Perulangan ke-", i)'''),
 L("List dan Dictionary",
   "list menyimpan data berurutan yang bisa diubah; dict menyimpan pasangan kunci-nilai. Keduanya adalah struktur data paling sering dipakai di Python.",
   r'''bahasa = ["Python", "HTML", "SQL"]
bahasa.append("CSS")
profil = {"nama": "Dina", "prodi": "Informatika"}
profil["angkatan"] = 2024
for b in bahasa:
    print(b)
print(profil)'''),
 L("Function dan Modularitas",
   "Function memecah program menjadi bagian kecil yang punya satu tugas. Gunakan return untuk mengembalikan hasil dan beri nama yang menjelaskan fungsinya. Program yang modular lebih mudah dibaca, diuji, dan dikembangkan.",
   r'''def hitung_rata(daftar):
    if not daftar:
        return 0
    return sum(daftar) / len(daftar)

print(hitung_rata([80, 90, 70]))'''),
],
"sql": [
 L("SELECT: Membaca Data",
   "SQL (Structured Query Language) dipakai untuk mengelola data di basis data relasional. SELECT memilih kolom dari sebuah tabel; tanda * berarti semua kolom.",
   r'''SELECT nama, prodi
FROM mahasiswa;

SELECT * FROM mahasiswa;'''),
 L("WHERE, ORDER BY, LIMIT",
   "WHERE menyaring baris, ORDER BY mengurutkan hasil (ASC naik, DESC turun), dan LIMIT membatasi jumlah baris yang ditampilkan.",
   r'''SELECT nama, ipk
FROM mahasiswa
WHERE ipk >= 3.5
ORDER BY ipk DESC
LIMIT 5;'''),
 L("INSERT, UPDATE, DELETE",
   "Tiga perintah untuk mengubah data: INSERT menambah baris, UPDATE mengubah, dan DELETE menghapus. Selalu sertakan WHERE pada UPDATE dan DELETE agar tidak mengubah seluruh tabel.",
   r'''INSERT INTO mahasiswa (nama, prodi, ipk)
VALUES ('Dina', 'Informatika', 3.8);

UPDATE mahasiswa SET ipk = 3.9 WHERE nama = 'Dina';
DELETE FROM mahasiswa WHERE nama = 'Dina';'''),
 L("JOIN: Menggabungkan Tabel",
   "JOIN menggabungkan baris dari dua tabel berdasarkan kolom yang berhubungan, biasanya kunci asing. INNER JOIN hanya menampilkan baris yang cocok di kedua tabel.",
   r'''SELECT m.nama, k.nama_kelas
FROM mahasiswa m
INNER JOIN kelas k ON m.kelas_id = k.id;'''),
],
"java": [
 L("Struktur Program Java",
   "Program Java berada di dalam kelas. Eksekusi dimulai dari method main. Java adalah bahasa berorientasi objek yang dikompilasi menjadi bytecode dan dijalankan di JVM.",
   r'''public class Halo {
    public static void main(String[] args) {
        System.out.println("Halo, UG-Stack!");
    }
}'''),
 L("Variabel dan Tipe Data",
   "Java bertipe statis: tipe variabel harus dideklarasikan. Tipe primitif umum: int, double, boolean, char. String adalah kelas untuk teks.",
   r'''int umur = 20;
double ipk = 3.75;
boolean aktif = true;
String nama = "Dina";
System.out.println(nama + " - IPK " + ipk);'''),
 L("Kelas dan Objek",
   "Kelas adalah cetak biru; objek adalah hasil bentukannya. Kelas berisi atribut (data) dan method (perilaku). Kata kunci new membuat objek.",
   r'''class Mahasiswa {
    String nama;
    Mahasiswa(String nama) { this.nama = nama; }
    void sapa() { System.out.println("Halo, saya " + nama); }
}
// pemakaian: new Mahasiswa("Dina").sapa();'''),
 L("Array dan Perulangan",
   "Array menyimpan sejumlah data bertipe sama dengan ukuran tetap. Perulangan for atau for-each dipakai untuk menelusurinya.",
   r'''int[] nilai = {80, 90, 70};
int total = 0;
for (int n : nilai) {
    total += n;
}
System.out.println("Rata-rata: " + (double) total / nilai.length);'''),
],
"php": [
 L("Sintaks Dasar PHP",
   "PHP berjalan di sisi server dan menghasilkan HTML. Kode PHP berada di dalam tag <?php ... ?>. Tiap pernyataan diakhiri titik koma, dan variabel diawali tanda $.",
   r'''<?php
$nama = "Dina";
echo "Halo, " . $nama . "!";
?>'''),
 L("Array dan Perulangan",
   "PHP punya array berindeks dan array asosiatif (kunci-nilai). foreach menelusuri isi array dengan ringkas.",
   r'''<?php
$bahasa = ["PHP", "HTML", "SQL"];
foreach ($bahasa as $b) {
    echo $b . "<br>";
}
$profil = ["nama" => "Dina", "prodi" => "Informatika"];
echo $profil["nama"];
?>'''),
 L("Fungsi",
   "Fungsi dibuat dengan kata kunci function. Tipe parameter dan nilai kembali bisa dideklarasikan sehingga kode lebih jelas dan aman.",
   r'''<?php
function luasPersegi(int $sisi): int {
    return $sisi * $sisi;
}
echo luasPersegi(5);
?>'''),
 L("Mengolah Data Formulir",
   "Data formulir diterima lewat variabel superglobal $_POST atau $_GET. Selalu validasi dan bersihkan input sebelum dipakai; gunakan htmlspecialchars() saat menampilkannya kembali untuk mencegah XSS.",
   r'''<?php
if ($_SERVER["REQUEST_METHOD"] === "POST") {
    $nama = trim($_POST["nama"] ?? "");
    if ($nama === "") {
        echo "Nama wajib diisi.";
    } else {
        echo "Halo, " . htmlspecialchars($nama);
    }
}
?>'''),
],
"c": [
 L("Program C Pertama",
   "C adalah bahasa dasar yang dekat dengan perangkat keras. Program dimulai dari fungsi main(). Header stdio.h menyediakan printf dan scanf untuk input/output.",
   r'''#include <stdio.h>

int main(void) {
    printf("Halo, UG-Stack!\n");
    return 0;
}'''),
 L("Variabel dan Input",
   "C bertipe statis: int untuk bilangan bulat, float/double untuk pecahan, char untuk karakter. scanf membaca input; format %d untuk int dan %f untuk float. Perhatikan tanda & pada scanf.",
   r'''#include <stdio.h>

int main(void) {
    int umur;
    printf("Umur: ");
    scanf("%d", &umur);
    printf("Tahun depan: %d\n", umur + 1);
    return 0;
}'''),
 L("Perulangan dan Percabangan",
   "for, while, dan do-while mengulang kode; if/else if/else mengatur percabangan. Contoh berikut mencetak bilangan genap dari 1 sampai 10.",
   r'''#include <stdio.h>

int main(void) {
    for (int i = 1; i <= 10; i++) {
        if (i % 2 == 0) {
            printf("%d\n", i);
        }
    }
    return 0;
}'''),
 L("Array dan Pointer Dasar",
   "Array menyimpan data bertipe sama. Pointer menyimpan alamat memori; operator & mengambil alamat dan * mengakses nilai di alamat tersebut. Pointer adalah kunci memahami memori di C.",
   r'''#include <stdio.h>

int main(void) {
    int nilai[3] = {80, 90, 70};
    int *p = &nilai[0];
    printf("%d %d\n", nilai[1], *(p + 2));
    return 0;
}'''),
],
"cpp": [
 L("Program C++ Pertama",
   "C++ memperluas C dengan pemrograman berorientasi objek dan pustaka standar (STL). cout menampilkan keluaran dan cin membaca masukan dari pustaka iostream.",
   r'''#include <iostream>
using namespace std;

int main() {
    cout << "Halo, UG-Stack!" << endl;
    return 0;
}'''),
 L("Vector dan String",
   "std::vector adalah array dinamis yang ukurannya bisa berubah, dan std::string menangani teks dengan aman. Keduanya jauh lebih nyaman daripada array dan char[] gaya C.",
   r'''#include <iostream>
#include <vector>
#include <string>
using namespace std;

int main() {
    vector<int> nilai = {80, 90, 70};
    nilai.push_back(85);
    string nama = "Dina";
    cout << nama << " punya " << nilai.size() << " nilai" << endl;
    return 0;
}'''),
 L("Kelas dan Objek",
   "Kelas membungkus data dan perilaku. Konstruktor menginisialisasi objek, sedangkan modifier private/public mengatur akses ke anggota kelas.",
   r'''#include <iostream>
#include <string>
using namespace std;

class Mahasiswa {
  private:
    string nama;
  public:
    Mahasiswa(string n) : nama(n) {}
    void sapa() { cout << "Halo, " << nama << endl; }
};

int main() { Mahasiswa("Dina").sapa(); }'''),
 L("Algoritma STL",
   "Header algorithm menyediakan fungsi siap pakai seperti sort, find, dan count. Memakainya menghemat waktu dan mengurangi bug dibanding menulis ulang.",
   r'''#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;

int main() {
    vector<int> v = {5, 2, 9, 1};
    sort(v.begin(), v.end());
    for (int x : v) cout << x << " ";
}'''),
],
"csharp": [
 L("Program C# Pertama",
   "C# adalah bahasa modern dari Microsoft untuk .NET, aplikasi desktop, web, dan game Unity. Console.WriteLine menampilkan teks ke konsol.",
   r'''using System;

class Program {
    static void Main() {
        Console.WriteLine("Halo, UG-Stack!");
    }
}'''),
 L("Variabel dan Tipe Data",
   "C# bertipe statis tetapi mendukung var untuk inferensi tipe. Tipe umum: int, double, bool, string. Interpolasi string memakai awalan $.",
   r'''string nama = "Dina";
int umur = 20;
var ipk = 3.8;
Console.WriteLine($"{nama}, {umur} tahun, IPK {ipk}");'''),
 L("List dan LINQ",
   "List<T> adalah koleksi dinamis. LINQ memungkinkan menyaring dan mengolah koleksi dengan sintaks ringkas, mirip SQL.",
   r'''using System;
using System.Collections.Generic;
using System.Linq;

var nilai = new List<int> { 80, 55, 90 };
var lulus = nilai.Where(n => n >= 70).ToList();
Console.WriteLine(string.Join(", ", lulus));'''),
 L("Kelas dan Properti",
   "Kelas C# memakai properti (get/set) untuk mengakses data secara terkontrol. Konstruktor menyiapkan objek saat dibuat.",
   r'''class Mahasiswa {
    public string Nama { get; set; }
    public Mahasiswa(string nama) { Nama = nama; }
    public void Sapa() => Console.WriteLine($"Halo, {Nama}");
}'''),
],
"react": [
 L("Komponen",
   "React membangun antarmuka dari komponen: fungsi yang mengembalikan JSX (HTML di dalam JavaScript). Nama komponen harus diawali huruf kapital.",
   r'''function Salam() {
  return <h1>Halo, UG-Stack!</h1>;
}

export default function App() {
  return <Salam />;
}'''),
 L("Props",
   "Props adalah data yang dikirim dari komponen induk ke anak, mirip atribut HTML. Props bersifat hanya-baca di dalam komponen penerima.",
   r'''function Kartu({ judul, level }) {
  return <div className="kartu"><h3>{judul}</h3><p>{level}</p></div>;
}

// pemakaian: <Kartu judul="Python" level="Pemula" />'''),
 L("State dengan useState",
   "State menyimpan data yang berubah dan memicu tampilan ulang saat berubah. Hook useState mengembalikan nilai saat ini dan fungsi untuk mengubahnya.",
   r'''import { useState } from "react";

function Penghitung() {
  const [n, setN] = useState(0);
  return <button onClick={() => setN(n + 1)}>Diklik {n} kali</button>;
}'''),
 L("Menampilkan Daftar dan Kondisi",
   "Gunakan map untuk merender daftar dan beri setiap item properti key yang unik. Rendering kondisional memakai operator ternary atau &&.",
   r'''function Daftar({ bahasa }) {
  if (bahasa.length === 0) return <p>Belum ada data.</p>;
  return (
    <ul>
      {bahasa.map(b => <li key={b}>{b}</li>)}
    </ul>
  );
}'''),
],
"mysql": [
 L("Membuat Database dan Tabel",
   "MySQL adalah sistem manajemen basis data relasional. Basis data dibuat dengan CREATE DATABASE, dan struktur data didefinisikan dengan CREATE TABLE beserta tipe tiap kolom.",
   r'''CREATE DATABASE ugstack;
USE ugstack;

CREATE TABLE mahasiswa (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nama VARCHAR(60) NOT NULL,
  prodi VARCHAR(40),
  ipk DECIMAL(3,2)
);'''),
 L("Tipe Data dan Kunci",
   "Pilih tipe data yang paling sesuai: INT untuk bilangan bulat, VARCHAR(n) untuk teks pendek, DATE untuk tanggal, DECIMAL untuk angka presisi. PRIMARY KEY mengidentifikasi baris secara unik, dan FOREIGN KEY menghubungkan antar tabel.",
   r'''CREATE TABLE nilai (
  id INT AUTO_INCREMENT PRIMARY KEY,
  mahasiswa_id INT NOT NULL,
  mata_kuliah VARCHAR(50),
  skor INT,
  FOREIGN KEY (mahasiswa_id) REFERENCES mahasiswa(id)
);'''),
 L("Agregasi dengan GROUP BY",
   "Fungsi agregat (COUNT, SUM, AVG, MIN, MAX) meringkas banyak baris. GROUP BY mengelompokkan baris, dan HAVING menyaring hasil kelompok.",
   r'''SELECT prodi, COUNT(*) AS jumlah, AVG(ipk) AS rata_ipk
FROM mahasiswa
GROUP BY prodi
HAVING AVG(ipk) >= 3.0;'''),
 L("Index dan EXPLAIN",
   "Index mempercepat pencarian pada kolom yang sering difilter, dengan biaya ruang dan kecepatan tulis. EXPLAIN menunjukkan bagaimana MySQL menjalankan sebuah query sehingga kita bisa mengoptimalkannya.",
   r'''CREATE INDEX idx_prodi ON mahasiswa (prodi);

EXPLAIN SELECT nama FROM mahasiswa WHERE prodi = 'Informatika';'''),
],
}
