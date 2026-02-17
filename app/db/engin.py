import sqlite3
from contextlib import contextmanager
from pathlib import Path


@contextmanager
def db_session(path: Path):
    conn = sqlite3.connect(path)
    try:
        conn.execute("PRAGMA foreign_keys = ON;")
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
    finally:
        conn.close()
