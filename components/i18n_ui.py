"""Menerjemahkan seluruh pohon kontrol Flet ke bahasa pilihan (dipanggil sebelum layar diperbarui)."""
from services.i18n import translate

_TEXT_ATTRS = {                                   # nama kelas -> atribut teks yang boleh diterjemahkan
    "Text": ("value",),
    "TextSpan": ("text",),
    "TextField": ("label", "hint_text", "helper_text"),
    "Dropdown": ("label", "hint_text"),
    "Option": ("text",),
    "ElevatedButton": ("text",), "TextButton": ("text",), "OutlinedButton": ("text",), "FilledButton": ("text",),
    "FilledTonalButton": ("text",),
    "Switch": ("label",), "Checkbox": ("label",), "Radio": ("label",),
    "PopupMenuItem": ("text",),
}
_CHILD_LISTS = ("controls", "actions", "items", "options", "spans", "tabs")
_CHILD_SINGLE = ("content", "title", "leading", "subtitle", "trailing")


def _set(obj, attr: str, lang: str) -> None:
    try:
        value = getattr(obj, attr, None)
        if isinstance(value, str) and value:
            new = translate(value, lang)
            if new != value:
                setattr(obj, attr, new)
    except Exception:
        pass                                      # satu atribut yang gagal tidak boleh menghentikan tampilan


def translate_tree(root, lang: str) -> None:
    if root is None:
        return
    seen = set()
    stack = [root]
    while stack:
        c = stack.pop()
        if c is None or isinstance(c, (str, int, float, bool)) or id(c) in seen:
            continue
        seen.add(id(c))
        for attr in _TEXT_ATTRS.get(type(c).__name__, ()):
            _set(c, attr, lang)
        _set(c, "tooltip", lang)
        for attr in _CHILD_LISTS:
            try:
                v = getattr(c, attr, None)
            except Exception:
                v = None
            if isinstance(v, (list, tuple)):
                stack.extend(v)
        for attr in _CHILD_SINGLE:
            try:
                v = getattr(c, attr, None)
            except Exception:
                v = None
            if v is not None and not isinstance(v, str):
                stack.append(v)


def translate_page(page, lang: str) -> None:
    """Terjemahkan semua yang tampil: isi halaman, appbar, dialog, dan overlay (snackbar, dll.)."""
    for root in list(getattr(page, "controls", None) or []):
        translate_tree(root, lang)
    for name in ("appbar", "dialog", "navigation_bar"):
        try:
            translate_tree(getattr(page, name, None), lang)
        except Exception:
            pass
    for root in list(getattr(page, "overlay", None) or []):
        translate_tree(root, lang)
