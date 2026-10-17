import flet as ft

from components.ui import GREEN, card, chip, dark_button, green_button, page_banner, pad, section_heading
from content.languages import LANGS
from services import audit, auth, backup, csv_io, enrollment, quiz_admin, reports, settings
from services.roles import ROLES, is_admin

TABS = [("ringkasan", "🖥️ Ringkasan"), ("laporan", "📊 Mahasiswa"), ("pengguna", "👥 Pengguna"), ("akun", "➕ Buat Akun"),
        ("soal", "📝 Soal Quiz"), ("log", "📜 Log Aktivitas"), ("data", "💾 Data (CSV/Backup)")]
DOSEN_TABS = ("laporan", "soal")      # dosen: laporan mahasiswa dan soal quiz (modul dikelola dari Dashboard)


def allowed_tabs(user: dict) -> list:
    return [k for k, _ in TABS] if is_admin(user) else list(DOSEN_TABS)


def get_admin_view(page: ft.Page, user: dict, tab: str, mobile: bool, on_tab, on_dashboard):
    allowed = allowed_tabs(user)
    if tab not in allowed:
        tab = allowed[0]
    tab_row = ft.Row([ft.ElevatedButton(label, bgcolor=GREEN if key == tab else ft.colors.SURFACE_VARIANT,
                                        color=ft.colors.WHITE if key == tab else ft.colors.BLACK,
                                        on_click=lambda e, k=key: on_tab(k)) for key, label in TABS if key in allowed],
                     wrap=True, spacing=6, run_spacing=6)
    builders = {"ringkasan": _tab_overview, "laporan": _tab_report, "pengguna": _tab_users, "akun": _tab_accounts, "soal": _tab_questions, "log": _tab_logs, "data": _tab_data}
    body = builders[tab](page, user, mobile, lambda: on_tab(tab))
    title = "Panel Admin" if is_admin(user) else "Panel Dosen"
    sub = "Pantau sistem; kelola akun, soal quiz, log aktivitas, dan data." if is_admin(user) else "Pantau progres mahasiswa dan kelola soal quiz."
    return ft.Column([
        page_banner(title, sub, mobile),
        ft.Container(padding=pad(mobile), content=ft.Column([
            ft.Row([dark_button("❮ Dashboard", lambda e: on_dashboard()), ], spacing=8),
            tab_row, body], spacing=14)),
    ], spacing=0, horizontal_alignment=ft.CrossAxisAlignment.STRETCH)


def _dialog(page, title, content, actions):
    page.dialog = ft.AlertDialog(modal=True, title=ft.Text(title), content=content, actions=actions)
    page.dialog.open = True
    page.update()


def _close(page):
    page.dialog.open = False
    page.update()


# ------------------------------------------------------------------ ringkasan sistem (admin)
def _tab_overview(page, user, mobile, refresh):
    st = reports.system_stats(user)
    def stat(label, value):
        return card(ft.Column([ft.Text(str(value), size=28, weight=ft.FontWeight.BOLD, color="#04AA6D"),
                               ft.Text(label, size=12, color=ft.colors.ON_SURFACE_VARIANT)], spacing=2), col={"xs": 6, "md": 3})
    cards = [stat("🎓 Mahasiswa", st["users"]["mahasiswa"]), stat("👨‍🏫 Dosen", st["users"]["dosen"]),
             stat("🛡️ Admin", st["users"]["admin"]), stat("📚 Modul", st["modules"]),
             stat("📝 Soal kustom", st["custom_questions"]), stat("🧪 Percobaan quiz", st["quiz_attempts"]),
             stat("🏅 Sertifikat terbit", st["certificates"]), stat("🎟️ Pendaftaran kursus", st["course_enrollments"])]
    plans = "  •  ".join(f"{name}: {st['plans'][key]}" for key, name in enrollment.PLANS.items())
    return ft.Column([
        section_heading("Ringkasan sistem"), ft.ResponsiveRow(cards, spacing=12, run_spacing=12),
        card(ft.Column([ft.Text("Langganan paket", weight=ft.FontWeight.BOLD), ft.Text(plans, size=13, color=ft.colors.ON_SURFACE_VARIANT)], spacing=4)),
        card(ft.Column([ft.Text("Login admin", weight=ft.FontWeight.BOLD),
                        ft.Text("Admin hanya masuk dengan kode 16 karakter yang berganti setiap 60 detik (tools/admin_generator.html). "
                                "Tidak ada tombol admin di halaman login.", size=13, color=ft.colors.ON_SURFACE_VARIANT)], spacing=4)),
    ], spacing=12)


# ------------------------------------------------------------------ laporan mahasiswa (admin dan dosen)
def _tab_report(page, user, mobile, refresh):
    st = {"kw": "", "sort": "persen", "desc": True}
    list_box = ft.Column(spacing=10)
    count = ft.Text("", size=13, color=ft.colors.ON_SURFACE_VARIANT)

    def load(update=True):
        rows = reports.student_overview(user, st["kw"], st["sort"], st["desc"])
        cards = []
        for r in rows:
            plan = r["plan"] or "-"
            cards.append(card(ft.Column([
                ft.Row([ft.Text(r["username"], size=16, weight=ft.FontWeight.BOLD), chip(f"{r['percent']:.0f}%")], wrap=True, spacing=8),
                ft.ProgressBar(value=r["percent"] / 100, color="#04AA6D", bgcolor=ft.colors.with_opacity(0.35, ft.colors.OUTLINE), height=8),
                ft.Row([ft.Text(f"{r['done']}/{r['total']} modul", size=12), ft.Text(f"🏅 {r['passed']} sertifikat", size=12),
                        ft.Text(f"Skor rata-rata {r['avg_best']:.0f}%", size=12), ft.Text(f"Paket: {plan}", size=12),
                        ft.Text(f"{r['courses']} kursus", size=12)], wrap=True, spacing=14)], spacing=6), padding=12))
        list_box.controls = cards or [ft.Text("Belum ada mahasiswa yang cocok.", size=13, color=ft.colors.ON_SURFACE_VARIANT)]
        count.value = f"{len(rows)} mahasiswa"
        if update:
            page.update()

    def on_filter(e):
        st["kw"] = e.control.value or ""
        load()

    def on_sort(e):
        st["sort"] = e.control.value or "persen"
        load()

    def on_order(e):
        st["desc"] = not st["desc"]
        order_btn.icon = ft.icons.ARROW_DOWNWARD if st["desc"] else ft.icons.ARROW_UPWARD
        load()

    order_btn = ft.IconButton(ft.icons.ARROW_DOWNWARD, tooltip="Naik / turun", on_click=on_order)
    toolbar = ft.ResponsiveRow([
        ft.TextField(hint_text="Cari nama / NPM...", prefix_icon=ft.icons.SEARCH, on_change=on_filter, border_radius=8, col={"xs": 12, "md": 5}),
        ft.Dropdown(label="Urutkan", value="persen", on_change=on_sort, col={"xs": 8, "md": 4},
                    options=[ft.dropdown.Option(key="persen", text="Progres"), ft.dropdown.Option(key="nama", text="Nama"),
                             ft.dropdown.Option(key="sertifikat", text="Sertifikat"), ft.dropdown.Option(key="nilai", text="Skor")]),
        ft.Container(order_btn, col={"xs": 4, "md": 3})], vertical_alignment=ft.CrossAxisAlignment.CENTER)
    load(update=False)
    return ft.Column([section_heading("Progres mahasiswa"), toolbar, count, list_box], spacing=10)


# ------------------------------------------------------------------ pengguna
def _tab_users(page, user, mobile, refresh):
    def on_toggle_registration(e):
        ok, msg = settings.set_registration_open(user, e.control.value)
        page.show_snack(msg)
        refresh()

    reg_switch = ft.Switch(label="Pendaftaran mandiri dibuka (mahasiswa boleh mendaftar sendiri)",
                           value=settings.registration_open(), on_change=on_toggle_registration)
    rows = []
    for u in auth.list_users(user):
        name = u["username"]

        def reset(e, name=name):
            tf = ft.TextField(label="Password sementara (kosongkan = acak)", password=True, can_reveal_password=True,
                              color=ft.colors.ON_SURFACE)
            err = ft.Text("", color=ft.colors.RED_700, size=13)

            def go(e2):
                temp = tf.value.strip() or auth.generate_password()
                ok, msg = auth.reset_password(user, name, temp)
                if ok:
                    _close(page)
                    page.set_clipboard(temp)
                    page.show_snack(f"{msg} Password sementara: {temp} (disalin ke clipboard)")
                else:
                    err.value = msg
                    page.update()
            _dialog(page, f"Reset password {name}", ft.Column([tf, err], tight=True),
                    [ft.TextButton("Batal", on_click=lambda e2: _close(page)), green_button("Reset", go)])

        def change_role(e, name=name):
            ok, msg = auth.set_role(user, name, e.control.value)
            page.show_snack(msg)
            refresh()

        def delete(e, name=name):
            def go(e2):
                ok, msg = auth.delete_user(user, name)
                _close(page)
                page.show_snack(msg)
                refresh()
            _dialog(page, "Hapus pengguna?", ft.Text(f"Akun {name} beserta progres, skor, dan langganannya dihapus permanen."),
                    [ft.TextButton("Batal", on_click=lambda e2: _close(page)),
                     ft.ElevatedButton("Hapus", bgcolor="#E53935", color=ft.colors.WHITE, on_click=go)])

        is_self = name.lower() == user["username"].lower()
        rows.append(card(ft.Column([
            ft.Row([ft.Text(name, size=16, weight=ft.FontWeight.BOLD, color=ft.colors.ON_SURFACE), chip(u["role"].upper()),
                    *([chip("wajib ganti password", "#FFE0B2")] if u["must_change"] else []),
                    ft.Text(f"sejak {u['created_at']}", size=12, color=ft.colors.ON_SURFACE_VARIANT)], wrap=True, spacing=8),
            ft.Row([ft.Dropdown(label="Peran", value=u["role"], width=170, on_change=change_role,
                                options=[ft.dropdown.Option(r) for r in ROLES]),
                    ft.OutlinedButton("Reset password", on_click=reset),
                    ft.OutlinedButton("Hapus", on_click=delete, disabled=is_self)],
                   wrap=True, spacing=8, run_spacing=6, vertical_alignment=ft.CrossAxisAlignment.CENTER)], spacing=8)))
    return ft.Column([section_heading("Pengaturan"), card(reg_switch),
                      section_heading(f"Daftar akun ({len(rows)})"), *rows], spacing=10)


# ------------------------------------------------------------------ buat akun (tunggal dan massal)
def _tab_accounts(page, user, mobile, refresh):
    username = ft.TextField(label="Username (4-20 huruf/angka/_)", color=ft.colors.ON_SURFACE)
    role = ft.Dropdown(label="Peran", value="mahasiswa", options=[ft.dropdown.Option(r) for r in ROLES])
    password = ft.TextField(label="Password sementara (kosongkan = dibuat otomatis)", password=True,
                            can_reveal_password=True, color=ft.colors.ON_SURFACE)
    err = ft.Text("", color=ft.colors.RED_700, size=13)
    result = ft.Column(spacing=6)

    def create(e):
        ok, msg, pw = auth.create_user(user, username.value, role.value, password.value)
        if not ok:
            err.value = msg
            result.controls = []
            page.update()
            return
        err.value = ""
        line = f"Username: {username.value.strip()}  |  Peran: {role.value}  |  Password sementara: {pw}"

        def copy(e2):
            page.set_clipboard(line)
            page.show_snack("Data akun disalin.")
        result.controls = [card(ft.Column([
            ft.Text(msg, size=13, color="#1B7F3B"),
            ft.Text(line, size=13, selectable=True, color=ft.colors.ON_SURFACE, weight=ft.FontWeight.BOLD),
            ft.Row([ft.OutlinedButton("Salin", on_click=copy)]),
            ft.Text("Pengguna wajib mengganti password ini saat pertama login.", size=12, color=ft.colors.ON_SURFACE_VARIANT)],
            spacing=6), bg=ft.colors.PRIMARY_CONTAINER)]
        username.value = ""
        password.value = ""
        page.update()

    batch = ft.TextField(label="Tempel CSV: kolom username dan role (opsional). Contoh:\nusername,role\nmhs_001,mahasiswa\ndosen_01,dosen",
                         multiline=True, min_lines=5, max_lines=10, color=ft.colors.ON_SURFACE)
    batch_result = ft.Column(spacing=6)

    def import_batch(e):
        ok, msg, rep = auth.import_users_csv(user, batch.value)
        if not ok:
            batch_result.controls = [ft.Text(msg, size=13, color=ft.colors.RED_700)]
            page.update()
            return
        lines = [f"{n},{r},{p}" for n, r, p in rep["created"]]

        def copy_all(e2):
            page.set_clipboard("username,role,password_sementara\n" + "\n".join(lines))
            page.show_snack("Daftar akun dan password sementara disalin.")
        batch_result.controls = [
            ft.Text(msg, size=13, color="#1B7F3B"),
            *([ft.Container(padding=10, bgcolor=ft.colors.SURFACE_VARIANT, border_radius=8, content=ft.Text(
                "\n".join(lines), size=12, font_family="monospace", selectable=True, color=ft.colors.ON_SURFACE)),
               ft.Row([green_button("Salin semua (CSV)", copy_all)]),
               ft.Text("Simpan daftar ini sekarang: password sementara tidak ditampilkan lagi.", size=12, color="#C62828")] if lines else []),
            *[ft.Text(f"Baris {n}: {why}", size=12, color="#C62828") for n, why in rep["skipped"][:10]]]
        page.update()

    return ft.Column([
        section_heading("Buat satu akun"),
        card(ft.Column([username, role, password, err, green_button("Buat akun", create)], spacing=8)),
        result,
        section_heading("Buat banyak akun sekaligus (CSV)"),
        card(ft.Column([ft.Text("Cocok untuk satu kelas: password sementara dibuat otomatis untuk setiap akun (maks. 100 per impor).",
                                size=13, color=ft.colors.ON_SURFACE_VARIANT), batch, green_button("Buat akun massal", import_batch), batch_result],
                       spacing=8)),
    ], spacing=10)


# ------------------------------------------------------------------ soal quiz
def _tab_questions(page, user, mobile, refresh):
    lang_dd = ft.Dropdown(label="Bahasa", value="python", options=[ft.dropdown.Option(key=l["key"], text=l["name"]) for l in LANGS])
    q = ft.TextField(label="Pertanyaan", multiline=True, min_lines=2, color=ft.colors.ON_SURFACE)
    opts = [ft.TextField(label=f"Opsi {c}", color=ft.colors.ON_SURFACE) for c in "ABCD"]
    correct = ft.Dropdown(label="Jawaban benar", value="0", options=[ft.dropdown.Option(key=str(i), text=c) for i, c in enumerate("ABCD")])
    explain = ft.TextField(label="Penjelasan jawaban", color=ft.colors.ON_SURFACE)
    err = ft.Text("", color=ft.colors.RED_700, size=13)

    def add(e):
        ok, msg = quiz_admin.add_question(user, lang_dd.value, {"q": q.value, "options": [o.value for o in opts],
                                                                "answer": correct.value, "explain": explain.value})
        if ok:
            page.show_snack(msg); refresh()
        else:
            err.value = msg; page.update()

    custom = quiz_admin.list_custom()
    items = []
    for c in custom:
        def delete(e, c=c):
            ok, msg = quiz_admin.delete_question(user, c["lang"], c["id"])
            page.show_snack(msg); refresh()
        items.append(card(ft.Row([ft.Column([ft.Text(f"[{c['lang']}] {c['q']}", size=13, color=ft.colors.ON_SURFACE),
                                             ft.Text(f"Jawaban: {'ABCD'[c['answer']]}", size=11, color=ft.colors.ON_SURFACE_VARIANT)], spacing=2, expand=True),
                                  ft.IconButton(ft.icons.DELETE, icon_color="#E53935", on_click=delete, tooltip="Hapus")]), padding=10))
    return ft.Column([
        section_heading("Tambah soal quiz"),
        card(ft.Column([lang_dd, q, *opts, correct, explain, err, green_button("Tambah soal", add)], spacing=8)),
        section_heading(f"Soal kustom ({len(custom)})"),
        *(items or [ft.Text("Belum ada soal kustom. Soal bawaan tetap dipakai.", size=13, color=ft.colors.ON_SURFACE_VARIANT)]),
    ], spacing=10)


# ------------------------------------------------------------------ log aktivitas
def _tab_logs(page, user, mobile, refresh):
    st = {"page": 1, "kw": ""}
    list_box = ft.Column(spacing=6)
    info = ft.Text("", size=12, color=ft.colors.ON_SURFACE_VARIANT)
    prev_btn = ft.OutlinedButton("❮ Sebelumnya")
    next_btn = ft.OutlinedButton("Berikutnya ❯")

    def load(update=True):
        entries, pages, total = audit.list_logs(st["page"], 10, st["kw"])
        st["page"] = min(st["page"], pages)
        list_box.controls = [ft.Container(padding=8, bgcolor=ft.colors.SURFACE, border=ft.border.all(1, ft.colors.with_opacity(0.35, ft.colors.OUTLINE)),
                                          border_radius=6, content=ft.Text(
                                              f"{e['time'].replace('T', ' ')}  |  {e['actor']}  |  {e['action']}  |  {e['detail']}",
                                              size=12, color=ft.colors.ON_SURFACE_VARIANT)) for e in entries] or \
                            [ft.Text("Tidak ada entri.", size=13, color=ft.colors.ON_SURFACE_VARIANT)]
        info.value = f"Halaman {st['page']} dari {pages} ({total} entri)"
        prev_btn.disabled = st["page"] <= 1
        next_btn.disabled = st["page"] >= pages
        if update:
            page.update()

    def go_prev(e):
        st["page"] -= 1; load()

    def go_next(e):
        st["page"] += 1; load()

    def on_filter(e):
        st["kw"], st["page"] = e.control.value or "", 1; load()

    prev_btn.on_click, next_btn.on_click = go_prev, go_next
    load(update=False)
    return ft.Column([
        section_heading("Log aktivitas"),
        ft.TextField(hint_text="Filter: LOGIN, MODUL, nama pengguna...", prefix_icon=ft.icons.SEARCH, on_change=on_filter,
                     color=ft.colors.ON_SURFACE, border_radius=8),
        list_box, ft.Row([prev_btn, next_btn, info], wrap=True, spacing=10, vertical_alignment=ft.CrossAxisAlignment.CENTER),
    ], spacing=10)


# ------------------------------------------------------------------ data: CSV dan backup
def _tab_data(page, user, mobile, refresh):
    def export_csv(e):
        ok, path = csv_io.export_to_file()
        page.set_clipboard(csv_io.export_modules_csv())
        page.show_snack(("CSV disalin ke clipboard dan disimpan di: " + path) if ok else path)

    def import_csv(e):
        tf = ft.TextField(label="Tempel isi CSV (kolom: judul,bahasa,level,durasi,deskripsi)", multiline=True, min_lines=6,
                          max_lines=10, color=ft.colors.ON_SURFACE)
        result = ft.Text("", size=12)

        def go(e2):
            ok, msg, report = csv_io.import_modules_csv(user, tf.value)
            lines = [msg] + [f"Baris {n}: {why}" for n, why in (report or {}).get("skipped", [])[:8]]
            result.value = "\n".join(lines)
            result.color = "#1B7F3B" if ok else "#C62828"
            page.update()
        _dialog(page, "Impor modul dari CSV", ft.Container(width=max(250, min(480, (page.width or 500) - 60)),
                                                          content=ft.Column([tf, result], tight=True, scroll=ft.ScrollMode.AUTO)),
                [ft.TextButton("Tutup", on_click=lambda e2: _close(page)), green_button("Impor", go)])

    def make_backup(e):
        ok, msg = backup.create_backup(user)
        page.show_snack(msg); refresh()

    backups = backup.list_backups()
    items = []
    for name in backups[:8]:
        def restore(e, name=name):
            def go(e2):
                ok, msg = backup.restore_backup(user, name)
                _close(page); page.show_snack(msg); refresh()
            _dialog(page, "Pulihkan data?", ft.Text(f"Data saat ini akan diganti dengan backup {name}."),
                    [ft.TextButton("Batal", on_click=lambda e2: _close(page)),
                     ft.ElevatedButton("Pulihkan", bgcolor="#E53935", color=ft.colors.WHITE, on_click=go)])
        items.append(card(ft.Row([ft.Text(name, size=13, color=ft.colors.ON_SURFACE, expand=True),
                                  ft.OutlinedButton("Pulihkan", on_click=restore)]), padding=10))
    return ft.Column([
        section_heading("Ekspor / impor modul (CSV)"),
        card(ft.Row([green_button("Ekspor CSV", export_csv), dark_button("Impor CSV", import_csv)], wrap=True, spacing=8)),
        section_heading("Backup dan pemulihan data"),
        card(ft.Column([ft.Text("Backup menyalin semua berkas data (pengguna, modul, progres, skor, soal kustom, log).",
                                size=13, color=ft.colors.ON_SURFACE_VARIANT), green_button("Buat backup sekarang", make_backup)], spacing=8)),
        *(items or [ft.Text("Belum ada backup.", size=13, color=ft.colors.ON_SURFACE_VARIANT)]),
    ], spacing=10)
