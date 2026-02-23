"""Tests for database seed module."""

import pytest
from pathlib import Path
from app.db.seed import seed_db


def test_seed_db_creates_tables(tmp_path: Path) -> None:
    """Test that seed_db creates tables from schema."""
    db_path = tmp_path / "test_seed.db"
    schema_path = Path(__file__).parent.parent / "app" / "db" / "sql" / "schema.sql"

    # seed_path is None - should still create tables from schema
    seed_db(db_path=db_path, schema_path=schema_path, seed_path=None)

    assert db_path.exists()

    # Verify the tables were created
    import sqlite3

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    conn.close()

    assert len(tables) > 0


def test_seed_db_with_data(tmp_path: Path) -> None:
    """Test that seed_db creates tables and inserts data."""
    db_path = tmp_path / "test_seed_data.db"
    schema_path = Path(__file__).parent.parent / "app" / "db" / "sql" / "schema.sql"
    data_path = Path(__file__).parent.parent / "app" / "db" / "sql" / "data.sql"

    seed_db(db_path=db_path, schema_path=schema_path, seed_path=data_path)

    assert db_path.exists()

    import sqlite3

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    conn.close()

    assert count > 0
