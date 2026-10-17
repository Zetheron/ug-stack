from datetime import date

import flet as ft

from components.live import community_feed
from components.ui import GREEN, card, chip, code_block, green_button, section_heading
from content.languages import BY_KEY
from content.lessons import LESSONS


def snippet_of_the_day(page, on_open_lesson, on_tryit):
    """Pilih satu contoh kode berdasarkan tanggal (berganti setiap hari)."""
    items = [(k, i, l) for k, ls in LESSONS.items() for i, l in enumerate(ls)]
    key, idx, lesson = items[date.today().toordinal() % len(items)]
    lang = BY_KEY[key]
    return ft.Container(
        padding=ft.padding.symmetric(horizontal=20, vertical=10),
        content=card(ft.Column([
            ft.Row([ft.Text("💡 Kode Hari Ini", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.ON_SURFACE),
                    chip(lang["name"]), chip(lesson["title"], "#E7F9F0")], wrap=True, spacing=8),
            code_block(page, lesson["code"], f"{lang['name']} - {lesson['title']}"),
            ft.Row([green_button("Try it Yourself ❯", lambda e: on_tryit(lang["name"], lesson["code"])),
                    ft.TextButton("Pelajari pelajarannya ❯", on_click=lambda e: on_open_lesson(key, idx))], wrap=True, spacing=8),
        ], spacing=10), bg=ft.colors.SURFACE_VARIANT))


def live_community_section(page):
    return ft.Container(
        padding=ft.padding.symmetric(horizontal=20, vertical=20),
        content=ft.Column([
            section_heading("🔥 Sedang Ramai di Komunitas Developer"),
            ft.Text("Diambil langsung dari DEV Community dan GitHub, diperbarui otomatis.", size=13, color=ft.colors.ON_SURFACE_VARIANT),
            community_feed(page),
        ], spacing=10))
