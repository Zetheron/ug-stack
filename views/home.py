import flet as ft

from components.app_banner import create_app_banner
from components.code_editor import create_editor_section
from components.course_cards import create_courses_grid
from components.footer import create_footer
from components.hero import create_hero_section
from components.home_extras import live_community_section, snippet_of_the_day
from components.promo_sections import create_career_spaces_sections, create_save_progress_section


def get_home_view(
    page, user=None, progress_text=None, on_tryit_click=None, on_search=None, on_roadmap_click=None,
    on_primary_click=None, on_pwa_install=None, on_select_course=None, on_more_courses=None,
    on_cert_click=None, on_spaces_click=None, on_footer_link=None, on_open_lesson=None
):
    label = "Buka Dashboard" if user else "Create Free Account"
    return ft.Column(
        controls=[
            create_hero_section(on_search=on_search, on_roadmap_click=on_roadmap_click,
                                on_primary_click=on_primary_click, primary_label=label, progress_text=progress_text),
            create_app_banner(on_tryit_click=on_tryit_click, on_pwa_install=on_pwa_install),
            create_editor_section(on_tryit_click=on_tryit_click),
            create_courses_grid(on_select_course=on_select_course, on_more_courses=on_more_courses),
            snippet_of_the_day(page, on_open_lesson, on_tryit_click),
            live_community_section(page),
            create_save_progress_section(on_primary_click=on_primary_click,
                                         primary_label="Buka Dashboard" if user else "Sign Up For Free"),
            create_career_spaces_sections(on_cert_click=on_cert_click, on_spaces_click=on_spaces_click),
            create_footer(on_footer_link=on_footer_link),
        ],
        spacing=0,
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
    )
