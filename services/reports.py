"""Laporan untuk panel dosen/admin dan ringkasan pribadi mahasiswa."""
from . import algorithms, enrollment, modules, progress, quiz_admin, storage
from .roles import can_manage_content, is_admin

SORT_KEYS = {
    "persen": lambda r: r["percent"],
    "nama": lambda r: r["username"].lower(),
    "sertifikat": lambda r: r["passed"],
    "nilai": lambda r: r["avg_best"],
}


def student_overview(actor, keyword: str = "", sort_by: str = "persen", descending: bool = True) -> list:
    """Satu baris per mahasiswa: progres modul, jumlah sertifikat, rata-rata skor terbaik, paket, kursus.
    Hanya admin/dosen. Difilter menurut nama dan diurutkan dengan merge sort buatan sendiri."""
    if not can_manage_content(actor):
        return []
    module_ids = [m["id"] for m in modules.list_modules()]
    done_by_user = storage.load_json(progress.PROGRESS_FILE, {})
    scores = storage.load_json("scores.json", {})
    plans = storage.load_json(enrollment.ENROLL_FILE, {})
    kw = (keyword or "").strip().lower()
    rows = []
    for user in storage.load_json("users.json", []):
        if user["role"] != "mahasiswa":
            continue
        name = user["username"]
        if kw and kw not in name.lower():
            continue
        done = [i for i in module_ids if i in done_by_user.get(name, [])]
        user_scores = scores.get(name, {})
        best = [rec["best"] for rec in user_scores.values()]
        rows.append({
            "username": name, "percent": progress.percent(done, module_ids), "done": len(done), "total": len(module_ids),
            "passed": len([1 for rec in user_scores.values() if rec.get("passed_at")]), "attempted": len(user_scores),
            "avg_best": sum(best) / len(best) if best else 0.0,
            "plan": plans.get(name, {}).get("plan"), "courses": len(plans.get(name, {}).get("courses", [])),
        })
    return algorithms.merge_sort(rows, key=SORT_KEYS.get(sort_by, SORT_KEYS["persen"]), descending=descending)


def system_stats(actor) -> dict:
    """Ringkasan sistem untuk admin."""
    if not is_admin(actor):
        return {}
    users = storage.load_json("users.json", [])
    scores = storage.load_json("scores.json", {})
    plans = storage.load_json(enrollment.ENROLL_FILE, {})
    by_role = {"admin": 0, "dosen": 0, "mahasiswa": 0}
    for u in users:
        by_role[u["role"]] = by_role.get(u["role"], 0) + 1
    attempts = certs = 0
    for langs in scores.values():
        for rec in langs.values():
            attempts += rec.get("attempts", 0)
            certs += 1 if rec.get("passed_at") else 0
    plan_count = {k: 0 for k in enrollment.PLANS}
    enrolled = 0
    for rec in plans.values():
        if rec.get("plan") in plan_count:
            plan_count[rec["plan"]] += 1
        enrolled += len(rec.get("courses", []))
    return {"users": by_role, "modules": len(modules.list_modules()), "custom_questions": len(quiz_admin.list_custom()),
            "quiz_attempts": attempts, "certificates": certs, "plans": plan_count, "course_enrollments": enrolled}


def student_summary(username: str) -> dict:
    """Ringkasan pribadi: progres, sertifikat, modul berikutnya, dan bahasa dengan skor terendah."""
    all_modules = modules.list_modules()
    ids = [m["id"] for m in all_modules]
    done_ids = progress.get_done(username)
    scores = storage.load_json("scores.json", {}).get(username, {})
    next_module = None
    for m in all_modules:                          # modul pertama yang belum selesai
        if m["id"] not in done_ids:
            next_module = m
            break
    weakest = None
    for key, rec in scores.items():                # skor terbaik terendah di antara quiz yang sudah dicoba dan belum lulus
        if not rec.get("passed_at") and (weakest is None or rec["best"] < scores[weakest]["best"]):
            weakest = key
    return {"percent": progress.percent(done_ids, ids), "done": len([i for i in ids if i in done_ids]), "total": len(ids),
            "passed": len([1 for rec in scores.values() if rec.get("passed_at")]), "attempted": len(scores),
            "next_module": next_module, "weakest_lang": weakest}
