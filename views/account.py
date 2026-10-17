import flet as ft

from components.ui import GREEN
from services import auth


def open_change_password(page: ft.Page, user: dict, forced: bool = False, on_done=None):
    """Dialog ganti password. forced=True: tidak bisa ditutup sebelum berhasil (password sementara)."""
    old = ft.TextField(label="Password lama", password=True, can_reveal_password=True, color=ft.colors.ON_SURFACE, autofocus=True)
    new = ft.TextField(label="Password baru (min. 8, huruf + angka)", password=True, can_reveal_password=True, color=ft.colors.ON_SURFACE)
    conf = ft.TextField(label="Ulangi password baru", password=True, can_reveal_password=True, color=ft.colors.ON_SURFACE)
    msg = ft.Text("", size=13, color=ft.colors.RED_700)
    width = max(250, min(380, (page.width or 400) - 70))

    def save(e=None):
        ok, text = auth.change_password(user["username"], old.value, new.value, conf.value)
        if ok:
            user["must_change"] = False
            page.dialog.open = False
            page.show_snack(text)
            if on_done:
                on_done()
            page.update()
        else:
            msg.value = text
            page.update()

    conf.on_submit = save
    note = "Password Anda masih sementara/bawaan. Ganti sekarang untuk melanjutkan." if forced else "Pilih password baru yang kuat."
    actions = [ft.ElevatedButton("Simpan", bgcolor=GREEN, color=ft.colors.WHITE, on_click=save)]
    if not forced:
        actions.insert(0, ft.TextButton("Batal", on_click=lambda e: (setattr(page.dialog, "open", False), page.update())))
    page.dialog = ft.AlertDialog(
        modal=True, title=ft.Text("Ganti Password"),
        content=ft.Container(width=width, content=ft.Column(
            [ft.Text(note, size=13), old, new, conf, msg], tight=True, scroll=ft.ScrollMode.AUTO)),
        actions=actions)
    page.dialog.open = True
    page.update()
