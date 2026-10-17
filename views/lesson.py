import flet as ft

from components.live import language_live_section
from components.ui import (DARK, GREEN, SIDEBAR, card, chip, code_block, dark_button, green_button, link_text,
                           pad, section_heading)
from content.lessons import LESSONS


def get_lesson_view(page: ft.Page, lang: dict, idx: int, mobile: bool, on_lesson, on_tryit, on_quiz, on_reference):
    key = lang["key"]
    lessons = LESSONS[key]
    idx = max(0, min(idx, len(lessons) - 1))
    lesson = lessons[idx]
    last = idx == len(lessons) - 1

    hero = ft.Container(
        bgcolor=DARK, padding=ft.padding.symmetric(vertical=22, horizontal=pad(mobile)),
        content=ft.Row([
            ft.Container(ft.Text(lang["icon"], size=34), bgcolor=lang["color"], width=62, height=62, border_radius=12,
                         alignment=ft.alignment.center),
            ft.Column([
                ft.Text(f"{lang['name']} Tutorial", size=26 if not mobile else 22, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                ft.Text(lang["tagline"], size=13, color="#C8CCD4"),
                ft.Row([chip(lang["level"]), chip(f"{len(lessons)} pelajaran", "#E7F9F0")], spacing=6, wrap=True),
            ], spacing=4, expand=True),
        ], spacing=14))

    # ---- sidebar daftar pelajaran (desktop) / dropdown (HP)
    if mobile:
        side = ft.Dropdown(
            label="Pelajaran", value=str(idx), col={"xs": 12},
            options=[ft.dropdown.Option(key=str(i), text=f"{i + 1}. {l['title']}") for i, l in enumerate(lessons)],
            on_change=lambda e: on_lesson(key, int(e.control.value)))
        sidebar = ft.Container(col={"xs": 12, "md": 3}, content=side)
    else:
        rows = [ft.Text(f"{lang['name']} Tutorial", weight=ft.FontWeight.BOLD, size=16, color=ft.colors.ON_SURFACE)]
        for i, l in enumerate(lessons):
            active = i == idx
            rows.append(ft.Container(
                ft.Text(f"{i + 1}. {l['title']}", size=13, color=ft.colors.WHITE if active else ft.colors.BLACK,
                        weight=ft.FontWeight.BOLD if active else ft.FontWeight.NORMAL),
                bgcolor=GREEN if active else None, padding=ft.padding.symmetric(horizontal=10, vertical=8),
                border_radius=6, ink=True, on_click=lambda e, i=i: on_lesson(key, i)))
        rows += [ft.Divider(height=10),
                 ft.TextButton("📋 Cheat sheet", on_click=lambda e: on_reference(key)),
                 ft.TextButton("📝 Quiz & sertifikat", on_click=lambda e: on_quiz(key))]
        sidebar = ft.Container(col={"xs": 12, "md": 3}, bgcolor=SIDEBAR, padding=14, border_radius=10,
                               content=ft.Column(rows, spacing=4))

    nav_row = ft.Row([
        dark_button("❮ Sebelumnya", lambda e: on_lesson(key, idx - 1), disabled=idx == 0),
        green_button("Ikut Quiz ❯" if last else "Selanjutnya ❯",
                     (lambda e: on_quiz(key)) if last else (lambda e: on_lesson(key, idx + 1))),
    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    paragraphs = [ft.Text(p, size=15, color=ft.colors.ON_SURFACE_VARIANT) for p in lesson["body"].split("\n\n")]
    main = ft.Container(col={"xs": 12, "md": 9}, content=ft.Column([
        ft.Text(f"Pelajaran {idx + 1} dari {len(lessons)}", size=12, color=ft.colors.ON_SURFACE_VARIANT),
        ft.Text(lesson["title"], size=28 if not mobile else 24, weight=ft.FontWeight.BOLD, color=ft.colors.ON_SURFACE),
        *paragraphs,
        code_block(page, lesson["code"], f"Contoh {lang['name']}"),
        ft.Row([green_button("Try it Yourself ❯", lambda e: on_tryit(lang["name"], lesson["code"]))]),
        ft.Divider(height=20),
        nav_row,
    ], spacing=12))

    docs = card(ft.Row([ft.Text("📚 Dokumentasi resmi:", size=14, color=ft.colors.ON_SURFACE),
                        link_text(f"{lang['docs_name']} ↗", lang["docs_url"], 14)], wrap=True, spacing=6), bg=ft.colors.PRIMARY_CONTAINER)

    return ft.Column([
        hero,
        ft.Container(padding=pad(mobile), content=ft.Column([
            ft.ResponsiveRow([sidebar, main], spacing=20, run_spacing=14),
            docs,
            ft.Divider(height=30),
            section_heading("Diperkaya otomatis dari sumber tepercaya"),
            ft.Text("Bagian ini dimuat langsung dari Wikipedia, MDN, Stack Overflow, DEV Community, dan GitHub.",
                    size=13, color=ft.colors.ON_SURFACE_VARIANT),
            language_live_section(page, lang),
        ], spacing=14)),
    ], spacing=0, horizontal_alignment=ft.CrossAxisAlignment.STRETCH)
