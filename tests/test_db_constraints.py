"""Tests for database constraints."""

import pytest
from pathlib import Path
from app.db.utils import excute_db_query
from app.db.seed import seed_db


def test_not_null_constraint(tmp_path: Path) -> None:
    """Test that NOT NULL constraint rejects NULL values."""
    db_path = tmp_path / "test_not_null.db"
    schema_path = Path(__file__).parent.parent / "app" / "db" / "sql" / "schema.sql"
    seed_db(db_path=db_path, schema_path=schema_path, seed_path=None)

    result = excute_db_query(
        db_path, "INSERT INTO users (name, email) VALUES (NULL, 'test@test.com')"
    )
    assert result["error"] != ""


def test_unique_constraint(tmp_path: Path) -> None:
    """Test that UNIQUE constraint prevents duplicates."""
    db_path = tmp_path / "test_unique.db"
    schema_path = Path(__file__).parent.parent / "app" / "db" / "sql" / "schema.sql"
    seed_db(db_path=db_path, schema_path=schema_path, seed_path=None)

    excute_db_query(
        db_path, "INSERT INTO users (name, email) VALUES ('Test', 'unique@test.com')"
    )
    result = excute_db_query(
        db_path, "INSERT INTO users (name, email) VALUES ('Test2', 'unique@test.com')"
    )

    assert result["error"] != ""
    assert "UNIQUE constraint failed" in result["error"]


def test_primary_key_constraint(tmp_path: Path) -> None:
    """Test that PRIMARY KEY auto-increments and is unique."""
    db_path = tmp_path / "test_pk.db"
    schema_path = Path(__file__).parent.parent / "app" / "db" / "sql" / "schema.sql"
    seed_db(db_path=db_path, schema_path=schema_path, seed_path=None)

    result1 = excute_db_query(
        db_path, "INSERT INTO users (name, email) VALUES ('User1', 'pk1@test.com')"
    )
    result2 = excute_db_query(
        db_path, "INSERT INTO users (name, email) VALUES ('User2', 'pk2@test.com')"
    )

    assert result1["error"] == ""
    assert result2["error"] == ""

    ids = excute_db_query(db_path, "SELECT id FROM users ORDER BY id")
    assert len(set(ids["rows"])) == 2


def test_foreign_key_constraint(tmp_path: Path) -> None:
    """Test that FK constraint enforces relationships."""
    db_path = tmp_path / "test_fk.db"
    schema_path = Path(__file__).parent.parent / "app" / "db" / "sql" / "schema.sql"
    seed_db(db_path=db_path, schema_path=schema_path, seed_path=None)

    result = excute_db_query(
        db_path,
        "INSERT INTO employees (name, email, department_id) VALUES ('Test', 'emp@test.com', 9999)",
    )

    assert result["error"] != ""
    assert "FOREIGN KEY constraint failed" in result["error"]


def test_check_constraint(tmp_path: Path) -> None:
    """Test CHECK constraint on orders.status."""
    db_path = tmp_path / "test_check.db"
    schema_path = Path(__file__).parent.parent / "app" / "db" / "sql" / "schema.sql"
    seed_db(db_path=db_path, schema_path=schema_path, seed_path=None)

    result = excute_db_query(
        db_path,
        "INSERT INTO orders (user_id, product_id, quantity, order_date, status) VALUES (1, 1, 1, '2024-01-01', 'INVALID_STATUS')",
    )

    assert result["error"] != ""
