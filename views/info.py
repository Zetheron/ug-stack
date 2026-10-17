import flet as ft

from components.ui import card, dark_button, page_banner, pad
from content.pages import INFO


def get_info_view(page: ft.Page, key: str, mobile: bool, on_home):
    info = INFO.get(key) or INFO["tentang"]
    return ft.Column([
        page_banner(info["title"], "", mobile),
        ft.Container(padding=pad(mobile), content=ft.Column([
            *[card(ft.Column([ft.Text(h, size=18, weight=ft.FontWeight.BOLD, color=ft.colors.ON_SURFACE),
                              ft.Text(t, size=14, color=ft.colors.ON_SURFACE_VARIANT)], spacing=6)) for h, t in info["sections"]],
            ft.Row([dark_button("❮ Beranda", lambda e: on_home())]),
        ], spacing=12)),
    ], spacing=0, horizontal_alignment=ft.CrossAxisAlignment.STRETCH)
