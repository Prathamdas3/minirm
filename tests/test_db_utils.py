"""Tests for database utility functions."""

import pytest
from pathlib import Path
from app.db.utils import excute_db_query, db_init, create_or_refresh_db
from app.constant import CONFIG_DIR


def test_excute_db_query_select(tmp_path: Path) -> None:
    """Test executing a SELECT query."""
    db_path = tmp_path / "test.db"
    schema_path = Path(__file__).parent.parent / "app" / "db" / "sql" / "schema.sql"
    data_path = Path(__file__).parent.parent / "app" / "db" / "sql" / "data.sql"
    db_init(db_path)

    result = excute_db_query(db_path, "SELECT * FROM users LIMIT 3")

    assert result["error"] == ""
    assert len(result["rows"]) == 3
    assert len(result["descriptions"]) == 7


def test_excute_db_query_insert(tmp_path: Path) -> None:
    """Test executing an INSERT query."""
    db_path = tmp_path / "test.db"
    schema_path = Path(__file__).parent.parent / "app" / "db" / "sql" / "schema.sql"
    db_init(db_path)

    result = excute_db_query(
        db_path, "INSERT INTO users (name, email) VALUES ('Test', 'test@test.com')"
    )

    assert result["error"] == ""
    assert result["rows"] == []


def test_excute_db_query_error(tmp_path: Path) -> None:
    """Test executing an invalid query."""
    db_path = tmp_path / "test.db"
    schema_path = Path(__file__).parent.parent / "app" / "db" / "sql" / "schema.sql"
    db_init(db_path)

    result = excute_db_query(db_path, "SELECT * FROM nonexistent_table")

    assert result["error"] != ""
    assert result["rows"] == []


def test_excute_db_query_descriptions(tmp_path: Path) -> None:
    """Test that descriptions are returned correctly."""
    db_path = tmp_path / "test.db"
    schema_path = Path(__file__).parent.parent / "app" / "db" / "sql" / "schema.sql"
    db_init(db_path)

    result = excute_db_query(db_path, "SELECT id, name, email FROM users LIMIT 1")

    assert result["descriptions"] == ["id", "name", "email"]


def test_create_or_refresh_db(tmp_path: Path, monkeypatch) -> None:
    """Test that create_or_refresh_db creates the database."""
    monkeypatch.setattr("app.db.utils.CONFIG_DIR", tmp_path / ".minirm")

    create_or_refresh_db()

    db_path = tmp_path / ".minirm" / "db.sqlite3"
    assert db_path.exists()

    import sqlite3

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    conn.close()

    assert len(tables) > 0


def test_excute_db_query_update(tmp_path: Path) -> None:
    """Test executing an UPDATE query."""
    db_path = tmp_path / "test.db"
    schema_path = Path(__file__).parent.parent / "app" / "db" / "sql" / "schema.sql"
    db_init(db_path)

    excute_db_query(
        db_path, "INSERT INTO users (name, email) VALUES ('Test', 'test@test.com')"
    )
    result = excute_db_query(
        db_path, "UPDATE users SET name = 'Updated' WHERE email = 'test@test.com'"
    )

    assert result["error"] == ""


def test_excute_db_query_delete(tmp_path: Path) -> None:
    """Test executing a DELETE query."""
    db_path = tmp_path / "test.db"
    schema_path = Path(__file__).parent.parent / "app" / "db" / "sql" / "schema.sql"
    db_init(db_path)

    excute_db_query(
        db_path, "INSERT INTO users (name, email) VALUES ('Test', 'test@test.com')"
    )
    result = excute_db_query(db_path, "DELETE FROM users WHERE email = 'test@test.com'")

    assert result["error"] == ""


def test_excute_db_query_empty_result(tmp_path: Path) -> None:
    """Test executing a query with no results."""
    db_path = tmp_path / "test.db"
    schema_path = Path(__file__).parent.parent / "app" / "db" / "sql" / "schema.sql"
    db_init(db_path)

    result = excute_db_query(db_path, "SELECT * FROM users WHERE id = 999999")

    assert result["error"] == ""
    assert result["rows"] == []
    assert result["descriptions"] == [
        "id",
        "name",
        "email",
        "phone",
        "age",
        "country",
        "city",
    ]


def test_excute_db_query_aggregation(tmp_path: Path) -> None:
    """Test GROUP BY with aggregate functions."""
    db_path = tmp_path / "test.db"
    schema_path = Path(__file__).parent.parent / "app" / "db" / "sql" / "schema.sql"
    data_path = Path(__file__).parent.parent / "app" / "db" / "sql" / "data.sql"
    db_init(db_path)

    result = excute_db_query(
        db_path, "SELECT country, COUNT(*) as cnt FROM users GROUP BY country"
    )

    assert result["error"] == ""
    assert len(result["rows"]) > 0
    assert "country" in result["descriptions"]
    assert "cnt" in result["descriptions"]


def test_db_init(tmp_path: Path) -> None:
    """Test db_init function."""
    db_path = tmp_path / "test.db"

    db_init(db_path)

    assert db_path.exists()

    import sqlite3

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    conn.close()

    assert "users" in tables
    assert "departments" in tables
    assert "employees" in tables
