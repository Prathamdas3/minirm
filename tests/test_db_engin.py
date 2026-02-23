"""Tests for database engine module."""

import pytest
from pathlib import Path
from app.db.engin import db_session


def test_db_session_basic(tmp_path: Path) -> None:
    """Test that db_session context manager works correctly."""
    db_path = tmp_path / "test.db"

    with db_session(path=db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT)")
        cursor.execute("INSERT INTO test (name) VALUES (?)", ("test_name",))

    assert db_path.exists()


def test_db_session_foreign_keys(tmp_path: Path) -> None:
    """Test that foreign keys are enabled by default."""
    db_path = tmp_path / "test_fk.db"

    with db_session(path=db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys")
        result = cursor.fetchone()
        assert result is not None
        assert result[0] == 1


def test_db_session_rollback(tmp_path: Path) -> None:
    """Test that db_session rolls back on error."""
    db_path = tmp_path / "test_rollback.db"

    # Even when exception is raised inside the context, it should rollback
    with db_session(path=db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE test (id INTEGER PRIMARY KEY)")
        # Raise exception but it should be caught by db_session
        raise Exception("Test rollback")

    # After rollback, check that no table was created (due to rollback)
    with db_session(path=db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        # The table should not exist because the transaction was rolled back
        assert len(tables) == 0
