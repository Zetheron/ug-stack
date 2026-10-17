import flet as ft

from components.live import loading_row, r_doc, r_so, run_in_thread
from components.ui import GREEN, card, green_button, link_text, page_banner, pad, section_heading
from content.languages import LANGS
from content.reference import REFERENCE
from services import web_sources as ws


def get_references_view(page: ft.Page, lang: dict, mobile: bool, on_lang):
    key = lang["key"]
    table = ft.Column(spacing=0)

    def build_rows(keyword=""):
        kw = (keyword or "").strip().lower()
        rows = []
        for syntax, desc in REFERENCE[key]:
            if kw and kw not in syntax.lower() and kw not in desc.lower():
                continue
            rows.append(ft.Container(
                padding=ft.padding.symmetric(horizontal=12, vertical=10),
                border=ft.border.only(bottom=ft.BorderSide(1, ft.colors.with_opacity(0.35, ft.colors.OUTLINE))),
                content=ft.ResponsiveRow([
                    ft.Text(syntax, font_family="monospace", size=13, color="#B31D4D", selectable=True, col={"xs": 12, "md": 5}),
                    ft.Text(desc, size=13, color=ft.colors.ON_SURFACE_VARIANT, col={"xs": 12, "md": 7}),
                ])))
        return rows or [ft.Container(padding=14, content=ft.Text("Tidak ada entri yang cocok.", color=ft.colors.ON_SURFACE_VARIANT))]

    table.controls = build_rows()

    def on_filter(e):
        table.controls = build_rows(e.control.value)
        page.update()

    filter_box = ft.TextField(hint_text=f"Filter cheat sheet {lang['name']}...", prefix_icon=ft.icons.FILTER_LIST,
                              on_change=on_filter, color=ft.colors.ON_SURFACE, border_radius=8)

    chips = ft.Row([ft.ElevatedButton(l["name"], bgcolor=GREEN if l["key"] == key else ft.colors.SURFACE_VARIANT,
                                      color=ft.colors.WHITE if l["key"] == key else ft.colors.BLACK,
                                      on_click=lambda e, k=l["key"]: on_lang(k)) for l in LANGS],
                   wrap=True, spacing=6, run_spacing=6)

    # ---- pencarian lanjutan di web (MDN untuk bahasa web, Stack Overflow untuk lainnya)
    results = ft.Column(spacing=10)
    use_mdn = bool(lang.get("mdn"))
    search_box = ft.TextField(hint_text="Cari topik, mis. flex, async, JOIN..." , color=ft.colors.ON_SURFACE, border_radius=8,
                              expand=True)

    def do_search(e=None):
        q = (search_box.value or "").strip()
        if len(q) < 2:
            page.show_snack("Ketik minimal 2 karakter.")
            return
        results.controls = [loading_row()]
        page.update()

        def work():
            try:
                if use_mdn:
                    data, _ = ws.mdn_search(f"{lang['name']} {q}", 6)
                    results.controls = [r_doc(i) for i in data] or [ft.Text("Tidak ada hasil.", size=12)]
                else:
                    data, _ = ws.stackoverflow_search(q, lang["so"], 6)
                    results.controls = [r_so(i) for i in data] or [ft.Text("Tidak ada hasil.", size=12)]
            except Exception:
                results.controls = [ft.Text("Tidak dapat memuat hasil. Periksa koneksi internet.", size=12, color=ft.colors.RED_700)]
            page.update()
        run_in_thread(page, work)

    search_box.on_submit = do_search
    src_name = "MDN Web Docs" if use_mdn else "Stack Overflow"

    return ft.Column([
        page_banner("Referensi", "Cheat sheet ringkas dan pencarian dokumentasi.", mobile),
        ft.Container(padding=pad(mobile), content=ft.Column([
            chips,
            ft.Text(f"{lang['icon']} {lang['name']} - Cheat Sheet", size=22, weight=ft.FontWeight.BOLD, color=ft.colors.ON_SURFACE),
            filter_box,
            ft.Container(content=table, border=ft.border.all(1, ft.colors.with_opacity(0.35, ft.colors.OUTLINE)), border_radius=8, bgcolor=ft.colors.SURFACE),
            card(ft.Row([ft.Text("📚 Dokumentasi resmi:", size=14, color=ft.colors.ON_SURFACE),
                         link_text(f"{lang['docs_name']} ↗", lang["docs_url"], 14)], wrap=True, spacing=6), bg=ft.colors.PRIMARY_CONTAINER),
            ft.Divider(height=20),
            section_heading(f"Cari lebih dalam di {src_name}"),
            ft.Row([search_box, green_button("Cari", do_search)], spacing=8),
            results,
        ], spacing=14)),
    ], spacing=0, horizontal_alignment=ft.CrossAxisAlignment.STRETCH)
