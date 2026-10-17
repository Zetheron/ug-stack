"""Komponen UI bersama bergaya UG-Stack (hijau #04AA6D, gelap #282A35)."""
import flet as ft

GREEN = "#04AA6D"
DARK = "#282A35"
LIGHT_GREEN = ft.colors.PRIMARY_CONTAINER
SIDEBAR = ft.colors.SURFACE_VARIANT


def pad(mobile: bool) -> int:
    return 12 if mobile else 30


def link_text(text: str, url: str, size: int = 13, color: str = GREEN) -> ft.Text:
    """Teks tautan yang bisa membungkus baris (aman untuk judul panjang)."""
    return ft.Text(spans=[ft.TextSpan(text, ft.TextStyle(color=color, decoration=ft.TextDecoration.UNDERLINE), url=url)],
                   size=size)


def chip(text: str, bg: str = "#FFF4A3", fg: str = ft.colors.BLACK) -> ft.Container:
    return ft.Container(ft.Text(text, size=11, weight=ft.FontWeight.BOLD, color=fg), bgcolor=bg,
                        padding=ft.padding.symmetric(horizontal=8, vertical=3), border_radius=10)


def page_banner(title: str, subtitle: str = "", mobile: bool = False, accent: str = GREEN) -> ft.Container:
    return ft.Container(
        bgcolor=DARK, padding=ft.padding.symmetric(vertical=28 if not mobile else 20, horizontal=pad(mobile)),
        content=ft.Column([
            ft.Text(title, size=30 if not mobile else 24, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
            ft.Container(width=60, height=4, bgcolor=accent, border_radius=2),
            ft.Text(subtitle, size=14, color="#C8CCD4") if subtitle else ft.Container(),
        ], spacing=8))


def section_heading(text: str) -> ft.Text:
    return ft.Text(text, size=20, weight=ft.FontWeight.BOLD, color=ft.colors.ON_SURFACE)


def green_button(text: str, on_click, **kw) -> ft.ElevatedButton:
    return ft.ElevatedButton(text, bgcolor=GREEN, color=ft.colors.WHITE, on_click=on_click, **kw)


def dark_button(text: str, on_click, **kw) -> ft.ElevatedButton:
    return ft.ElevatedButton(text, bgcolor=DARK, color=ft.colors.WHITE, on_click=on_click, **kw)


def card(content, col=None, bg=ft.colors.SURFACE, padding=16, on_click=None) -> ft.Container:
    return ft.Container(content=content, col=col, bgcolor=bg, padding=padding, border_radius=12,
                        border=ft.border.all(1, ft.colors.with_opacity(0.35, ft.colors.OUTLINE)), on_click=on_click,
                        ink=bool(on_click))


def code_block(page: ft.Page, code: str, title: str = "Contoh kode") -> ft.Container:
    def copy(e):
        page.set_clipboard(code)
        page.show_snack("Kode disalin ke clipboard.")

    return ft.Container(
        bgcolor="#1E1F26", border_radius=8, padding=ft.padding.only(left=14, right=6, top=2, bottom=12),
        content=ft.Column([
            ft.Row([ft.Text(title, size=11, color="#9AA0A6"),
                    ft.IconButton(ft.icons.COPY, icon_size=16, icon_color="#9AA0A6", tooltip="Salin kode", on_click=copy)],
                   alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Row([ft.Text(code, font_family="monospace", size=13, color="#E6E6E6", selectable=True)],
                   scroll=ft.ScrollMode.AUTO),
        ], spacing=0))
