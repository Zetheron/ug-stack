"""Pencarian di dalam materi bawaan (bahasa, pelajaran, cheat sheet)."""
from content.languages import LANGS
from content.lessons import LESSONS
from content.reference import REFERENCE


def search_content(query: str) -> dict:
    q = (query or "").strip().lower()
    result = {"languages": [], "lessons": [], "reference": []}
    if len(q) < 2:
        return result
    for lang in LANGS:
        if q in lang["name"].lower() or q in lang["tagline"].lower():
            result["languages"].append(lang)
    for key, lessons in LESSONS.items():
        for i, lesson in enumerate(lessons):
            haystack = (lesson["title"] + " " + lesson["body"] + " " + lesson["code"]).lower()
            if q in haystack:
                result["lessons"].append({"lang": key, "index": i, "title": lesson["title"],
                                          "snippet": lesson["body"].split("\n")[0][:110]})
    for key, items in REFERENCE.items():
        for syntax, desc in items:
            if q in syntax.lower() or q in desc.lower():
                result["reference"].append({"lang": key, "syntax": syntax, "desc": desc})
    return result
