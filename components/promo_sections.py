import flet as ft

def create_save_progress_section(on_primary_click=None, primary_label="Sign Up For Free"):
    return ft.Container(
        bgcolor=ft.colors.PRIMARY_CONTAINER,
        padding=40,
        margin=ft.margin.symmetric(vertical=20),
        content=ft.ResponsiveRow([
            ft.Column([
                ft.Text("Save your progress. Everywhere.", size=32, weight=ft.FontWeight.BOLD, color=ft.colors.ON_SURFACE),
                ft.Text("Create a free account to track your progress, score points, and log in from anywhere.", color=ft.colors.ON_SURFACE_VARIANT),
                ft.Container(height=10),
                ft.Row([ft.Icon(ft.icons.CHECK, color="#04AA6D"), ft.Text("Track your progress", color=ft.colors.ON_SURFACE)]),
                ft.Row([ft.Icon(ft.icons.CHECK, color="#04AA6D"), ft.Text("Earn free certificates", color=ft.colors.ON_SURFACE)]),
                ft.Row([ft.Icon(ft.icons.CHECK, color="#04AA6D"), ft.Text("Access interactive quizzes", color=ft.colors.ON_SURFACE)]),
            ], col={"xs": 12, "md": 7}),
            ft.Column([
                ft.Container(
                    bgcolor=ft.colors.SURFACE,
                    padding=25,
                    border_radius=10,
                    content=ft.Column([
                        ft.Text("Start in one click", weight=ft.FontWeight.BOLD, size=18, color=ft.colors.ON_SURFACE),
                        ft.Text("Login atau daftar untuk membuka dashboard modul dan progres belajar.", size=13, color=ft.colors.ON_SURFACE_VARIANT),
                        ft.ElevatedButton(
                            primary_label,
                            bgcolor="#04AA6D",
                            color=ft.colors.WHITE,
                            on_click=lambda e: on_primary_click() if on_primary_click else None
                        )
                    ])
                )
            ], col={"xs": 12, "md": 5})
        ], vertical_alignment=ft.CrossAxisAlignment.CENTER)
    )

def create_career_spaces_sections(on_cert_click=None, on_spaces_click=None):
    career_card = ft.Container(
        bgcolor=ft.colors.SURFACE_VARIANT,
        padding=30,
        border_radius=12,
        col={"xs": 12, "md": 6},
        content=ft.Column([
            ft.Text("Kickstart your career", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.ON_SURFACE),
            ft.Text("Get certified by completing a course today!", color=ft.colors.ON_SURFACE_VARIANT),
            ft.Container(height=15),
            ft.Row([
                ft.ElevatedButton(
                    "Get Certified", 
                    bgcolor="#04AA6D", 
                    color=ft.colors.WHITE,
                    on_click=lambda e: on_cert_click() if on_cert_click else None
                ),
                ft.Icon(ft.icons.VERIFIED, size=50, color="#04AA6D")
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        ])
    )

    spaces_card = ft.Container(
        bgcolor="#282A35",
        padding=30,
        border_radius=12,
        col={"xs": 12, "md": 6},
        content=ft.Column([
            ft.Text("Build and host websites", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
            ft.Text("Create your own website with UG-Stack Spaces.", color=ft.colors.with_opacity(0.35, ft.colors.OUTLINE)),
            ft.Container(height=15),
            ft.ElevatedButton(
                "Try Spaces", 
                bgcolor="#04AA6D", 
                color=ft.colors.WHITE,
                on_click=lambda e: on_spaces_click() if on_spaces_click else None
            )
        ])
    )

    return ft.Container(
        padding=ft.padding.symmetric(horizontal=20, vertical=10),
        content=ft.ResponsiveRow([career_card, spaces_card], spacing=20)
    )
