"""Pengujian lanjutan: algoritma, keamanan, audit, CSV, backup, soal kustom, CLI, dan konkurensi."""
import json
import os
import random
import shutil
import tempfile
import threading
import unittest

import cli
from content.quizzes import QUIZZES
from services import admin_code, algorithms, audit, auth, backup, csv_io, modules, progress, quiz, quiz_admin, storage

ADMIN = {"username": "admin", "role": "admin"}


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        os.environ["FLET_APP_STORAGE_DATA"] = self.tmp
        os.environ["UG_ADMIN_KEY"] = "kunci-uji-admin-123"
        auth.init_data()
        auth.reset_lock()

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)
        os.environ.pop("FLET_APP_STORAGE_DATA", None)
        os.environ.pop("UG_ADMIN_KEY", None)

    def student(self, name="budi123"):
        auth.register(name, "Rahasia123", "Rahasia123")
        return {"username": name, "role": "mahasiswa"}

    def data(self, **kw):
        d = {"judul": "Modul Uji", "bahasa": "Python", "level": "Beginner", "durasi": "30", "deskripsi": "uji"}
        d.update(kw)
        return d


class TestAlgoritma(unittest.TestCase):
    def test_T28_sorting_dan_searching_buatan_sendiri(self):
        random.seed(7)
        for n in (0, 1, 2, 17, 200):
            data = [{"k": random.randint(0, 20), "i": i} for i in range(n)]
            for desc in (False, True):
                expect = sorted(data, key=lambda x: x["k"], reverse=desc)
                self.assertEqual(algorithms.merge_sort(data, key=lambda x: x["k"], descending=desc), expect)
                self.assertEqual(algorithms.insertion_sort(data, key=lambda x: x["k"], descending=desc), expect)
        ids = list(range(1, 50, 3))
        for target in ids:
            self.assertEqual(algorithms.binary_search(ids, target), ids.index(target))
        self.assertEqual(algorithms.binary_search(ids, 2), -1)
        self.assertEqual(algorithms.binary_search([], 1), -1)
        self.assertEqual(algorithms.linear_search(["a", "b", "c"], "c"), 2)
        self.assertEqual(algorithms.linear_search([], "x"), -1)
        self.assertTrue(algorithms.is_sorted(ids))


class TestModulAlgoritma(Base):
    def test_T29_modul_memakai_algoritma_sendiri(self):
        mods = modules.list_modules()
        for sort_by in ("judul", "durasi", "level"):
            for desc in (False, True):
                hasil = modules.search_modules(mods, "", "Semua", sort_by, desc)
                self.assertEqual(len(hasil), len(mods))
        self.assertEqual(modules.get_module(5)["id"], 5)
        self.assertIsNone(modules.get_module(999))


class TestAudit(Base):
    def test_T30_audit_log_paginasi_dan_tanpa_password(self):
        for i in range(12):
            audit.log("admin", "UJI", f"entri {i}")
        halaman1, total_hal, total = audit.list_logs(1, 5, "uji")
        self.assertEqual((len(halaman1), total_hal, total), (5, 3, 12))
        self.assertEqual(halaman1[0]["detail"], "entri 11")                   # terbaru dulu
        self.assertEqual(len(audit.list_logs(3, 5, "uji")[0]), 2)
        auth.login("admin", "PasswordRahasia999")
        self.assertNotIn("PasswordRahasia999", json.dumps(storage.load_json("activity_log.json", [])))
        self.assertTrue(any(e["action"] == "LOGIN_GAGAL" for e in audit.list_logs(1, 50)[0]))


class TestKeamanan(Base):
    def test_T31_kunci_akun_tersimpan_di_file(self):
        for _ in range(3):
            auth.login("admin", "salah1234")
        self.assertTrue(os.path.exists(os.path.join(self.tmp, "lockouts.json")))
        locks = storage.load_json("lockouts.json", {})
        self.assertGreater(locks["admin"]["locked_until"], 0)                  # tetap terkunci setelah "restart"
        self.assertIn("terkunci", auth.login("admin", "Admin123")[1])

    def test_T32_admin_bawaan_wajib_ganti_password(self):
        ok, _, user = auth.login("admin", "Admin123", allow_admin=True)
        self.assertTrue(ok and user["must_change"])
        self.assertFalse(auth.change_password("admin", "salah1234", "BaruAman123", "BaruAman123")[0])
        self.assertFalse(auth.change_password("admin", "Admin123", "pendek1", "pendek1")[0])
        self.assertFalse(auth.change_password("admin", "Admin123", "BaruAman123", "Beda123456")[0])
        self.assertFalse(auth.change_password("admin", "Admin123", "Admin123", "Admin123")[0])
        self.assertTrue(auth.change_password("admin", "Admin123", "BaruAman123", "BaruAman123")[0])
        ok, _, user = auth.login("admin", "BaruAman123", allow_admin=True)
        self.assertTrue(ok and not user["must_change"])
        self.assertFalse(auth.login("admin", "Admin123", allow_admin=True)[0])

    def test_T33_admin_lama_berpassword_bawaan_ditandai(self):
        users = storage.load_json("users.json", [])
        users[0].pop("must_change")
        storage.save_json("users.json", users)
        auth.init_data()
        self.assertTrue(storage.load_json("users.json", [])[0]["must_change"])

    def test_T34_manajemen_pengguna(self):
        s = self.student()
        self.assertEqual(auth.list_users(s), [])                                # mahasiswa tidak boleh
        self.assertEqual(len(auth.list_users(ADMIN)), 2)
        self.assertFalse(auth.reset_password(s, "admin", "Rahasia123")[0])
        self.assertTrue(auth.reset_password(ADMIN, "budi123", "Sementara123")[0])
        ok, _, user = auth.login("budi123", "Sementara123")
        self.assertTrue(ok and user["must_change"])
        self.assertFalse(auth.set_role(ADMIN, "admin", "mahasiswa")[0])         # admin terakhir
        self.assertFalse(auth.set_role(ADMIN, "budi123", "dewa")[0])
        self.assertTrue(auth.set_role(ADMIN, "budi123", "admin")[0])
        self.assertTrue(auth.set_role(ADMIN, "admin", "mahasiswa")[0])          # kini ada 2 admin, boleh diturunkan
        budi = {"username": "budi123", "role": "admin"}
        self.assertFalse(auth.delete_user(budi, "budi123")[0])                  # tidak boleh menghapus akun sendiri
        progress.toggle_done("admin", 1)
        quiz.save_result("admin", "python", quiz.grade("python", [q["answer"] for q in QUIZZES["python"]]))
        self.assertTrue(auth.delete_user(budi, "admin")[0])
        self.assertEqual(progress.get_done("admin"), [])                        # data terkait ikut bersih
        self.assertEqual(quiz.get_results("admin"), {})
        self.assertFalse(auth.delete_user(budi, "admin")[0])                    # sudah tidak ada
        self.assertFalse(auth.set_role(budi, "budi123", "mahasiswa")[0])        # admin terakhir tidak boleh turun

    def test_T40_penulisan_bersamaan_tidak_bentrok(self):
        errors = []

        def daftar(i):
            ok, msg = auth.register(f"user_{i:03d}", "Rahasia123", "Rahasia123")
            if not ok:
                errors.append(msg)

        threads = [threading.Thread(target=daftar, args=(i,)) for i in range(15)]
        [t.start() for t in threads]
        [t.join() for t in threads]
        self.assertEqual(errors, [])
        self.assertEqual(len(storage.load_json("users.json", [])), 16)          # 15 + admin, tanpa data hilang


class TestSoalKustom(Base):
    SOAL = {"q": "Apa itu variabel?", "options": ["Wadah data", "Jenis loop", "Nama file", "Operator"], "answer": 0,
            "explain": "Variabel menyimpan nilai."}

    def test_T35_soal_quiz_kustom(self):
        awal = len(quiz_admin.get_questions("python"))
        self.assertFalse(quiz_admin.add_question(self.student(), "python", self.SOAL)[0])
        for rusak in ({"q": ""}, dict(self.SOAL, answer=9), dict(self.SOAL, options=["a", "a", "b", "c"]),
                      dict(self.SOAL, explain=""), dict(self.SOAL, options=["a", "b", "c", ""])):
            self.assertFalse(quiz_admin.add_question(ADMIN, "python", dict(self.SOAL, **rusak))[0])
        self.assertTrue(quiz_admin.add_question(ADMIN, "python", self.SOAL)[0])
        self.assertEqual(len(quiz_admin.get_questions("python")), awal + 1)
        hasil = quiz.grade("python", [q["answer"] for q in quiz_admin.get_questions("python")])
        self.assertEqual(hasil["total"], awal + 1)
        qid = quiz_admin.list_custom()[0]["id"]
        self.assertTrue(quiz_admin.delete_question(ADMIN, "python", qid)[0])
        self.assertFalse(quiz_admin.delete_question(ADMIN, "python", qid)[0])


class TestCsvDanBackup(Base):
    def test_T36_ekspor_impor_csv(self):
        teks = csv_io.export_modules_csv()
        self.assertTrue(teks.startswith("id,judul,bahasa,level,durasi,deskripsi"))
        self.assertFalse(csv_io.import_modules_csv(self.student(), teks)[0])         # bukan admin
        self.assertFalse(csv_io.import_modules_csv(ADMIN, "")[0])
        self.assertFalse(csv_io.import_modules_csv(ADMIN, "a,b\n1,2")[0])           # kolom wajib hilang
        ok, _, laporan = csv_io.import_modules_csv(ADMIN, teks)                      # semua duplikat
        self.assertTrue(ok and laporan["added"] == 0 and len(laporan["skipped"]) == 8)
        baru = ("judul,bahasa,level,durasi,deskripsi\nModul A,Python,Beginner,20,x\n"
                "Modul B,Cobol,Beginner,20,x\nModul C,SQL,Beginner,abc,x\nModul A,Python,Beginner,20,x\n")
        ok, msg, laporan = csv_io.import_modules_csv(ADMIN, baru)
        self.assertTrue(ok)
        self.assertEqual(laporan["added"], 1)
        self.assertEqual([b[0] for b in laporan["skipped"]], [3, 4, 5])             # nomor baris yang gagal
        self.assertEqual(len(modules.list_modules()), 9)
        ok, path = csv_io.export_to_file()
        self.assertTrue(ok and os.path.exists(path))

    def test_T37_backup_dan_restore(self):
        self.assertFalse(backup.create_backup(self.student())[0])
        ok, msg = backup.create_backup(ADMIN)
        self.assertTrue(ok)
        nama = backup.list_backups()[0]
        modules.add_module(ADMIN, self.data())
        self.assertEqual(len(modules.list_modules()), 9)
        self.assertTrue(backup.restore_backup(ADMIN, nama)[0])
        self.assertEqual(len(modules.list_modules()), 8)                              # kembali seperti backup
        self.assertFalse(backup.restore_backup(ADMIN, "../../etc")[0])               # nama tidak valid ditolak
        self.assertFalse(backup.restore_backup(ADMIN, "20200101_000000")[0])         # tidak ada
        storage.save_json(f"backup_{nama}.json", {"files": {"modules.json": "bukan daftar"}})   # snapshot rusak
        modules.add_module(ADMIN, self.data(judul="Tambahan"))
        self.assertFalse(backup.restore_backup(ADMIN, nama)[0])                       # backup rusak ditolak
        self.assertIn("Tambahan", [m["judul"] for m in modules.list_modules()])      # data tidak berubah


def jalankan_cli(inputs):
    antrian = iter(inputs)
    keluar = []
    cli.run(cli.Console(lambda prompt: next(antrian), keluar.append))
    return "\n".join(keluar)


class TestCli(Base):
    def test_T38_cli_alur_admin_lengkap(self):
        out = jalankan_cli([
            "3", "admin", admin_code.current_code(),       # login admin lewat kode berputar
            "3", "Modul CLI", "4", "1", "30", "uji cli",   # tambah (Python, Beginner)
            "1",                                           # tampil
            "2", "CLI", "", "", "t",                       # cari
            "4", "9", "", "4", "2", "", "",                # ubah id 9 (level -> Intermediate)
            "5", "9", "y",                                 # hapus
            "7", "q",                                      # log aktivitas
            "9",                                           # logout
            "0"])                                          # keluar
        for teks in ("Login admin berhasil", "[OK] Modul berhasil ditambahkan",
                     "Modul CLI", "Modul berhasil diubah", "Modul berhasil dihapus", "Log aktivitas",
                     "Anda telah logout", "Sampai jumpa"):
            self.assertIn(teks, out)
        self.assertIsNone(modules.get_module(9))
        self.assertTrue(any(e["action"] == "LOGOUT" for e in audit.list_logs(1, 50)[0]))

    def test_T39_cli_mahasiswa_dan_input_salah(self):
        out = jalankan_cli(["2", "siti_01", "Rahasia123", "Rahasia123",                  # daftar
                            "1", "siti_01", "salah", "siti_01", "salah", "siti_01", "salah",   # 3x gagal
                            "1", "siti_01", "Rahasia123",                                 # login (terkunci)
                            "x", "0"])
        self.assertIn("Registrasi berhasil", out)
        self.assertIn("terkunci", out)
        self.assertIn("Login gagal", out)
        auth.reset_lock()
        out = jalankan_cli(["1", "siti_01", "Rahasia123",
                            "3", "abc", "3", "999", "3", "1", "4", "99", "9", "0"])       # id salah, id tak ada, id valid
        self.assertIn("ID harus berupa angka", out)
        self.assertIn("Modul tidak ditemukan", out)
        self.assertIn("Modul ditandai selesai", out)
        self.assertIn("Progres Anda: 12%", out)
        self.assertIn("Pilihan tidak dikenal", out)


if __name__ == "__main__":
    unittest.main(verbosity=2)
