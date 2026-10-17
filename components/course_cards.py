import flet as ft

LOGO_URLS = {
    "HTML": "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/html5/html5-original.svg",
    "CSS": "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/css3/css3-original.svg",
    "JavaScript": "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/javascript/javascript-original.svg",
    "Python": "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/python/python-original.svg",
    "SQL": "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/sqldeveloper/sqldeveloper-original.svg",
    "PHP": "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/php/php-original.svg",
    "jQuery": "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/jquery/jquery-original.svg",
    "Java": "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/java/java-original.svg",
    "C++": "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/cplusplus/cplusplus-original.svg",
    "C#": "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/csharp/csharp-original.svg",
    "React": "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/react/react-original.svg",
    "MySQL": "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/mysql/mysql-original.svg",
}

COURSES = [
    ("HTML", "The building blocks of every webpage", "#D9EEE1"),
    ("CSS", "Style and layout for web pages", "#FFF4A3"),
    ("JavaScript", "Interactive and dynamic web pages", "#E7E9EB"),
    ("Python", "Popular language for web, data & AI", "#F3E5F5"),
    ("SQL", "Query and manage databases", "#E8EAF6"),
    ("PHP", "A web server programming language", "#FFD2D7"),
    ("jQuery", "A JS library for developing web pages", "#E1F5FE"),
    ("Java", "Object-oriented programming language", "#FFF8E1"),
    ("C++", "A powerful general-purpose language", "#E8F5E9"),
    ("C#", "A multi-paradigm programming language", "#F3E5F5"),
    ("React", "Building user interfaces for web", "#E0F7FA"),
    ("MySQL", "Relational database management system", "#E1F5FE"),
]

def create_course_card(title, desc, color_bg, on_select_course=None):
    logo_src = LOGO_URLS.get(title, "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/code/code-original.svg")

    return ft.Container(
        bgcolor=color_bg,
        padding=25,
        border_radius=12,
        col={"xs": 12, "sm": 6, "lg": 3},
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Image(
                    src=logo_src,
                    width=55,
                    height=55,
                    fit=ft.ImageFit.CONTAIN
                ),
                ft.Container(height=5),
                ft.Text(title, size=24, weight=ft.FontWeight.BOLD, color="#212121"),
                ft.Text(desc, text_align=ft.TextAlign.CENTER, color="#424242", size=13),
                ft.Container(height=10),
                ft.ElevatedButton(
                    f"Learn {title}",
                    bgcolor="#282A35",
                    color=ft.colors.WHITE,
                    width=170,
                    on_click=lambda e: on_select_course(title) if on_select_course else None
                )
            ]
        )
    )

def create_courses_grid(on_select_course=None, on_more_courses=None):
    cards = [create_course_card(title, desc, bg, on_select_course) for title, desc, bg in COURSES]
    
    return ft.Container(
        padding=30,
        bgcolor=ft.colors.SURFACE,
        content=ft.Column([
            ft.Text("Popular Courses", size=32, weight=ft.FontWeight.BOLD, color=ft.colors.ON_SURFACE),
            ft.Container(height=15),
            ft.ResponsiveRow(spacing=20, run_spacing=20, controls=cards),
            ft.Container(height=20),
            ft.Container(
                alignment=ft.alignment.center,
                content=ft.ElevatedButton(
                    "And 40+ more ❯",
                    bgcolor="#282A35",
                    color=ft.colors.WHITE,
                    style=ft.ButtonStyle(padding=ft.padding.symmetric(horizontal=30, vertical=15)),
                    on_click=lambda e: on_more_courses() if on_more_courses else None
                )
            )
        ])
    )
