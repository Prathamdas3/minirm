"""Tests for application constants."""

import pytest
from app.constant import SCHEMAS, RELATIONSHIPS, APP_NAME, CONFIG_DIR, HOME_DIR
from pathlib import Path


def test_app_name() -> None:
    """Test APP_NAME constant."""
    assert APP_NAME in ("minirm", "squilio")


def test_config_dir() -> None:
    """Test CONFIG_DIR is a Path."""
    assert isinstance(CONFIG_DIR, Path)
    assert CONFIG_DIR.name == ".minirm" or CONFIG_DIR.name == ".squilio"


def test_home_dir() -> None:
    """Test HOME_DIR is a string."""
    assert isinstance(HOME_DIR, str)
    assert HOME_DIR == str(Path.home())


def test_schemas_tables() -> None:
    """Verify expected tables exist in SCHEMAS."""
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
        assert table in SCHEMAS, f"Table {table} not found in SCHEMAS"


def test_schemas_structure() -> None:
    """Verify schema structure (column, type, constraints)."""
    for table_name, columns in SCHEMAS.items():
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


def test_schemas_users_columns() -> None:
    """Verify users table has expected columns."""
    users_cols = SCHEMAS["users"]
    column_names = [col["column"] for col in users_cols]

    assert "id" in column_names
    assert "name" in column_names
    assert "email" in column_names
    assert "phone" in column_names
    assert "age" in column_names
    assert "country" in column_names
    assert "city" in column_names


def test_schemas_foreign_keys() -> None:
    """Verify foreign key relationships in schemas."""
    employees = SCHEMAS["employees"]
    emp_cols = {col["column"]: col["constraints"] for col in employees}

    assert "department_id" in emp_cols
    assert "FK -> departments" in emp_cols["department_id"]

    assert "manager_id" in emp_cols
    assert "FK -> employees" in emp_cols["manager_id"]


def test_relationships_count() -> None:
    """Verify RELATIONSHIPS has expected count."""
    assert len(RELATIONSHIPS) > 0
    assert isinstance(RELATIONSHIPS, list)
    assert all(isinstance(rel, str) for rel in RELATIONSHIPS)


def test_relationships_format() -> None:
    """Verify relationships are properly formatted."""
    for rel in RELATIONSHIPS:
        assert "->" in rel, f"Relationship {rel} missing '->'"


def test_schemas_primary_keys() -> None:
    """Verify primary keys are defined correctly."""
    for table_name, columns in SCHEMAS.items():
        id_col = next((col for col in columns if col["column"] == "id"), None)
        assert id_col is not None, f"Table {table_name} missing id column"
        assert "PRIMARY KEY" in id_col["constraints"]
