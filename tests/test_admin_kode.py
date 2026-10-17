"""Pengujian: login admin dengan kode berputar 60 detik, laporan dosen/admin, dan ringkasan mahasiswa."""
import hashlib
import hmac
import os
import shutil
import tempfile
import unittest

from services import admin_code, auth, enrollment, modules, progress, quiz, reports, storage
from content.quizzes import QUIZZES

KEY = "kunci-uji-admin-123"
ADMIN = {"username": "admin", "role": "admin"}
DOSEN = {"username": "dosen_01", "role": "dosen"}
MHS = {"username": "budi123", "role": "mahasiswa"}


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        os.environ["FLET_APP_STORAGE_DATA"] = self.tmp
        os.environ["UG_ADMIN_KEY"] = KEY
        storage.reset_backend()
        auth.init_data()
        auth.reset_lock()
        self.now = 1_800_000_000.0                         # waktu tetap agar pengujian deterministik

    def tearDown(self):
        storage.reset_backend()
        shutil.rmtree(self.tmp, ignore_errors=True)
        os.environ.pop("FLET_APP_STORAGE_DATA", None)
        os.environ.pop("UG_ADMIN_KEY", None)


class TestKodeAdmin(Base):
    def code(self, offset_minutes=0):
        return admin_code.code_for_minute(KEY, int(self.now // 60) + offset_minutes)

    def test_T60_kode_dibuat_dengan_hmac_sha256(self):
        minute = int(self.now // 60)
        expect = hmac.new(KEY.encode(), str(minute).encode(), hashlib.sha256).hexdigest()[:16]
        self.assertEqual(admin_code.current_code(KEY, self.now), expect)
        self.assertEqual(len(expect), 16)
        self.assertNotEqual(self.code(0), self.code(1))                                  # berganti tiap menit
        self.assertEqual(admin_code.seconds_left(self.now + 0), 60 - int(self.now % 60))

    def test_T61_verifikasi_kode_toleransi_dan_sekali_pakai(self):
        ok, msg = admin_code.verify(self.code(0), self.now)
        self.assertTrue(ok, msg)
        ok, msg = admin_code.verify(self.code(0), self.now)                              # dipakai ulang ditolak
        self.assertFalse(ok)
        self.assertIn("sudah dipakai", msg)
        self.assertTrue(admin_code.verify(self.code(-1), self.now)[0])                   # menit sebelumnya masih diterima
        self.assertTrue(admin_code.verify(self.code(1), self.now)[0])                    # menit sesudahnya (selisih jam)
        self.assertFalse(admin_code.verify(self.code(-2), self.now)[0])                  # kedaluwarsa
        self.assertFalse(admin_code.verify(self.code(2), self.now)[0])

    def test_T62_format_kode_dan_url(self):
        c = self.code(0)
        self.assertEqual(admin_code.extract_code(f"https://situs.example/ruang?key={c.upper()}"), c)
        self.assertEqual(admin_code.extract_code(f"  {c}  "), c)
        self.assertTrue(admin_code.verify(f"https://x.test/?key={c}", self.now)[0])      # URL lengkap diterima
        for bad in ("", "abc", "g" * 16, c[:-1], c + "0"):
            self.assertFalse(admin_code.verify(bad, self.now + 600)[0])

    def test_T63_kunci_akun_setelah_5_kode_salah(self):
        for _ in range(5):
            admin_code.verify("0" * 16, self.now)
        ok, msg = admin_code.verify(self.code(0), self.now)                              # kode benar pun ditolak saat terkunci
        self.assertFalse(ok)
        self.assertIn("Coba lagi dalam", msg)
        later = self.now + admin_code.LOCK_SECONDS + 5
        fresh = admin_code.code_for_minute(KEY, int(later // 60))
        self.assertTrue(admin_code.verify(fresh, later)[0])                                # setelah kunci habis, kode baru diterima

    def test_T64_tanpa_kunci_login_admin_nonaktif(self):
        os.environ.pop("UG_ADMIN_KEY")
        original = admin_code._project_root
        admin_code._project_root = lambda: self.tmp                                      # tidak ada admin_key.txt
        try:
            ok, msg = admin_code.verify("0" * 16, self.now)
            self.assertFalse(ok)
            self.assertIn("belum dikonfigurasi", msg)
            new = admin_code.ensure_secret()                                              # pengembangan lokal: kunci dibuat otomatis
            self.assertEqual(len(new), 32)
            self.assertIsNone(admin_code.ensure_secret())                                 # kunci sudah ada
            self.assertEqual(admin_code.get_secret(), new)
            self.assertTrue(admin_code.verify(admin_code.current_code(new, self.now), self.now)[0])
        finally:
            admin_code._project_root = original

    def test_T65_login_admin_hanya_lewat_kode(self):
        self.assertFalse(auth.login("admin", "Admin123")[0])                              # password benar ditolak
        self.assertFalse(auth.login("admin", "Admin123", expected_role="admin")[0])
        ok, msg, user = auth.login_admin("admin", self.code(0), self.now)
        self.assertTrue(ok and user["role"] == "admin" and not user["must_change"])
        self.assertFalse(auth.login_admin("admin", self.code(0), self.now)[0])                      # kode sama tidak bisa dipakai dua kali
        auth.create_user(ADMIN, "dosen_01", "dosen", "Dosen12345")
        ok, msg, _ = auth.login_admin("dosen_01", self.code(1), self.now)                           # bukan akun admin
        self.assertFalse(ok)
        self.assertIn("tidak ditemukan", msg)
        ok, _, _ = auth.login_admin("", self.code(-1), self.now)                                    # username kosong = "admin"
        self.assertTrue(ok)


class TestLaporan(Base):
    def seed(self):
        auth.register("budi123", "Rahasia123", "Rahasia123")
        auth.register("siti_01", "Rahasia123", "Rahasia123")
        auth.register("andi_02", "Rahasia123", "Rahasia123")
        ids = [m["id"] for m in modules.list_modules()]
        progress.toggle_done("budi123", ids[0])
        progress.toggle_done("budi123", ids[1])
        progress.toggle_done("siti_01", ids[0])
        benar = [q["answer"] for q in QUIZZES["python"]]
        quiz.save_result("budi123", "python", quiz.grade("python", benar))
        quiz.save_result("siti_01", "sql", quiz.grade("sql", [None] * len(QUIZZES["sql"])))
        enrollment.set_plan("budi123", "pro")
        enrollment.enroll("budi123", "python")

    def test_T66_laporan_mahasiswa_untuk_dosen_dan_admin(self):
        self.seed()
        rows = reports.student_overview(DOSEN)
        self.assertEqual([r["username"] for r in rows], ["budi123", "siti_01", "andi_02"])   # persen menurun
        budi = rows[0]
        self.assertEqual((budi["done"], budi["passed"], budi["plan"], budi["courses"]), (2, 1, "pro", 1))
        self.assertAlmostEqual(budi["percent"], 100 * 2 / budi["total"])
        self.assertEqual([r["username"] for r in reports.student_overview(ADMIN, sort_by="nama", descending=False)],
                         ["andi_02", "budi123", "siti_01"])
        self.assertEqual([r["username"] for r in reports.student_overview(ADMIN, keyword="SIT")], ["siti_01"])
        self.assertEqual(reports.student_overview(MHS), [])                                  # mahasiswa tidak boleh
        self.assertEqual(reports.student_overview(DOSEN, sort_by="tidak-ada")[0]["username"], "budi123")

    def test_T67_statistik_sistem_hanya_admin(self):
        self.seed()
        self.assertEqual(reports.system_stats(DOSEN), {})
        st = reports.system_stats(ADMIN)
        self.assertEqual(st["users"], {"admin": 1, "dosen": 0, "mahasiswa": 3})
        self.assertEqual((st["certificates"], st["quiz_attempts"], st["course_enrollments"]), (1, 2, 1))
        self.assertEqual(st["plans"]["pro"], 1)

    def test_T68_ringkasan_pribadi_mahasiswa(self):
        self.seed()
        s = reports.student_summary("budi123")
        self.assertEqual((s["done"], s["passed"], s["attempted"]), (2, 1, 1))
        self.assertEqual(s["next_module"]["id"], modules.list_modules()[2]["id"])            # modul berikutnya yang belum selesai
        self.assertIsNone(s["weakest_lang"])                                                  # Python sudah lulus
        self.assertEqual(reports.student_summary("siti_01")["weakest_lang"], "sql")          # quiz belum lulus = perlu diulang
        self.assertIsNone(reports.student_summary("tidak_ada")["next_module"] and None)


if __name__ == "__main__":
    unittest.main(verbosity=2)
