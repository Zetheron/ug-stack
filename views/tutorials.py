import flet as ft

from components.ui import GREEN, card, chip, green_button, page_banner, pad
from content.languages import LANGS
from content.lessons import LESSONS


def get_tutorials_view(page: ft.Page, mobile: bool, on_open_lang, on_roadmap):
    cards = []
    for l in LANGS:
        cards.append(card(
            col={"xs": 12, "sm": 6, "lg": 4}, padding=0, on_click=lambda e, k=l["key"]: on_open_lang(k),
            content=ft.Column([
                ft.Container(bgcolor=l["color"], padding=16, border_radius=ft.border_radius.only(top_left=12, top_right=12),
                             content=ft.Row([ft.Text(l["icon"], size=28),
                                             ft.Text(f"{l['name']} Tutorial", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE)],
                                            spacing=10)),
                ft.Container(padding=16, content=ft.Column([
                    ft.Text(l["tagline"], size=14, color=ft.colors.ON_SURFACE_VARIANT),
                    ft.Row([chip(l["level"]), chip(l["group"], "#E1F5FE"), chip(f"{len(LESSONS[l['key']])} pelajaran", "#E7F9F0")],
                           wrap=True, spacing=6),
                    green_button("Mulai belajar ❯", lambda e, k=l["key"]: on_open_lang(k)),
                ], spacing=10)),
            ], spacing=0)))
    return ft.Column([
        page_banner("Tutorial UG-Stack", "Pilih bahasa, belajar bertahap, lalu uji dengan quiz.", mobile),
        ft.Container(padding=pad(mobile), content=ft.Column([
            ft.Row([ft.Text("Bingung mulai dari mana?", size=15, color=ft.colors.ON_SURFACE_VARIANT),
                    ft.TextButton("Lihat Roadmap ❯", on_click=lambda e: on_roadmap())], wrap=True),
            ft.ResponsiveRow(cards, spacing=14, run_spacing=14),
        ], spacing=14)),
    ], spacing=0, horizontal_alignment=ft.CrossAxisAlignment.STRETCH)
