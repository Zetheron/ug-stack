import flet as ft

from components.live import r_doc, r_so, r_wiki, source_panel
from components.ui import card, chip, green_button, page_banner, pad, section_heading
from content.languages import BY_KEY
from services import web_sources as ws
from services.content_search import search_content

SUGGESTIONS = ["flexbox", "list comprehension", "JOIN", "pointer", "useState", "async", "class", "array"]


def get_search_view(page: ft.Page, query: str, mobile: bool, on_search, on_open_lang, on_open_lesson, on_open_ref):
    box = ft.TextField(value=query or "", hint_text="Cari bahasa, konsep, atau sintaks...", prefix_icon=ft.icons.SEARCH,
                       color=ft.colors.ON_SURFACE, border_radius=8, expand=True, autofocus=not query)
    box.on_submit = lambda e: on_search(box.value)
    bar = ft.Row([box, green_button("Cari", lambda e: on_search(box.value))], spacing=8)

    controls = [bar]
    q = (query or "").strip()
    if len(q) < 2:
        controls.append(ft.Text("Coba cari:", size=13, color=ft.colors.ON_SURFACE_VARIANT))
        controls.append(ft.Row([ft.OutlinedButton(s, on_click=lambda e, s=s: on_search(s)) for s in SUGGESTIONS], wrap=True, spacing=6, run_spacing=6))
    else:
        res = search_content(q)
        total = len(res["languages"]) + len(res["lessons"]) + len(res["reference"])
        controls.append(ft.Text(f"{total} hasil di materi UG-Stack untuk \"{q}\"", size=14, color=ft.colors.ON_SURFACE_VARIANT))
        if res["languages"]:
            controls.append(section_heading("Bahasa"))
            controls.append(ft.Row([green_button(f"{l['icon']} {l['name']}", lambda e, k=l["key"]: on_open_lang(k)) for l in res["languages"]], wrap=True, spacing=6))
        if res["lessons"]:
            controls.append(section_heading("Pelajaran"))
            for r in res["lessons"][:8]:
                controls.append(card(ft.Column([
                    ft.Row([chip(BY_KEY[r["lang"]]["name"]), ft.Text(r["title"], size=15, weight=ft.FontWeight.BOLD, color=ft.colors.ON_SURFACE)], wrap=True, spacing=8),
                    ft.Text(r["snippet"], size=12, color=ft.colors.ON_SURFACE_VARIANT)], spacing=4),
                    on_click=lambda e, r=r: on_open_lesson(r["lang"], r["index"])))
        if res["reference"]:
            controls.append(section_heading("Cheat sheet"))
            for r in res["reference"][:8]:
                controls.append(card(ft.Row([chip(BY_KEY[r["lang"]]["name"]),
                                             ft.Text(r["syntax"], font_family="monospace", size=12, color="#B31D4D"),
                                             ft.Text(r["desc"], size=12, color=ft.colors.ON_SURFACE_VARIANT)], wrap=True, spacing=8),
                                     padding=10, on_click=lambda e, r=r: on_open_ref(r["lang"])))
        if total == 0:
            controls.append(ft.Text("Tidak ada hasil di materi bawaan. Lihat hasil dari web di bawah.", size=13, color=ft.colors.ON_SURFACE_VARIANT))
        controls.append(ft.Divider(height=20))
        controls.append(section_heading("Dari web (sumber tepercaya)"))
        controls.append(ft.ResponsiveRow([
            source_panel(page, "Wikipedia", "📖", "Wikipedia", "https://www.wikipedia.org",
                         lambda: ws.wikipedia_search(q, 4), r_doc, "Tidak ada artikel."),
            source_panel(page, "Stack Overflow", "💬", "Stack Overflow", "https://stackoverflow.com",
                         lambda: ws.stackoverflow_search(q, None, 6), r_so, "Tidak ada pertanyaan."),
        ], spacing=14, run_spacing=14))

    return ft.Column([
        page_banner("Pencarian", "Cari di materi UG-Stack dan sumber tepercaya di web.", mobile),
        ft.Container(padding=pad(mobile), content=ft.Column(controls, spacing=12)),
    ], spacing=0, horizontal_alignment=ft.CrossAxisAlignment.STRETCH)
