"""Penyimpanan data JSON dengan beberapa backend (satu antarmuka, tiga tempat penyimpanan).

 - FileBackend           : berkas JSON di folder data (pengembangan lokal / desktop)
 - ClientStorageBackend  : penyimpanan perangkat Flet (SharedPreferences) -> dipakai di APK agar data awet
 - PostgresBackend       : tabel key-value di PostgreSQL (mis. Neon) -> dipakai di server online (DATABASE_URL)

Semua service hanya memakai load_json / save_json, sehingga backend bisa diganti tanpa mengubah logika.
"""
import copy
import json
import os
import ssl
import tempfile
import threading
import urllib.parse


class StorageError(Exception):
    """Kesalahan saat membaca/menulis data."""


# Kunci untuk operasi baca-ubah-tulis. Aplikasi web melayani banyak sesi sekaligus,
# jadi bagian kritis di service dibungkus: with storage.LOCK: ...
LOCK = threading.RLock()


# ====================================================================== backend berkas
def _writable(path: str) -> bool:
    try:
        os.makedirs(path, exist_ok=True)
        probe = tempfile.NamedTemporaryFile(dir=path, delete=True)
        probe.close()
        return True
    except OSError:
        return False


def get_data_dir() -> str:
    """Urutan: FLET_APP_STORAGE_DATA (Flet >= 0.25) -> folder data proyek -> folder rumah pengguna."""
    env = os.getenv("FLET_APP_STORAGE_DATA")
    if env:
        base = env
    else:
        base = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
        if not _writable(base):
            base = os.path.join(os.path.expanduser("~"), ".ugstack_data")
    try:
        os.makedirs(base, exist_ok=True)
    except OSError as e:
        raise StorageError(f"Folder data tidak dapat dibuat: {e}")
    return base


class FileBackend:
    label = "berkas"

    def read(self, name: str):
        path = os.path.join(get_data_dir(), name)
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            return None
        except OSError as e:
            raise StorageError(f"Gagal membaca {name}: {e}")

    def write(self, name: str, text: str) -> None:
        path = os.path.join(get_data_dir(), name)
        tmp = path + ".tmp"
        try:
            with open(tmp, "w", encoding="utf-8") as f:
                f.write(text)
            os.replace(tmp, path)          # tulis atomik supaya file tidak setengah jadi
        except OSError as e:
            raise StorageError(f"Gagal menyimpan {name}: {e}")

    def delete(self, name: str) -> None:
        try:
            os.remove(os.path.join(get_data_dir(), name))
        except FileNotFoundError:
            pass
        except OSError as e:
            raise StorageError(f"Gagal menghapus {name}: {e}")

    def names(self) -> list:
        try:
            return [n for n in os.listdir(get_data_dir()) if n.endswith(".json")]
        except OSError as e:
            raise StorageError(str(e))


# ====================================================================== backend penyimpanan perangkat (APK)
class ClientStorageBackend:
    """Membungkus page.client_storage milik Flet (SharedPreferences di Android, localStorage di web)."""
    label = "penyimpanan perangkat"
    PREFIX = "ugstack:"

    def __init__(self, client_storage):
        self.cs = client_storage

    def read(self, name: str):
        try:
            value = self.cs.get(self.PREFIX + name)
        except Exception as e:
            raise StorageError(f"Gagal membaca {name}: {e}")
        if value is None:
            return None
        return value if isinstance(value, str) else json.dumps(value)

    def write(self, name: str, text: str) -> None:
        try:
            self.cs.set(self.PREFIX + name, text)
        except Exception as e:
            raise StorageError(f"Gagal menyimpan {name}: {e}")

    def delete(self, name: str) -> None:
        try:
            self.cs.remove(self.PREFIX + name)
        except Exception as e:
            raise StorageError(f"Gagal menghapus {name}: {e}")

    def names(self) -> list:
        try:
            return [k[len(self.PREFIX):] for k in self.cs.get_keys(self.PREFIX)]
        except Exception as e:
            raise StorageError(str(e))


# ====================================================================== backend PostgreSQL (server)
class PostgresBackend:
    """Tabel key-value ug_kv(name, data). `connect` mengembalikan objek dengan .run(sql, **param) dan .close()."""
    label = "database"

    def __init__(self, connect):
        self._connect = connect
        self._con = None
        self._ready = False
        self._lock = threading.RLock()

    def _run(self, sql: str, **params):
        with self._lock:
            last = None
            for _ in range(2):                           # coba ulang sekali bila koneksi terputus
                try:
                    if self._con is None:
                        self._con = self._connect()
                        self._ready = False
                    if not self._ready:
                        self._con.run("CREATE TABLE IF NOT EXISTS ug_kv (name TEXT PRIMARY KEY, data TEXT NOT NULL, "
                                      "updated_at TIMESTAMPTZ DEFAULT now())")
                        self._ready = True
                    return self._con.run(sql, **params)
                except Exception as e:                   # koneksi mati / Neon sedang bangun
                    last = e
                    try:
                        if self._con is not None:
                            self._con.close()
                    except Exception:
                        pass
                    self._con = None
            raise StorageError(f"Database tidak dapat diakses: {last}")

    def read(self, name: str):
        rows = self._run("SELECT data FROM ug_kv WHERE name = :n", n=name)
        return rows[0][0] if rows else None

    def write(self, name: str, text: str) -> None:
        self._run("INSERT INTO ug_kv (name, data) VALUES (:n, :d) "
                  "ON CONFLICT (name) DO UPDATE SET data = EXCLUDED.data, updated_at = now()", n=name, d=text)

    def delete(self, name: str) -> None:
        self._run("DELETE FROM ug_kv WHERE name = :n", n=name)

    def names(self) -> list:
        return [r[0] for r in self._run("SELECT name FROM ug_kv")]

    @classmethod
    def from_url(cls, url: str):
        u = urllib.parse.urlparse(url)
        if u.scheme not in ("postgres", "postgresql") or not u.hostname:
            raise StorageError("DATABASE_URL tidak valid (harus postgresql://user:password@host/database).")
        query = urllib.parse.parse_qs(u.query)
        use_ssl = query.get("sslmode", ["require"])[0] != "disable"

        def connect():
            import pg8000.native                          # pustaka murni Python; hanya dimuat bila DATABASE_URL dipakai
            return pg8000.native.Connection(
                user=urllib.parse.unquote(u.username or ""), password=urllib.parse.unquote(u.password or ""),
                host=u.hostname, port=u.port or 5432, database=(u.path or "/").lstrip("/"),
                ssl_context=ssl.create_default_context() if use_ssl else None, timeout=15)
        return cls(connect)


# ====================================================================== pemilihan backend
_backend = None


def set_backend(backend) -> None:
    global _backend
    _backend = backend


def reset_backend() -> None:
    set_backend(None)


def get_backend():
    global _backend
    if _backend is None:
        url = os.getenv("DATABASE_URL")
        _backend = PostgresBackend.from_url(url) if url else FileBackend()
    return _backend


def backend_label() -> str:
    return get_backend().label


# ====================================================================== antarmuka JSON
def save_json(name: str, data) -> None:
    text = json.dumps(data, ensure_ascii=False, indent=2)
    with LOCK:
        get_backend().write(name, text)


def load_json(name: str, default):
    with LOCK:
        backend = get_backend()
        text = backend.read(name)
        if text is None:
            save_json(name, default)
            return copy.deepcopy(default)
        try:
            return json.loads(text)
        except ValueError:
            # Data rusak: simpan salinannya (.corrupt), lalu buat ulang dari data bawaan.
            try:
                backend.write(name + ".corrupt", text)
            except StorageError:
                pass
            save_json(name, default)
            return copy.deepcopy(default)


def peek_json(name: str):
    """Baca tanpa membuat data bawaan. None bila tidak ada atau tidak valid."""
    try:
        text = get_backend().read(name)
        return None if text is None else json.loads(text)
    except (ValueError, StorageError):
        return None


def delete_json(name: str) -> None:
    with LOCK:
        get_backend().delete(name)


def list_names(prefix: str = "") -> list:
    return sorted(n for n in get_backend().names() if n.startswith(prefix))
