"""Tests for dynamic schema loading from database."""

import pytest
from pathlib import Path
from app.components.schema import get_db_schema
from app.db.utils import db_init


def test_get_db_schema_returns_schemas_and_relationships(tmp_path: Path) -> None:
    """Test that get_db_schema returns both schemas dict and relationships list."""
    db_path = tmp_path / "test.db"
    db_init(db_path)

    schemas, relationships = get_db_schema(db_path)

    assert isinstance(schemas, dict)
    assert isinstance(relationships, list)


def test_get_db_schema_returns_expected_tables(tmp_path: Path) -> None:
    """Test that get_db_schema returns expected tables from database."""
    db_path = tmp_path / "test.db"
    db_init(db_path)

    schemas, relationships = get_db_schema(db_path)

    expected_tables = [
        "users",
        "departments",
        "employees",
        "categories",
        "suppliers",
        "products",
        "orders",
        "reviews",
    ]
    for table in expected_tables:
        assert table in schemas, f"Table {table} not found in schemas"


def test_get_db_schema_table_structure(tmp_path: Path) -> None:
    """Test that each table has correct structure with column, type, constraints."""
    db_path = tmp_path / "test.db"
    db_init(db_path)

    schemas, relationships = get_db_schema(db_path)

    for table_name, columns in schemas.items():
        assert isinstance(table_name, str)
        assert isinstance(columns, list)
        assert len(columns) > 0

        for col in columns:
            assert "column" in col
            assert "type" in col
            assert "constraints" in col
            assert isinstance(col["column"], str)
            assert isinstance(col["type"], str)
            assert isinstance(col["constraints"], str)


def test_get_db_schema_users_table(tmp_path: Path) -> None:
    """Test that users table has expected columns."""
    db_path = tmp_path / "test.db"
    db_init(db_path)

    schemas, relationships = get_db_schema(db_path)

    users_cols = schemas.get("users", [])
    column_names = [col["column"] for col in users_cols]

    assert "id" in column_names
    assert "name" in column_names
    assert "email" in column_names


def test_get_db_schema_foreign_keys(tmp_path: Path) -> None:
    """Test that foreign key relationships are extracted."""
    db_path = tmp_path / "test.db"
    db_init(db_path)

    schemas, relationships = get_db_schema(db_path)

    assert len(relationships) > 0
    for rel in relationships:
        assert "->" in rel
        assert isinstance(rel, str)


def test_get_db_schema_empty_db(tmp_path: Path) -> None:
    """Test get_db_schema with empty database."""
    db_path = tmp_path / "empty.db"

    # Create empty database
    import sqlite3

    conn = sqlite3.connect(db_path)
    conn.close()

    schemas, relationships = get_db_schema(db_path)

    assert schemas == {}
    assert relationships == []


def test_get_db_schema_creates_empty_db(tmp_path: Path) -> None:
    """Test that get_db_schema works with non-existent database (creates it)."""
    db_path = tmp_path / "new.db"

    # sqlite3.connect creates the file if it doesn't exist
    schemas, relationships = get_db_schema(db_path)

    assert isinstance(schemas, dict)
    assert isinstance(relationships, list)
