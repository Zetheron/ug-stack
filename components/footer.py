import flet as ft

def create_footer(on_footer_link=None):
    def make_link(text):
        return ft.TextButton(
            content=ft.Text(text, color=ft.colors.GREY_400, size=13),
            on_click=lambda e: on_footer_link(text) if on_footer_link else None,
            style=ft.ButtonStyle(padding=0)
        )

    return ft.Container(
        bgcolor="#282A35",
        padding=40,
        content=ft.Column([
            ft.ResponsiveRow([
                ft.Column([
                    ft.Text("Top Tutorials", weight=ft.FontWeight.BOLD, color=ft.colors.WHITE, size=16),
                    make_link("Python Tutorial"),
                    make_link("HTML Tutorial"),
                    make_link("CSS Tutorial"),
                    make_link("JavaScript Tutorial"),
                    make_link("SQL Tutorial"),
                ], col={"xs": 6, "md": 3}),
                
                ft.Column([
                    ft.Text("Top References", weight=ft.FontWeight.BOLD, color=ft.colors.WHITE, size=16),
                    make_link("Python Reference"),
                    make_link("HTML Reference"),
                    make_link("CSS Reference"),
                    make_link("JS Reference"),
                ], col={"xs": 6, "md": 3}),
                
                ft.Column([
                    ft.Text("Top Examples", weight=ft.FontWeight.BOLD, color=ft.colors.WHITE, size=16),
                    make_link("Python Examples"),
                    make_link("HTML Examples"),
                    make_link("CSS Examples"),
                ], col={"xs": 6, "md": 3}),
                
                ft.Column([
                    ft.Text("Get Certified", weight=ft.FontWeight.BOLD, color=ft.colors.WHITE, size=16),
                    make_link("HTML Certificate"),
                    make_link("Python Certificate"),
                    make_link("Front End Certificate"),
                ], col={"xs": 6, "md": 3}),
            ], run_spacing=20),
            
            ft.Divider(color=ft.colors.GREY_800, height=40),
            
            ft.Row([
                ft.IconButton(ft.icons.PUBLIC, icon_color=ft.colors.WHITE, tooltip="Website Utama", on_click=lambda e: on_footer_link("Website UG-Stack") if on_footer_link else None),
                ft.IconButton(ft.icons.CAMERA_ALT, icon_color=ft.colors.WHITE, tooltip="Instagram", on_click=lambda e: on_footer_link("Instagram Official") if on_footer_link else None),
                ft.IconButton(ft.icons.CHAT, icon_color=ft.colors.WHITE, tooltip="Komunitas Discord", on_click=lambda e: on_footer_link("Discord Community") if on_footer_link else None),
                ft.IconButton(ft.icons.WORK, icon_color=ft.colors.WHITE, tooltip="LinkedIn Profile", on_click=lambda e: on_footer_link("LinkedIn") if on_footer_link else None),
            ], alignment=ft.MainAxisAlignment.CENTER),
            
            ft.Row([
                ft.Text("© 2026 UG-Stack. Platform Edukasi Koding Berbasis Full Python (Flet).", color=ft.colors.GREY_500, size=13, text_align=ft.TextAlign.CENTER),
            ], alignment=ft.MainAxisAlignment.CENTER)
        ])
    )
