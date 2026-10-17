"""Pengujian konten, quiz/sertifikat, pencarian, dan sumber konten otomatis (tanpa jaringan)."""
import os
import shutil
import tempfile
import time
import unittest

from content.languages import BY_KEY, LANGS, find_lang
from content.lessons import LESSONS
from content.quizzes import QUIZZES
from content.reference import REFERENCE
from services import content_search, quiz, web_sources


class IsolatedStorage(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        os.environ["FLET_APP_STORAGE_DATA"] = self.tmp

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)
        os.environ.pop("FLET_APP_STORAGE_DATA", None)


class TestKonten(unittest.TestCase):
    def test_T18_konten_lengkap_untuk_setiap_bahasa(self):
        for lang in LANGS:
            k = lang["key"]
            self.assertGreaterEqual(len(LESSONS[k]), 4, k)
            self.assertGreaterEqual(len(REFERENCE[k]), 6, k)
            self.assertEqual(len(QUIZZES[k]), 8, k)
            self.assertTrue(lang["docs_url"].startswith("https://"))

    def test_T19_soal_quiz_valid(self):
        for k, qs in QUIZZES.items():
            for q in qs:
                self.assertEqual(len(q["options"]), 4)
                self.assertIn(q["answer"], range(4))
                self.assertTrue(q["explain"])

    def test_T20_find_lang_alias(self):
        self.assertEqual(find_lang("Python Tutorial")["key"], "python")
        self.assertEqual(find_lang("C++")["key"], "cpp")
        self.assertEqual(find_lang("JS Reference")["key"], "javascript")
        self.assertEqual(find_lang("c#")["key"], "csharp")
        self.assertIsNone(find_lang("Rust"))
        self.assertIsNone(find_lang(""))


class TestQuizSertifikat(IsolatedStorage):
    def benar(self, k):
        return [q["answer"] for q in QUIZZES[k]]

    def test_T21_penilaian_quiz(self):
        r = quiz.grade("python", self.benar("python"))
        self.assertEqual((r["correct"], r["percent"], r["passed"]), (8, 100.0, True))
        r = quiz.grade("python", [None] * 8)                 # belum dijawab
        self.assertEqual((r["correct"], r["passed"]), (0, False))
        salah = [(q["answer"] + 1) % 4 for q in QUIZZES["python"]]
        self.assertFalse(quiz.grade("python", salah)["passed"])
        n = len(QUIZZES["python"])
        r = quiz.grade("python", self.benar("python")[:6] + [None] * (n - 6))    # 6/8 = 75% lulus
        self.assertTrue(r["passed"])
        r = quiz.grade("python", self.benar("python")[:5] + [None] * (n - 5))    # 5/8 = 62,5% belum lulus
        self.assertFalse(r["passed"])

    def test_T22_simpan_skor_dan_sertifikat(self):
        self.assertIsNone(quiz.certificate("budi123", "python"))
        quiz.save_result("budi123", "python", quiz.grade("python", [None] * 8))
        self.assertIsNone(quiz.certificate("budi123", "python"))            # gagal: belum ada sertifikat
        quiz.save_result("budi123", "python", quiz.grade("python", self.benar("python")))
        cert = quiz.certificate("budi123", "python")
        self.assertEqual((cert["lang"], cert["score"]), ("Python", 100))
        quiz.save_result("budi123", "python", quiz.grade("python", [None] * 8))   # skor terbaik tidak turun
        self.assertEqual(quiz.get_results("budi123")["python"]["best"], 100)
        self.assertEqual(quiz.get_results("budi123")["python"]["attempts"], 3)

    def test_T23_verifikasi_sertifikat(self):
        quiz.save_result("budi123", "sql", quiz.grade("sql", self.benar("sql")))
        cert = quiz.certificate("budi123", "sql")
        self.assertEqual(quiz.verify_certificate(cert["id"].lower())["username"], "budi123")
        self.assertIsNone(quiz.verify_certificate("ABCDEF1234"))
        self.assertIsNone(quiz.verify_certificate(""))


class TestPencarian(unittest.TestCase):
    def test_T24_pencarian_konten(self):
        r = content_search.search_content("flexbox")
        self.assertTrue(any(x["lang"] == "css" for x in r["lessons"]))
        r = content_search.search_content("python")
        self.assertTrue(any(l["key"] == "python" for l in r["languages"]))
        self.assertEqual(content_search.search_content("zzzxqj"), {"languages": [], "lessons": [], "reference": []})
        self.assertEqual(content_search.search_content("a")["lessons"], [])     # terlalu pendek


class TestSumberKonten(IsolatedStorage):
    def test_T25_parser_semua_sumber(self):
        wiki = web_sources.parse_wikipedia({"title": "Python", "extract": "Kalimat satu. " * 80,
                                            "content_urls": {"desktop": {"page": "https://en.wikipedia.org/wiki/Python"}}})
        self.assertLessEqual(len(wiki["extract"]), 660)
        self.assertEqual(wiki["url"], "https://en.wikipedia.org/wiki/Python")
        so = web_sources.parse_stackoverflow({"items": [{"title": "What&#39;s new?", "link": "u", "score": 5,
                                                         "answer_count": 2, "tags": ["a", "b", "c", "d"]}]})
        self.assertEqual(so[0]["title"], "What's new?")
        self.assertEqual(len(so[0]["tags"]), 3)
        dev = web_sources.parse_devto([{"title": "T", "url": "u", "description": "d", "user": {"name": "N"},
                                        "public_reactions_count": 9, "reading_time_minutes": 3}])
        self.assertEqual((dev[0]["author"], dev[0]["reactions"]), ("N", 9))
        gh = web_sources.parse_github({"items": [{"full_name": "a/b", "description": None, "stargazers_count": 7,
                                                  "html_url": "u", "language": None}]})
        self.assertEqual((gh[0]["desc"], gh[0]["lang"]), ("", ""))
        mdn = web_sources.parse_mdn({"documents": [{"title": "div", "summary": "s", "mdn_url": "/en-US/docs/x"}]})
        self.assertEqual(mdn[0]["url"], "https://developer.mozilla.org/en-US/docs/x")
        ws = web_sources.parse_wiki_search({"pages": [{"title": "Rust", "key": "Rust_(programming_language)",
                                                       "description": None, "excerpt": "a <span>b</span> &amp; c"}]})
        self.assertEqual(ws[0]["desc"], "a b & c")
        self.assertEqual(web_sources.parse_stackoverflow({}), [])                # respons kosong tidak crash

    def test_T26_cache_segar_tidak_memanggil_jaringan(self):
        calls = []
        fetch = lambda: calls.append(1) or {"v": 1}
        self.assertEqual(web_sources.cached("k1", fetch), ({"v": 1}, "live"))
        self.assertEqual(web_sources.cached("k1", fetch), ({"v": 1}, "cache"))
        self.assertEqual(len(calls), 1)

    def test_T27_offline_memakai_cache_lama_atau_gagal(self):
        web_sources.cached("k2", lambda: {"v": 2})
        def mati():
            raise OSError("offline")
        data, status = web_sources.cached("k2", mati, ttl=0)                     # cache kedaluwarsa + offline
        self.assertEqual((data, status), ({"v": 2}, "stale"))
        with self.assertRaises(OSError):
            web_sources.cached("belum-pernah-ada", mati)                          # tanpa cache: error diteruskan


if __name__ == "__main__":
    unittest.main(verbosity=2)
