import re
import flet as ft

LANG_TEMPLATES = {
    "HTML": "<!DOCTYPE html>\n<html>\n<head>\n  <style>\n    body { font-family: Arial, sans-serif; padding: 20px; }\n    h1 { color: #04AA6D; }\n  </style>\n</head>\n<body>\n  <h1>Heading UG-Stack</h1>\n  <p>Selamat mencoba Tryit Editor UG-Stack!</p>\n</body>\n</html>",
    "CSS": "/* CSS Style UG-Stack */\nbody {\n  background-color: #E7F9F0;\n  color: #282A35;\n  padding: 25px;\n}\nh1 {\n  border-bottom: 2px solid #04AA6D;\n}",
    "JavaScript": "// JavaScript Interactive Engine\nfunction hitung(a, b) {\n  return a + b;\n}\nconsole.log('Hasil 10 + 20 = ' + hitung(10, 20));",
    "Python": "# Python Runner UG-Stack\ndef sapa_mahasiswa(nama, prodi):\n    return f'Halo {nama} dari prodi {prodi}! Selamat belajar di UG-Stack.'\n\nprint(sapa_mahasiswa('Dzakwan', 'Informatika'))",
    "SQL": "-- SQL Query Playground\nSELECT user_id, username, status \nFROM users \nWHERE role = 'Student' \nORDER BY user_id DESC;"
}

def get_tryit_view(page: ft.Page, default_lang="HTML", on_back=None, code=None):
    current_code = code or LANG_TEMPLATES.get(default_lang, LANG_TEMPLATES["HTML"])

    code_input = ft.TextField(
        value=current_code,
        multiline=True,
        min_lines=12,
        font_family="monospace",
        text_size=13,
        bgcolor="#F9F9F9",
        border_color=ft.colors.with_opacity(0.35, ft.colors.OUTLINE),
        color=ft.colors.ON_SURFACE
    )

    preview_output = ft.Column([
        ft.Text("Hasil Eksekusi Output:", weight=ft.FontWeight.BOLD, color="#04AA6D", size=15),
        ft.Divider(),
        ft.Text("Tekan 'Run ❯' untuk melihat output.", size=13, color=ft.colors.ON_SURFACE_VARIANT)
    ])

    def run_code(e):
        text = code_input.value
        preview_output.controls.clear()
        preview_output.controls.append(ft.Text("Hasil Eksekusi Output:", weight=ft.FontWeight.BOLD, color="#04AA6D", size=15))
        preview_output.controls.append(ft.Divider())

        if "<h1>" in text and "</h1>" in text:
            h1_text = text.split("<h1>")[1].split("</h1>")[0]
            preview_output.controls.append(ft.Text(h1_text, size=20, weight=ft.FontWeight.BOLD, color="#04AA6D"))
        if "<p>" in text and "</p>" in text:
            p_text = text.split("<p>")[1].split("</p>")[0]
            preview_output.controls.append(ft.Text(p_text, size=14, color=ft.colors.ON_SURFACE_VARIANT))
        
        if "print(" in text:
            matches = re.findall(r'print\((.*?)\)', text)
            for m in matches:
                cleaned = m.strip().strip("\"'")
                preview_output.controls.append(
                    ft.Container(
                        bgcolor="#282A35",
                        padding=8,
                        border_radius=5,
                        content=ft.Text(f"> {cleaned}", font_family="monospace", color="#00FF66", size=13)
                    )
                )

        if len(preview_output.controls) <= 2:
            preview_output.controls.append(
                ft.Container(
                    bgcolor="#282A35",
                    padding=10,
                    border_radius=5,
                    content=ft.Text(f"[Status 200 OK] Program {default_lang} Berhasil Dijalankan!", font_family="monospace", color="#00FF66", size=12)
                )
            )

        page.update()

    top_bar = ft.Container(
        bgcolor="#282A35",
        padding=10,
        content=ft.Row([
            ft.ElevatedButton("❮ Kembali", on_click=lambda e: on_back() if on_back else None, bgcolor=ft.colors.GREY_700, color=ft.colors.WHITE),
            ft.ElevatedButton("Run ❯", on_click=run_code, bgcolor="#04AA6D", color=ft.colors.WHITE),
            ft.Container(expand=True),
            ft.Text(f"Mode: {default_lang}", color=ft.colors.WHITE, size=12, weight="bold"),
        ])
    )

    editor_pane = ft.Container(
        col={"xs": 12, "md": 6},
        padding=10,
        content=ft.Column([
            ft.Text(f"Source Code ({default_lang}):", weight=ft.FontWeight.BOLD, color=ft.colors.ON_SURFACE),
            code_input
        ])
    )

    preview_pane = ft.Container(
        col={"xs": 12, "md": 6},
        padding=15,
        bgcolor=ft.colors.SURFACE,
        border=ft.border.all(1, ft.colors.with_opacity(0.35, ft.colors.OUTLINE)),
        border_radius=8,
        content=preview_output
    )

    return ft.Column([
        top_bar,
        ft.Container(
            padding=10,
            content=ft.ResponsiveRow([editor_pane, preview_pane], spacing=10)
        )
    ], horizontal_alignment=ft.CrossAxisAlignment.STRETCH, spacing=0)
