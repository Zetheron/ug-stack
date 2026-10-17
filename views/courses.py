import flet as ft

from components.ui import GREEN, card, chip, dark_button, green_button, page_banner, pad
from content.languages import BY_KEY
from content.lessons import LESSONS
from content.quizzes import PASS_PERCENT
from services import enrollment

COURSE_KEYS = ["html", "css", "javascript", "python", "sql", "react"]


def get_paid_courses_view(page: ft.Page, user, mobile: bool, on_login, on_changed, on_open_lang):
    mine = enrollment.get_info(user["username"])["courses"] if user else []

    def join(key):
        if not user:
            page.show_snack("Login terlebih dahulu untuk mendaftar kursus.")
            on_login()
            return
        ok, msg = enrollment.enroll(user["username"], key)
        page.show_snack(msg)
        if ok:
            on_changed()

    cards = []
    for key in COURSE_KEYS:
        lang = BY_KEY[key]
        joined = key in mine
        cards.append(card(col={"xs": 12, "sm": 6, "lg": 4}, content=ft.Column([
            ft.Row([ft.Text(lang["icon"], size=30), ft.Text(f"Kursus {lang['name']}", size=19, weight=ft.FontWeight.BOLD,
                                                           color=ft.colors.ON_SURFACE, expand=True)], spacing=10),
            ft.Text(lang["tagline"], size=13, color=ft.colors.ON_SURFACE_VARIANT),
            ft.Row([chip(lang["level"]), chip(f"{len(LESSONS[key])} pelajaran", "#E7F9F0"),
                    chip(f"quiz lulus {PASS_PERCENT}%", "#E1F5FE")], wrap=True, spacing=6),
            ft.Text("Gratis (demo kampus)", size=16, weight=ft.FontWeight.BOLD, color=GREEN),
            ft.Row([ft.ElevatedButton("✓ Terdaftar", disabled=True) if joined else green_button("Daftar kursus", lambda e, k=key: join(k)),
                    dark_button("Mulai belajar ❯", lambda e, k=key: on_open_lang(k))], wrap=True, spacing=8),
        ], spacing=8)))
    note = (f"Anda terdaftar di {len(mine)} kursus." if user else "Login untuk mendaftar kursus.")
    return ft.Column([
        page_banner("Kursus Lengkap", "Setiap kursus berisi pelajaran, quiz, dan sertifikat berkode verifikasi.", mobile),
        ft.Container(padding=pad(mobile), content=ft.Column([
            ft.Text(note, size=14, color=ft.colors.ON_SURFACE_VARIANT),
            ft.ResponsiveRow(cards, spacing=16, run_spacing=16),
        ], spacing=14)),
    ], spacing=0, horizontal_alignment=ft.CrossAxisAlignment.STRETCH)
