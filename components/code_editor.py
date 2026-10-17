import flet as ft

SAMPLES = {
    "HTML": "<!DOCTYPE html>\n<html>\n<head>\n  <title>HTML Tutorial</title>\n</head>\n<body>\n  <h1>This is a Heading</h1>\n  <p>This is a paragraph.</p>\n</body>\n</html>",
    "CSS": "body {\n  background-color: lightblue;\n}\nh1 {\n  color: navy;\n  text-align: center;\n}",
    "JavaScript": "function myFunction() {\n  console.log('Hello from UG-Stack JavaScript!');\n}\nmyFunction();",
    "Python": "def ug_stack_welcome(user):\n    print(f'Selamat Datang {user} di UG-Stack!')\n\nug_stack_welcome('Mahasiswa Gunadarma')",
    "SQL": "SELECT * FROM Customers\nWHERE Country='Indonesia'\nORDER BY CustomerName;"
}

def create_editor_section(on_tryit_click=None):
    code_text = ft.Text(SAMPLES["HTML"], font_family="monospace", color="#00FF66", size=13)
    active_lang = {"value": "HTML"}

    def change_tab(lang):
        active_lang["value"] = lang
        code_text.value = SAMPLES[lang]
        for btn in tab_buttons.controls:
            if btn.text == lang:
                btn.bgcolor = "#04AA6D"
                btn.color = ft.colors.WHITE
            else:
                btn.bgcolor = ft.colors.with_opacity(0.35, ft.colors.OUTLINE)
                btn.color = ft.colors.ON_SURFACE
        code_text.update()
        tab_buttons.update()

    tab_buttons = ft.Row([
        ft.ElevatedButton("HTML", on_click=lambda e: change_tab("HTML"), bgcolor="#04AA6D", color=ft.colors.WHITE),
        ft.ElevatedButton("CSS", on_click=lambda e: change_tab("CSS"), bgcolor=ft.colors.with_opacity(0.35, ft.colors.OUTLINE), color=ft.colors.ON_SURFACE),
        ft.ElevatedButton("JavaScript", on_click=lambda e: change_tab("JavaScript"), bgcolor=ft.colors.with_opacity(0.35, ft.colors.OUTLINE), color=ft.colors.ON_SURFACE),
        ft.ElevatedButton("Python", on_click=lambda e: change_tab("Python"), bgcolor=ft.colors.with_opacity(0.35, ft.colors.OUTLINE), color=ft.colors.ON_SURFACE),
        ft.ElevatedButton("SQL", on_click=lambda e: change_tab("SQL"), bgcolor=ft.colors.with_opacity(0.35, ft.colors.OUTLINE), color=ft.colors.ON_SURFACE),
    ], scroll=ft.ScrollMode.AUTO, spacing=8, alignment=ft.MainAxisAlignment.CENTER)

    return ft.Container(
        bgcolor=ft.colors.SURFACE_VARIANT,
        padding=ft.padding.symmetric(vertical=35, horizontal=20),
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            controls=[
                ft.Text("What do you want to learn?", size=28, weight=ft.FontWeight.BOLD, color=ft.colors.ON_SURFACE, text_align=ft.TextAlign.CENTER),
                ft.Text("Mulai latihan koding interaktif langsung di browser kamu.", color=ft.colors.ON_SURFACE_VARIANT, text_align=ft.TextAlign.CENTER),
                ft.Container(height=10),
                tab_buttons,
                ft.Container(height=15),
                
                ft.Container(
                    bgcolor=ft.colors.SURFACE,
                    border_radius=10,
                    border=ft.border.all(1, ft.colors.with_opacity(0.35, ft.colors.OUTLINE)),
                    padding=20,
                    content=ft.Column(horizontal_alignment=ft.CrossAxisAlignment.STRETCH, controls=[
                        ft.Row([
                            ft.Text("Code Example:", weight=ft.FontWeight.BOLD, size=16, color=ft.colors.ON_SURFACE),
                            ft.Container(expand=True),
                            ft.Icon(ft.icons.CODE, color=ft.colors.ON_SURFACE_VARIANT)
                        ]),
                        ft.Container(
                            bgcolor="#282A35",
                            padding=15,
                            border_radius=6,
                            content=ft.Row([code_text], scroll=ft.ScrollMode.AUTO)
                        ),
                        ft.Container(height=10),
                        ft.Row([
                            ft.ElevatedButton(
                                "Try it Yourself ❯",
                                bgcolor="#04AA6D",
                                color=ft.colors.WHITE,
                                style=ft.ButtonStyle(padding=ft.padding.symmetric(horizontal=25, vertical=15)),
                                on_click=lambda e: on_tryit_click(active_lang["value"]) if on_tryit_click else None
                            )
                        ])
                    ])
                )
            ]
        )
    )
