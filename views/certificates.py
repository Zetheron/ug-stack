import flet as ft

from components.ui import DARK, GREEN, card, chip, dark_button, green_button, page_banner, pad
from content.languages import BY_KEY, LANGS
from content.quizzes import PASS_PERCENT
from services import quiz as quiz_service


def get_certificates_view(page: ft.Page, user, mobile: bool, on_login, on_quiz, on_view_cert):
    # ---- verifikasi kode (terbuka untuk siapa saja)
    code_box = ft.TextField(hint_text="Kode verifikasi (10 karakter)", color=ft.colors.ON_SURFACE, border_radius=8, expand=True)
    verdict = ft.Text("", size=13)

    def verify(e=None):
        cert = quiz_service.verify_certificate(code_box.value)
        if cert:
            verdict.value = f"✓ Valid: {cert['username']} lulus quiz {cert['lang']} dengan nilai {cert['score']}% pada {cert['date']}."
            verdict.color = "#1B7F3B"
        else:
            verdict.value = "✗ Kode tidak ditemukan."
            verdict.color = "#C62828"
        page.update()

    code_box.on_submit = verify
    verify_card = card(ft.Column([
        ft.Text("🔎 Verifikasi sertifikat", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.ON_SURFACE),
        ft.Row([code_box, green_button("Periksa", verify)], spacing=8), verdict], spacing=8), bg=ft.colors.PRIMARY_CONTAINER)

    if not user:
        body = [card(ft.Column([
            ft.Text("Login untuk melihat sertifikat Anda", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.ON_SURFACE),
            ft.Text(f"Selesaikan quiz setiap bahasa dengan nilai minimal {PASS_PERCENT}% untuk mendapatkan sertifikat dengan kode verifikasi unik.",
                    size=14, color=ft.colors.ON_SURFACE_VARIANT),
            green_button("Login / Daftar", lambda e: on_login())], spacing=10))]
    else:
        results = quiz_service.get_results(user["username"])
        cards = []
        for l in LANGS:
            rec = results.get(l["key"])
            earned = bool(rec and rec.get("passed_at"))
            cards.append(card(col={"xs": 12, "sm": 6, "lg": 4}, bg=ft.colors.SECONDARY_CONTAINER if earned else ft.colors.WHITE, content=ft.Column([
                ft.Row([ft.Text("🏅" if earned else "🔒", size=24),
                        ft.Text(f"{l['name']} Certificate", size=17, weight=ft.FontWeight.BOLD, color=ft.colors.ON_SURFACE)], spacing=8),
                chip(f"Diperoleh - nilai {rec['best']}%", "#C8E6C9") if earned else
                chip(f"Terbaik {rec['best']}%" if rec else "Belum ada skor", "#EEEEEE"),
                green_button("Lihat sertifikat ❯", lambda e, k=l["key"]: on_view_cert(k)) if earned else
                dark_button("Ikut quiz ❯", lambda e, k=l["key"]: on_quiz(k)),
            ], spacing=8)))
        body = [ft.Text(f"Sertifikat milik {user['username']}", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.ON_SURFACE),
                ft.ResponsiveRow(cards, spacing=14, run_spacing=14)]

    return ft.Column([
        page_banner("Sertifikat", "Bukti kelulusan quiz dengan kode verifikasi unik.", mobile),
        ft.Container(padding=pad(mobile), content=ft.Column([*body, verify_card], spacing=16)),
    ], spacing=0, horizontal_alignment=ft.CrossAxisAlignment.STRETCH)


def get_certificate_detail_view(page: ft.Page, user, lang_key: str, mobile: bool, on_back):
    cert = quiz_service.certificate(user["username"], lang_key) if user else None
    if not cert:
        return ft.Container(padding=pad(mobile), content=ft.Column([
            ft.Text("Sertifikat belum tersedia. Lulus quiz terlebih dahulu.", size=16, color=ft.colors.ON_SURFACE),
            dark_button("❮ Kembali", lambda e: on_back())]))

    def copy(e):
        page.set_clipboard(cert["id"])
        page.show_snack("Kode verifikasi disalin.")

    sheet = ft.Container(
        bgcolor=ft.colors.SURFACE, border=ft.border.all(6, GREEN), border_radius=8,
        padding=ft.padding.symmetric(vertical=30, horizontal=16 if mobile else 50),
        content=ft.Column([
            ft.Text("🏅", size=44),
            ft.Text("SERTIFIKAT KELULUSAN", size=24 if not mobile else 20, weight=ft.FontWeight.BOLD, color=DARK, text_align=ft.TextAlign.CENTER),
            ft.Text("UG-Stack Learning Platform", size=13, color=ft.colors.ON_SURFACE_VARIANT),
            ft.Divider(height=20),
            ft.Text("Diberikan kepada", size=14, color=ft.colors.ON_SURFACE_VARIANT),
            ft.Text(cert["username"], size=32 if not mobile else 26, weight=ft.FontWeight.BOLD, color=GREEN, text_align=ft.TextAlign.CENTER),
            ft.Text(f"telah lulus quiz {cert['lang']} dengan nilai {cert['score']}%", size=16, color=ft.colors.ON_SURFACE, text_align=ft.TextAlign.CENTER),
            ft.Text(f"Tanggal: {cert['date']}", size=13, color=ft.colors.ON_SURFACE_VARIANT),
            ft.Container(height=10),
            ft.Text(f"Kode verifikasi: {cert['id']}", size=14, weight=ft.FontWeight.BOLD, color=DARK, selectable=True),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=6))
    return ft.Column([
        page_banner(f"Sertifikat {cert['lang']}", "", mobile),
        ft.Container(padding=pad(mobile), content=ft.Column([
            sheet,
            ft.Row([green_button("Salin kode verifikasi", copy), dark_button("❮ Semua sertifikat", lambda e: on_back())], wrap=True, spacing=8),
            ft.Text("Kode ini dapat diperiksa di halaman Sertifikat (kolom Verifikasi).", size=12, color=ft.colors.ON_SURFACE_VARIANT),
        ], spacing=14)),
    ], spacing=0, horizontal_alignment=ft.CrossAxisAlignment.STRETCH)
