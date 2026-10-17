import flet as ft


def create_hero_section(on_search=None, on_roadmap_click=None, on_primary_click=None,
                        primary_label="Create Free Account", progress_text=None):
    search_tf = ft.TextField(
        hint_text="Search e.g. Python, HTML, SQL...",
        bgcolor=ft.colors.SURFACE,
        border_radius=25,
        color=ft.colors.ON_SURFACE,
        suffix_icon=ft.icons.SEARCH,
        content_padding=ft.padding.symmetric(horizontal=15, vertical=12),
        on_submit=lambda e: on_search(search_tf.value) if on_search else None
    )

    left_content = ft.Column([
        ft.Text("Learn to Code", size=38, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
        ft.Text(
            "With Gunadarma's largest web developer learning platform.",
            size=16, color="#FFF4A3", weight=ft.FontWeight.W_600
        ),
        ft.Container(height=10),
        search_tf,
        ft.Container(height=5),
        ft.TextButton(
            content=ft.Text(
                "Not Sure Where To Begin?",
                color=ft.colors.WHITE,
                style=ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE)
            ),
            on_click=lambda e: on_roadmap_click() if on_roadmap_click else None
        )
    ], col={"xs": 12, "lg": 7}, spacing=5)

    badge = ft.Container(
        content=ft.Text("PRO FEATURES", size=10, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK),
        bgcolor="#FFF4A3", padding=ft.padding.symmetric(horizontal=6, vertical=3), border_radius=4
    )
    top_row = [badge]
    if progress_text:
        top_row.append(ft.Text(progress_text, color="#00FF66", weight=ft.FontWeight.BOLD, size=12))

    feature = lambda t: ft.Row([ft.Icon(ft.icons.CHECK_CIRCLE, color="#04AA6D", size=16),
                                ft.Text(t, color=ft.colors.WHITE, size=13)])

    pro_card = ft.Container(
        bgcolor="#38444D",
        padding=20,
        border_radius=12,
        col={"xs": 12, "lg": 5},
        content=ft.Column([
            ft.Row(top_row, alignment=ft.MainAxisAlignment.SPACE_BETWEEN, wrap=True),
            ft.Container(height=5),
            ft.Text("Upgrade Your Learning Experience", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
            ft.Divider(color=ft.colors.ON_SURFACE_VARIANT),
            feature("Progress tracking & analytics"),
            feature("Ad-free learning environment"),
            feature("Interactive quizzes & practice"),
            feature("Official UG-Stack Certificates"),
            ft.Container(height=10),
            ft.ElevatedButton(
                primary_label,
                bgcolor="#04AA6D",
                color=ft.colors.WHITE,
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)),
                on_click=lambda e: on_primary_click() if on_primary_click else None
            )
        ], spacing=8)
    )

    return ft.Container(
        bgcolor="#282A35",
        padding=ft.padding.symmetric(vertical=35, horizontal=25),
        content=ft.ResponsiveRow([left_content, pro_card], vertical_alignment=ft.CrossAxisAlignment.CENTER, spacing=20)
    )
