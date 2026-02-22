"""Database engine and session management."""

import sqlite3
from contextlib import contextmanager
from pathlib import Path


@contextmanager
def db_session(path: Path):
    """Context manager for database sessions with automatic commit/rollback.

    Args:
        path: Path to the SQLite database file.

    Yields:
        sqlite3.Connection: Database connection with foreign keys enabled.
    """
    conn = sqlite3.connect(path)
    try:
        conn.execute("PRAGMA foreign_keys = ON;")
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
    finally:
        conn.close()
