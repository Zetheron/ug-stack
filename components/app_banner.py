import flet as ft

def create_app_banner(on_tryit_click=None, on_pwa_install=None):
    return ft.Container(
        bgcolor=ft.colors.PRIMARY_CONTAINER,
        padding=35,
        margin=ft.margin.symmetric(vertical=25, horizontal=20),
        border_radius=16,
        content=ft.ResponsiveRow([
            ft.Column([
                ft.Text("UG-Stack Adventure App", size=28, weight=ft.FontWeight.BOLD, color=ft.colors.ON_SURFACE),
                ft.Text(
                    "Learn to code by playing a game! Available on mobile and desktop devices.",
                    size=15, color=ft.colors.ON_SURFACE_VARIANT
                ),
                ft.Container(height=15),
                ft.Row([
                    ft.ElevatedButton(
                        content=ft.Row([ft.Icon(ft.icons.PHONE_IPHONE), ft.Text("App Store")]),
                        bgcolor="#282A35", color=ft.colors.WHITE,
                        on_click=lambda e: on_pwa_install("iOS") if on_pwa_install else None
                    ),
                    ft.ElevatedButton(
                        content=ft.Row([ft.Icon(ft.icons.ANDROID), ft.Text("Google Play")]),
                        bgcolor="#282A35", color=ft.colors.WHITE,
                        on_click=lambda e: on_pwa_install("Android") if on_pwa_install else None
                    ),
                    ft.OutlinedButton(
                        content=ft.Text("Try now in Browser", color=ft.colors.ON_SURFACE),
                        on_click=lambda e: on_tryit_click("HTML") if on_tryit_click else None
                    )
                ], wrap=True, spacing=10)
            ], col={"xs": 12, "md": 8}),
            ft.Column([
                ft.Container(
                    content=ft.Icon(ft.icons.SMARTPHONE, size=100, color="#04AA6D"),
                    alignment=ft.alignment.center
                )
            ], col={"xs": 12, "md": 4})
        ], vertical_alignment=ft.CrossAxisAlignment.CENTER)
    )
