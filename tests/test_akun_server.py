"""Pengujian: backend penyimpanan (perangkat/PostgreSQL), peran dosen, pembuatan akun oleh admin,
pendaftaran mandiri, langganan/kursus, dan pengaturan server."""
import os
import shutil
import tempfile
import unittest

import cli

from services import (auth, backup, enrollment, modules, quiz_admin, settings, storage)

ADMIN = {"username": "admin", "role": "admin"}
DOSEN = {"username": "dosen_01", "role": "dosen"}
MHS = {"username": "budi123", "role": "mahasiswa"}
DATA = {"judul": "Modul Dosen", "bahasa": "Python", "level": "Beginner", "durasi": "30", "deskripsi": "uji"}


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        os.environ["FLET_APP_STORAGE_DATA"] = self.tmp
        os.environ["UG_ADMIN_KEY"] = "kunci-uji-admin-123"
        storage.reset_backend()
        auth.init_data()
        auth.reset_lock()

    def tearDown(self):
        storage.reset_backend()
        shutil.rmtree(self.tmp, ignore_errors=True)
        os.environ.pop("FLET_APP_STORAGE_DATA", None)
        os.environ.pop("UG_ADMIN_KEY", None)
        os.environ.pop("UG_ADMIN_PASSWORD", None)
        os.environ.pop("DATABASE_URL", None)


# ------------------------------------------------------------------ backend penyimpanan
class FakeClientStorage:
    """Meniru page.client_storage Flet (SharedPreferences)."""
    def __init__(self):
        self.d = {}
    def get(self, k): return self.d.get(k)
    def set(self, k, v): self.d[k] = v; return True
    def remove(self, k): return self.d.pop(k, None) is not None
    def get_keys(self, prefix): return [k for k in self.d if k.startswith(prefix)]


class FakeConnection:
    """Meniru pg8000.native.Connection untuk tabel ug_kv."""
    def __init__(self, store, fail_first=False):
        self.store, self.fail_first, self.closed = store, fail_first, False
    def run(self, sql, **p):
        if self.fail_first:
            self.fail_first = False
            raise OSError("koneksi terputus")
        if sql.startswith("CREATE TABLE"):
            return None
        if sql.startswith("SELECT data"):
            return [[self.store[p["n"]]]] if p["n"] in self.store else []
        if sql.startswith("INSERT"):
            self.store[p["n"]] = p["d"]
            return None
        if sql.startswith("DELETE"):
            self.store.pop(p["n"], None)
            return None
        if sql.startswith("SELECT name"):
            return [[k] for k in self.store]
        raise AssertionError("SQL tak dikenal: " + sql)
    def close(self):
        self.closed = True


class TestBackend(Base):
    def test_T41_backend_penyimpanan_perangkat_untuk_apk(self):
        cs = FakeClientStorage()
        storage.set_backend(storage.ClientStorageBackend(cs))
        auth.init_data()
        self.assertTrue(auth.register("budi123", "Rahasia123", "Rahasia123")[0])
        self.assertTrue(modules.add_module(ADMIN, DATA)[0])
        self.assertTrue(any(k.startswith("ugstack:users.json") for k in cs.d))
        storage.reset_backend()                                              # "tutup aplikasi"
        storage.set_backend(storage.ClientStorageBackend(cs))                # "buka lagi": data tetap ada
        self.assertTrue(auth.login("budi123", "Rahasia123")[0])
        self.assertIn("Modul Dosen", [m["judul"] for m in modules.list_modules()])
        cs.d["ugstack:modules.json"] = "{rusak"                              # data rusak dipulihkan
        self.assertGreater(len(modules.list_modules()), 0)
        self.assertIn("ugstack:modules.json.corrupt", cs.d)
        self.assertEqual(storage.backend_label(), "penyimpanan perangkat")

    def test_T42_backend_postgres_dan_koneksi_ulang(self):
        store = {}
        conns = []

        def connect():
            c = FakeConnection(store, fail_first=(len(conns) == 0))          # koneksi pertama putus -> harus dicoba ulang
            conns.append(c)
            return c
        storage.set_backend(storage.PostgresBackend(connect))
        auth.init_data()
        self.assertTrue(auth.register("siti_01", "Rahasia123", "Rahasia123")[0])
        self.assertTrue(auth.login("siti_01", "Rahasia123")[0])
        self.assertGreaterEqual(len(conns), 2)                                # ada koneksi ulang
        self.assertTrue(conns[0].closed)
        self.assertIn("users.json", storage.list_names())
        storage.delete_json("users.json")
        self.assertIsNone(storage.peek_json("users.json"))
        self.assertEqual(storage.backend_label(), "database")

    def test_T43_database_url(self):
        with self.assertRaises(storage.StorageError):
            storage.PostgresBackend.from_url("mysql://u:p@h/db")
        b = storage.PostgresBackend.from_url("postgresql://user:p%40ss@host.example.com/dbname?sslmode=require")
        self.assertEqual(b.label, "database")                                 # belum terhubung sampai dipakai
        os.environ["DATABASE_URL"] = "postgresql://u:p@h/db"
        storage.reset_backend()
        self.assertEqual(storage.get_backend().label, "database")


# ------------------------------------------------------------------ peran dosen dan akun oleh admin
class TestAkun(Base):
    def test_T44_admin_membuat_akun_dosen_dan_mahasiswa(self):
        ok, msg, pw = auth.create_user(ADMIN, "dosen_01", "dosen")
        self.assertTrue(ok and len(pw) == 12)
        ok, _, user = auth.login("dosen_01", pw)
        self.assertTrue(ok and user["role"] == "dosen" and user["must_change"])
        self.assertTrue(auth.create_user(ADMIN, "mhs_001", "mahasiswa", "Sementara123")[0])
        self.assertTrue(auth.login("mhs_001", "Sementara123")[0])
        self.assertFalse(auth.create_user(ADMIN, "dosen_01", "dosen")[0])               # duplikat
        self.assertFalse(auth.create_user(ADMIN, "abc", "dosen")[0])                    # username pendek
        self.assertFalse(auth.create_user(ADMIN, "dosen_02", "rektor")[0])              # peran tidak valid
        self.assertFalse(auth.create_user(ADMIN, "dosen_02", "dosen", "lemah")[0])      # password lemah
        self.assertFalse(auth.create_user(DOSEN, "dosen_03", "dosen")[0])               # bukan admin
        self.assertFalse(auth.create_user(MHS, "dosen_03", "dosen")[0])

    def test_T45_impor_akun_massal_csv(self):
        csv_text = ("username,role\\nmhs_a01,mahasiswa\\nmhs_a02,\\ndosen_a1,dosen\\nab,mahasiswa\\n"
                    "mhs_a01,mahasiswa\\nmhs_x99,rektor\\n").replace("\\n", "\n")
        ok, msg, rep = auth.import_users_csv(ADMIN, csv_text)
        self.assertTrue(ok)
        self.assertEqual([c[0] for c in rep["created"]], ["mhs_a01", "mhs_a02", "dosen_a1"])
        self.assertEqual([r[0] for r in rep["skipped"]], [5, 6, 7])
        name, role, pw = rep["created"][2]
        self.assertTrue(auth.login(name, pw)[2]["role"] == "dosen")
        self.assertFalse(auth.import_users_csv(DOSEN, csv_text)[0])
        self.assertFalse(auth.import_users_csv(ADMIN, "")[0])
        self.assertFalse(auth.import_users_csv(ADMIN, "nama,peran\nx,y")[0])
        banyak = "username\n" + "\n".join(f"mhs_{i:04d}" for i in range(105))
        rep = auth.import_users_csv(ADMIN, banyak)[2]
        self.assertEqual(len(rep["created"]), auth.MAX_BATCH)                            # dibatasi 100 per impor

    def test_T46_dosen_mengelola_konten_bukan_akun(self):
        self.assertTrue(modules.add_module(DOSEN, DATA)[0])
        mid = modules.list_modules()[-1]["id"]
        self.assertTrue(modules.update_module(DOSEN, mid, dict(DATA, durasi="50"))[0])
        soal = {"q": "Apa itu loop?", "options": ["Perulangan", "Variabel", "Kelas", "Modul"], "answer": 0, "explain": "Loop = perulangan."}
        self.assertTrue(quiz_admin.add_question(DOSEN, "python", soal)[0])
        self.assertTrue(modules.delete_module(DOSEN, mid)[0])
        self.assertFalse(modules.add_module(MHS, DATA)[0])
        self.assertEqual(auth.list_users(DOSEN), [])
        self.assertFalse(auth.reset_password(DOSEN, "admin", "Rahasia123")[0])
        self.assertFalse(auth.delete_user(DOSEN, "admin")[0])
        self.assertFalse(backup.create_backup(DOSEN)[0])
        self.assertFalse(settings.set_registration_open(DOSEN, False)[0])

    def test_T47_ubah_peran_ke_dosen(self):
        auth.register("budi123", "Rahasia123", "Rahasia123")
        self.assertTrue(auth.set_role(ADMIN, "budi123", "dosen")[0])
        self.assertEqual([u["role"] for u in auth.list_users(ADMIN) if u["username"] == "budi123"], ["dosen"])
        self.assertEqual(auth.list_students(), [])

    def test_T48_pendaftaran_mandiri_bisa_ditutup(self):
        self.assertTrue(settings.registration_open())
        self.assertTrue(settings.set_registration_open(ADMIN, False)[0])
        ok, msg = auth.register("budi123", "Rahasia123", "Rahasia123")
        self.assertFalse(ok)
        self.assertIn("ditutup", msg)
        self.assertTrue(auth.create_user(ADMIN, "mhs_001", "mahasiswa")[0])             # admin tetap bisa membuat akun
        self.assertTrue(settings.set_registration_open(ADMIN, True)[0])
        self.assertTrue(auth.register("budi123", "Rahasia123", "Rahasia123")[0])
        self.assertFalse(settings.set_registration_open(MHS, False)[0])

    def test_T49_password_admin_awal_dari_variabel_lingkungan(self):
        shutil.rmtree(self.tmp)
        os.makedirs(self.tmp)
        os.environ["UG_ADMIN_PASSWORD"] = "RahasiaServer9"
        auth.init_data()
        ok, _, user = auth.login("admin", "RahasiaServer9", allow_admin=True)
        self.assertTrue(ok and not user["must_change"])
        self.assertFalse(auth.login("admin", "Admin123", allow_admin=True)[0])
        shutil.rmtree(self.tmp)
        os.makedirs(self.tmp)
        os.environ["UG_ADMIN_PASSWORD"] = "lemah"                                        # terlalu lemah -> pakai bawaan
        auth.init_data()
        ok, _, user = auth.login("admin", "Admin123", allow_admin=True)
        self.assertTrue(ok and user["must_change"])


class TestLangganan(Base):
    def test_T50_langganan_dan_kursus(self):
        self.assertEqual(enrollment.get_info("budi123"), {"plan": None, "courses": []})
        self.assertTrue(enrollment.set_plan("budi123", "pro")[0])
        self.assertFalse(enrollment.set_plan("budi123", "pro")[0])                       # sudah aktif
        self.assertFalse(enrollment.set_plan("budi123", "emas")[0])
        self.assertTrue(enrollment.enroll("budi123", "python")[0])
        self.assertFalse(enrollment.enroll("budi123", "python")[0])
        self.assertFalse(enrollment.enroll("budi123", "cobol")[0])
        info = enrollment.get_info("budi123")
        self.assertEqual((info["plan"], info["courses"]), ("pro", ["python"]))
        auth.register("budi123", "Rahasia123", "Rahasia123")
        self.assertTrue(auth.delete_user(ADMIN, "budi123")[0])                            # data ikut terhapus
        self.assertEqual(enrollment.get_info("budi123"), {"plan": None, "courses": []})

    def test_T51_backup_menyertakan_semua_data_dan_dibatasi_10(self):
        enrollment.enroll("budi123", "sql")
        settings.set_registration_open(ADMIN, False)
        for i in range(12):
            storage.save_json(f"backup_2020010{i % 10}_0000{i:02d}.json", {"created": "x", "files": {"users.json": []}})
        self.assertTrue(backup.create_backup(ADMIN)[0])
        self.assertLessEqual(len(backup.list_backups()), backup.KEEP)
        nama = backup.list_backups()[0]
        enrollment.enroll("budi123", "css")
        settings.set_registration_open(ADMIN, True)
        self.assertTrue(backup.restore_backup(ADMIN, nama)[0])
        self.assertEqual(enrollment.get_info("budi123")["courses"], ["sql"])
        self.assertFalse(settings.registration_open())


class TestCliDosen(Base):
    def test_T52_konsol_untuk_dosen(self):
        ok, _, pw = auth.create_user(ADMIN, "dosen_01", "dosen")
        antrian = iter(["1", "dosen_01", pw,                       # login dengan password sementara
                        pw, "BaruAman123", "BaruAman123",          # wajib ganti password
                        "3", "Modul Dosen CLI", "4", "1", "40", "uji",   # tambah modul
                        "7",                                       # menu dosen hanya 6 butir -> tidak dikenal
                        "9", "0"])
        keluar = []
        cli.run(cli.Console(lambda prompt: next(antrian), keluar.append))
        out = "\n".join(keluar)
        self.assertIn("Menu DOSEN", out)
        self.assertIn("[OK] Modul berhasil ditambahkan", out)
        self.assertIn("Pilihan tidak dikenal", out)
        self.assertNotIn("Log aktivitas", out.split("Menu DOSEN")[1].split("9. Logout")[0])   # menu dosen tanpa log/ekspor


if __name__ == "__main__":
    unittest.main(verbosity=2)
