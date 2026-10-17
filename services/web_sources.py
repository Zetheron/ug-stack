"""Konten otomatis dari sumber tepercaya lewat API publik + cache lokal 24 jam.

Sumber: Wikipedia, MDN Web Docs, Stack Overflow (Stack Exchange API), DEV Community, GitHub.
Fungsi publik mengembalikan (data, status); status: "live" | "cache" | "stale" (cache lama, saat offline).
Bila gagal dan tidak ada cache, exception dilempar dan UI menampilkan pesan ramah.
"""
import gzip
import html
import json
import re
import time
import urllib.parse
import urllib.request

from . import storage

USER_AGENT = "UG-Stack/1.0 (student learning project)"
TIMEOUT = 6
CACHE_TTL = 24 * 3600


# ------------------------------------------------------------------ HTTP + cache
def http_get_json(url: str, accept: str = "application/json"):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": accept,
                                               "Accept-Encoding": "gzip"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:   # Stack Exchange selalu mengirim gzip
        raw = resp.read()
        if resp.headers.get("Content-Encoding", "").lower() == "gzip":
            raw = gzip.decompress(raw)
    return json.loads(raw.decode("utf-8"))


def _cache_name(key: str) -> str:
    return "cache_" + re.sub(r"[^A-Za-z0-9_.-]", "_", key)[:90] + ".json"


def _cache_read(key: str):
    entry = storage.peek_json(_cache_name(key))
    return entry if isinstance(entry, dict) and "ts" in entry and "data" in entry else None


def _cache_write(key: str, data) -> None:
    try:
        storage.save_json(_cache_name(key), {"ts": time.time(), "data": data})
    except storage.StorageError:
        pass   # cache gagal ditulis tidak boleh mengganggu aplikasi


def cached(key: str, fetcher, ttl: int = CACHE_TTL):
    entry = _cache_read(key)
    if entry and time.time() - entry["ts"] < ttl:
        return entry["data"], "cache"
    try:
        data = fetcher()
    except Exception:
        if entry:
            return entry["data"], "stale"      # offline: pakai cache lama
        raise
    _cache_write(key, data)
    return data, "live"


# ------------------------------------------------------------------ parser (murni, mudah diuji)
def _clip(text: str, limit: int) -> str:
    text = (text or "").strip()
    if len(text) <= limit:
        return text
    cut = text[:limit]
    end = max(cut.rfind(". "), cut.rfind("; "))
    return (cut[: end + 1] if end > limit // 2 else cut.rstrip() + "…")


def _strip_tags(text: str) -> str:
    return html.unescape(re.sub(r"<[^>]+>", "", text or "")).strip()


def parse_wikipedia(d: dict) -> dict:
    url = ((d.get("content_urls") or {}).get("desktop") or {}).get("page", "")
    return {"title": d.get("title", ""), "extract": _clip(d.get("extract", ""), 650), "url": url}


def parse_stackoverflow(d: dict, n: int = 6) -> list:
    out = []
    for i in (d.get("items") or [])[:n]:
        out.append({"title": html.unescape(i.get("title", "")), "url": i.get("link", ""),
                    "score": i.get("score", 0), "answers": i.get("answer_count", 0),
                    "tags": (i.get("tags") or [])[:3]})
    return out


def parse_devto(items: list, n: int = 6) -> list:
    out = []
    for a in (items or [])[:n]:
        out.append({"title": a.get("title", ""), "url": a.get("url", ""), "desc": _clip(a.get("description", ""), 140),
                    "author": (a.get("user") or {}).get("name", ""), "reactions": a.get("public_reactions_count", 0),
                    "minutes": a.get("reading_time_minutes", 0)})
    return out


def parse_github(d: dict, n: int = 6) -> list:
    out = []
    for r in (d.get("items") or [])[:n]:
        out.append({"name": r.get("full_name", ""), "desc": _clip(r.get("description") or "", 130),
                    "stars": r.get("stargazers_count", 0), "url": r.get("html_url", ""), "lang": r.get("language") or ""})
    return out


def parse_mdn(d: dict, n: int = 6) -> list:
    out = []
    for doc in (d.get("documents") or [])[:n]:
        out.append({"title": doc.get("title", ""), "desc": _clip(doc.get("summary", ""), 140),
                    "url": "https://developer.mozilla.org" + doc.get("mdn_url", "")})
    return out


def parse_wiki_search(d: dict, n: int = 4) -> list:
    out = []
    for p in (d.get("pages") or [])[:n]:
        out.append({"title": p.get("title", ""), "desc": p.get("description") or _clip(_strip_tags(p.get("excerpt", "")), 140),
                    "url": "https://en.wikipedia.org/wiki/" + urllib.parse.quote(p.get("key", ""), safe="_()")})
    return out


# ------------------------------------------------------------------ fungsi publik
def wikipedia_summary(title: str):
    url = "https://en.wikipedia.org/api/rest_v1/page/summary/" + urllib.parse.quote(title.replace(" ", "_"), safe="_()")
    return cached(f"wiki_{title}", lambda: parse_wikipedia(http_get_json(url)))


def wikipedia_search(query: str, n: int = 4):
    url = "https://en.wikipedia.org/w/rest.php/v1/search/page?q=" + urllib.parse.quote(query) + f"&limit={n}"
    return cached(f"wikisearch_{query}_{n}", lambda: parse_wiki_search(http_get_json(url), n))


def stackoverflow_top(tag: str, n: int = 6):
    url = ("https://api.stackexchange.com/2.3/questions?order=desc&sort=votes&site=stackoverflow"
           f"&tagged={urllib.parse.quote(tag)}&pagesize={n}")
    return cached(f"so_top_{tag}_{n}", lambda: parse_stackoverflow(http_get_json(url), n))


def stackoverflow_search(query: str, tag: str = None, n: int = 6):
    url = ("https://api.stackexchange.com/2.3/search/advanced?order=desc&sort=relevance&site=stackoverflow"
           f"&q={urllib.parse.quote(query)}&pagesize={n}" + (f"&tagged={urllib.parse.quote(tag)}" if tag else ""))
    return cached(f"so_search_{query}_{tag}_{n}", lambda: parse_stackoverflow(http_get_json(url), n))


def devto_articles(tag: str = None, top: int = 30, n: int = 6):
    url = f"https://dev.to/api/articles?top={top}&per_page={n}" + (f"&tag={urllib.parse.quote(tag)}" if tag else "")
    return cached(f"dev_{tag}_{top}_{n}", lambda: parse_devto(http_get_json(url), n))


def github_repos(query: str, n: int = 6):
    url = ("https://api.github.com/search/repositories?sort=stars&order=desc"
           f"&q={urllib.parse.quote(query, safe=':')}&per_page={n}")
    return cached(f"gh_{query}_{n}", lambda: parse_github(http_get_json(url, "application/vnd.github+json"), n))


def mdn_search(query: str, n: int = 6):
    url = "https://developer.mozilla.org/api/v1/search?q=" + urllib.parse.quote(query) + f"&locale=en-US&size={n}"
    return cached(f"mdn_{query}_{n}", lambda: parse_mdn(http_get_json(url), n))
