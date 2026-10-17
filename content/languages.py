"""Katalog bahasa + metadata sumber konten tepercaya (dokumentasi resmi, Wikipedia, dll.)."""

LANGS = [
    dict(key="html", name="HTML", color="#E44D26", icon="🌐", level="Pemula", group="Web",
         tagline="Kerangka dan struktur halaman web.", wiki="HTML", so="html", dev="html", gh="language:html",
         docs_name="MDN Web Docs", docs_url="https://developer.mozilla.org/en-US/docs/Web/HTML", mdn=True),
    dict(key="css", name="CSS", color="#264DE4", icon="🎨", level="Pemula", group="Web",
         tagline="Warna, tata letak, dan tampilan halaman.", wiki="CSS", so="css", dev="css", gh="language:css",
         docs_name="MDN Web Docs", docs_url="https://developer.mozilla.org/en-US/docs/Web/CSS", mdn=True),
    dict(key="javascript", name="JavaScript", color="#F0B90B", icon="⚡", level="Pemula", group="Web",
         tagline="Membuat halaman web interaktif.", wiki="JavaScript", so="javascript", dev="javascript",
         gh="language:javascript", docs_name="MDN Web Docs",
         docs_url="https://developer.mozilla.org/en-US/docs/Web/JavaScript", mdn=True),
    dict(key="python", name="Python", color="#3776AB", icon="🐍", level="Pemula", group="Umum",
         tagline="Bahasa serbaguna: web, data, AI, otomasi.", wiki="Python (programming language)", so="python",
         dev="python", gh="language:python", docs_name="Dokumentasi Python",
         docs_url="https://docs.python.org/3/tutorial/", mdn=False),
    dict(key="sql", name="SQL", color="#00758F", icon="🗄️", level="Pemula", group="Data",
         tagline="Bahasa standar untuk mengelola basis data.", wiki="SQL", so="sql", dev="sql", gh="topic:sql",
         docs_name="PostgreSQL Docs", docs_url="https://www.postgresql.org/docs/current/sql.html", mdn=False),
    dict(key="java", name="Java", color="#E76F00", icon="☕", level="Menengah", group="Umum",
         tagline="Bahasa berorientasi objek untuk aplikasi skala besar.", wiki="Java (programming language)",
         so="java", dev="java", gh="language:java", docs_name="Oracle Java Tutorials",
         docs_url="https://docs.oracle.com/javase/tutorial/", mdn=False),
    dict(key="php", name="PHP", color="#777BB4", icon="🐘", level="Pemula", group="Web",
         tagline="Bahasa sisi server untuk membangun situs dinamis.", wiki="PHP", so="php", dev="php",
         gh="language:php", docs_name="PHP Manual", docs_url="https://www.php.net/manual/en/", mdn=False),
    dict(key="c", name="C", color="#5C6BC0", icon="🔧", level="Menengah", group="Sistem",
         tagline="Dasar pemrograman sistem dan memori.", wiki="C (programming language)", so="c", dev="c",
         gh="language:c", docs_name="cppreference (C)", docs_url="https://en.cppreference.com/w/c", mdn=False),
    dict(key="cpp", name="C++", color="#00599C", icon="⚙️", level="Menengah", group="Sistem",
         tagline="C dengan OOP dan pustaka standar yang kaya.", wiki="C++", so="c++", dev="cpp",
         gh='language:"c++"', docs_name="cppreference (C++)", docs_url="https://en.cppreference.com/w/cpp", mdn=False),
    dict(key="csharp", name="C#", color="#68217A", icon="🎯", level="Menengah", group="Umum",
         tagline="Bahasa modern untuk .NET, game (Unity), dan desktop.", wiki="C Sharp (programming language)",
         so="c#", dev="csharp", gh='language:"c#"', docs_name="Microsoft Learn (C#)",
         docs_url="https://learn.microsoft.com/en-us/dotnet/csharp/", mdn=False),
    dict(key="react", name="React", color="#0E9FBC", icon="⚛️", level="Menengah", group="Web",
         tagline="Pustaka UI berbasis komponen dari JavaScript.", wiki="React (software)", so="reactjs", dev="react",
         gh="topic:react", docs_name="react.dev", docs_url="https://react.dev/learn", mdn=False),
    dict(key="mysql", name="MySQL", color="#00618A", icon="🐬", level="Menengah", group="Data",
         tagline="Sistem basis data relasional paling populer.", wiki="MySQL", so="mysql", dev="mysql",
         gh="topic:mysql", docs_name="MySQL Reference Manual", docs_url="https://dev.mysql.com/doc/refman/8.0/en/",
         mdn=False),
]

BY_KEY = {l["key"]: l for l in LANGS}
_ALIASES = {"js": "javascript", "c++": "cpp", "c#": "csharp", "reactjs": "react", "react.js": "react",
            "front end": "html", "frontend": "html"}
_SUFFIXES = (" tutorial", " reference", " examples", " example", " certificate", " quiz")


def find_lang(name):
    """Cari bahasa dari nama bebas ("Python Tutorial", "JS", "C++", "JAVASCRIPT"). None bila tidak ada."""
    if not name:
        return None
    n = name.strip().lower()
    for s in _SUFFIXES:
        if n.endswith(s):
            n = n[: -len(s)].strip()
    n = _ALIASES.get(n, n)
    if n in BY_KEY:
        return BY_KEY[n]
    for l in LANGS:
        if l["name"].lower() == n:
            return l
    return None
