import flet as ft

from content.languages import LANGS

NAV_ITEMS = [
    ("Tutorials", "tutorials"), ("References", "references"), ("Exercises", "exercises"),
    ("Certificates", "certificates"), ("Roadmap", "roadmap"), ("Upgrade", "upgrade"), ("Paid Courses", "paid_courses"),
]


def create_header(page: ft.Page, user=None, mobile=False, active_nav=None, active_lang=None,
                  dark=False, ui_lang="id", on_theme_toggle=None, on_lang_toggle=None, on_nav_click=None, on_lang_click=None, on_search_click=None, on_home_click=None,
                  on_login_click=None, on_dashboard_click=None, on_logout_click=None):
    def call(fn, *args):
        return fn(*args) if fn else None

    logo = ft.Container(
        content=ft.IconButton(icon=ft.icons.CODE, icon_color="#04AA6D", icon_size=26,
                              on_click=lambda e: call(on_home_click), tooltip="UG-Stack Home"),
        padding=ft.padding.only(left=5))
    search_btn = ft.IconButton(ft.icons.SEARCH, icon_color=ft.colors.WHITE, tooltip="Cari",
                               on_click=lambda e: call(on_search_click))
    theme_btn = ft.IconButton(ft.icons.LIGHT_MODE if dark else ft.icons.DARK_MODE, icon_color=ft.colors.WHITE,
                              tooltip="Tema terang" if dark else "Tema gelap", on_click=lambda e: call(on_theme_toggle))
    lang_btn = ft.TextButton(content=ft.Text("EN" if ui_lang == "id" else "ID", color=ft.colors.WHITE, weight=ft.FontWeight.BOLD),
                             tooltip="Switch to English" if ui_lang == "id" else "Ganti ke Bahasa Indonesia",
                             on_click=lambda e: call(on_lang_toggle))

    if mobile:
        items = [ft.PopupMenuItem(text=label, on_click=lambda e, k=key: call(on_nav_click, k)) for label, key in NAV_ITEMS]
        if user:
            items.append(ft.PopupMenuItem(text="Dashboard", icon=ft.icons.DASHBOARD, on_click=lambda e: call(on_dashboard_click)))
            items.append(ft.PopupMenuItem(text="Logout", icon=ft.icons.LOGOUT, on_click=lambda e: call(on_logout_click)))
        else:
            items.append(ft.PopupMenuItem(text="Login / Daftar", icon=ft.icons.LOGIN, on_click=lambda e: call(on_login_click)))
        title = ft.Text("UG-Stack", color=ft.colors.WHITE, weight=ft.FontWeight.BOLD, size=18)
        actions = [lang_btn, theme_btn, search_btn, ft.PopupMenuButton(icon=ft.icons.MENU, icon_color=ft.colors.WHITE, items=items)]
    else:
        def nav_button(label, key):
            if key == "paid_courses":
                return ft.ElevatedButton(label, bgcolor="#9B51E0", color=ft.colors.WHITE,
                                         style=ft.ButtonStyle(padding=ft.padding.symmetric(horizontal=10, vertical=5)),
                                         on_click=lambda e: call(on_nav_click, key))
            active = key == active_nav
            return ft.TextButton(
                content=ft.Text(label, color="#04AA6D" if active else ft.colors.WHITE, size=13,
                                weight=ft.FontWeight.BOLD if active else ft.FontWeight.NORMAL),
                on_click=lambda e, k=key: call(on_nav_click, k))

        title = ft.Row([nav_button(l, k) for l, k in NAV_ITEMS], spacing=4, scroll=ft.ScrollMode.AUTO)
        if user:
            actions = [lang_btn, theme_btn, search_btn,
                       ft.TextButton(content=ft.Text(f"👤 {user['username']}", color=ft.colors.WHITE, size=13),
                                     on_click=lambda e: call(on_dashboard_click)),
                       ft.IconButton(ft.icons.LOGOUT, icon_color=ft.colors.WHITE, tooltip="Logout",
                                     on_click=lambda e: call(on_logout_click))]
        else:
            actions = [lang_btn, theme_btn, search_btn,
                       ft.ElevatedButton("Login", bgcolor="#04AA6D", color=ft.colors.WHITE, on_click=lambda e: call(on_login_click)),
                       ft.Container(width=8)]

    sub_buttons = [
        ft.TextButton(
            content=ft.Text(l["name"].upper(), color="#04AA6D" if l["key"] == active_lang else ft.colors.WHITE,
                            size=12, weight=ft.FontWeight.BOLD),
            on_click=lambda e, k=l["key"]: call(on_lang_click, k),
            style=ft.ButtonStyle(padding=ft.padding.symmetric(horizontal=8)))
        for l in LANGS]
    sub_nav = ft.Container(bgcolor="#1D2A35", padding=ft.padding.symmetric(horizontal=10, vertical=3),
                           content=ft.Row(sub_buttons, scroll=ft.ScrollMode.AUTO, spacing=2))

    appbar = ft.AppBar(leading=logo, title=title, center_title=False, bgcolor="#282A35", actions=actions)
    return appbar, sub_nav
