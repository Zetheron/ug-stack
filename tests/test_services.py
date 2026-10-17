"""Pengujian otomatis lapisan logika UG-Stack. Jalankan: python -m unittest tests.test_services -v"""
import os
import shutil
import tempfile
import unittest

from services import auth, modules, progress, storage
from services.storage import StorageError


class BaseCase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        os.environ["FLET_APP_STORAGE_DATA"] = self.tmp   # data uji terpisah dari data asli
        auth.reset_lock()
        auth.init_data()

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)
        os.environ.pop("FLET_APP_STORAGE_DATA", None)
        os.environ.pop("UG_ADMIN_KEY", None)

    def admin(self):
        return {"username": "admin", "role": "admin"}

    def student(self):
        auth.register("budi123", "Rahasia123", "Rahasia123")
        return {"username": "budi123", "role": "mahasiswa"}


class TestLoginAuth(BaseCase):
    def test_T01_login_berhasil(self):
        ok, _, user = auth.login("admin", "Admin123", allow_admin=True)      # jalur internal (admin tidak login lewat UI dengan password)
        self.assertTrue(ok)
        self.assertEqual(user["role"], "admin")
        ok, msg, user = auth.login("admin", "Admin123")                      # jalur UI: admin ditolak walau password benar
        self.assertFalse(ok)
        self.assertIsNone(user)
        self.assertIn("tidak dapat masuk dengan password", msg)
        self.student()
        self.assertTrue(auth.login("budi123", "Rahasia123")[0])              # mahasiswa tetap bisa

    def test_T02_login_gagal_password_salah(self):
        ok, msg, user = auth.login("admin", "salah123")
        self.assertFalse(ok)
        self.assertIsNone(user)
        self.assertIn("Sisa percobaan: 2", msg)

    def test_T03_login_input_kosong(self):
        ok, msg, _ = auth.login("", "")
        self.assertFalse(ok)
        self.assertIn("wajib diisi", msg)

    def test_T04_akun_terkunci_setelah_3_kali_gagal(self):
        for _ in range(3):
            auth.login("admin", "salah123")
        ok, msg, _ = auth.login("admin", "Admin123")   # benar pun ditolak saat terkunci
        self.assertFalse(ok)
        self.assertIn("terkunci", msg)

    def test_T05_password_tidak_disimpan_polos(self):
        users = storage.load_json("users.json", [])
        self.assertNotIn("Admin123", str(users))

    def test_T06_registrasi_valid_dan_username_ganda(self):
        self.assertTrue(auth.register("siti_01", "Rahasia123", "Rahasia123")[0])
        ok, msg = auth.register("SITI_01", "Rahasia123", "Rahasia123")
        self.assertFalse(ok)
        self.assertIn("sudah dipakai", msg)


class TestValidasi(BaseCase):
    def test_T07_validasi_registrasi(self):
        self.assertFalse(auth.register("", "Rahasia123", "Rahasia123")[0])
        self.assertFalse(auth.register("ab", "Rahasia123", "Rahasia123")[0])
        self.assertFalse(auth.register("budi123", "pendek1", "pendek1")[0])
        self.assertFalse(auth.register("budi123", "hurufsaja", "hurufsaja")[0])
        self.assertFalse(auth.register("budi123", "Rahasia123", "Beda12345")[0])

    def test_T08_validasi_modul(self):
        base = {"judul": "Modul Uji", "bahasa": "Python", "level": "Beginner", "durasi": "30", "deskripsi": ""}
        for kunci, nilai in [("judul", ""), ("bahasa", "Cobol"), ("level", "Dewa"), ("durasi", "abc"), ("durasi", "0")]:
            data = dict(base); data[kunci] = nilai
            self.assertFalse(modules.add_module(self.admin(), data)[0], f"{kunci}={nilai}")


class TestCRUD(BaseCase):
    DATA = {"judul": "Modul Uji", "bahasa": "Python", "level": "Beginner", "durasi": "30", "deskripsi": "uji"}

    def test_T09_tambah_modul(self):
        before = len(modules.list_modules())
        ok, _ = modules.add_module(self.admin(), self.DATA)
        self.assertTrue(ok)
        self.assertEqual(len(modules.list_modules()), before + 1)

    def test_T10_mahasiswa_tidak_boleh_ubah_data(self):
        s = self.student()
        self.assertFalse(modules.add_module(s, self.DATA)[0])
        self.assertFalse(modules.update_module(s, 1, self.DATA)[0])
        self.assertFalse(modules.delete_module(s, 1)[0])

    def test_T11_pencarian_filter_sorting(self):
        mods = modules.list_modules()
        hasil = modules.search_modules(mods, keyword="python")
        self.assertTrue(hasil and all("python" in (m["judul"] + m["deskripsi"]).lower() for m in hasil))
        hasil = modules.search_modules(mods, bahasa="SQL")
        self.assertTrue(all(m["bahasa"] == "SQL" for m in hasil))
        hasil = modules.search_modules(mods, sort_by="durasi", descending=True)
        durasi = [m["durasi"] for m in hasil]
        self.assertEqual(durasi, sorted(durasi, reverse=True))
        self.assertEqual(modules.search_modules(mods, keyword="tidak-ada-xyz"), [])

    def test_T12_ubah_modul(self):
        ok, _ = modules.update_module(self.admin(), 1, self.DATA)
        self.assertTrue(ok)
        self.assertEqual(modules.get_module(1)["judul"], "Modul Uji")
        self.assertFalse(modules.update_module(self.admin(), 999, self.DATA)[0])

    def test_T13_hapus_modul_dan_progres_terkait(self):
        s = self.student()
        progress.toggle_done(s["username"], 2)
        ok, _ = modules.delete_module(self.admin(), 2)
        self.assertTrue(ok)
        self.assertIsNone(modules.get_module(2))
        self.assertNotIn(2, progress.get_done(s["username"]))
        self.assertFalse(modules.delete_module(self.admin(), 2)[0])   # sudah tidak ada


class TestProgresDanFile(BaseCase):
    def test_T14_progres_dan_persentase(self):
        s = self.student()
        ids = [m["id"] for m in modules.list_modules()]
        progress.toggle_done(s["username"], ids[0])
        progress.toggle_done(s["username"], ids[1])
        self.assertAlmostEqual(progress.percent(progress.get_done(s["username"]), ids), 100 * 2 / len(ids))
        progress.toggle_done(s["username"], ids[1])                      # batalkan
        self.assertEqual(len(progress.get_done(s["username"])), 1)
        self.assertEqual(progress.percent([], []), 0.0)

    def test_T15_data_tersimpan_dan_terbaca_kembali(self):
        modules.add_module(self.admin(), TestCRUD.DATA)
        self.assertTrue(os.path.exists(os.path.join(self.tmp, "modules.json")))
        self.assertIn("Modul Uji", [m["judul"] for m in modules.list_modules()])

    def test_T16_file_json_rusak_ditangani(self):
        with open(os.path.join(self.tmp, "modules.json"), "w") as f:
            f.write("{ bukan json")
        self.assertTrue(len(modules.list_modules()) > 0)                   # dipulihkan dari data bawaan
        self.assertTrue(os.path.exists(os.path.join(self.tmp, "modules.json.corrupt")))

    def test_T17_folder_tidak_bisa_ditulis(self):
        os.environ["FLET_APP_STORAGE_DATA"] = "/proc/tidak/bisa/ditulis"
        with self.assertRaises(StorageError):
            storage.save_json("x.json", {})
        ok, _ = auth.register("budi123", "Rahasia123", "Rahasia123")
        self.assertFalse(ok)                                               # tidak crash, pesan kesalahan


if __name__ == "__main__":
    unittest.main(verbosity=2)
