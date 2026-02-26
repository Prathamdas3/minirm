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


def test_excute_db_query_insert_verifies(tmp_path: Path) -> None:
    """Test executing an INSERT and verifying data was actually inserted."""
    db_path = tmp_path / "test.db"
    db_init(db_path)

    result = excute_db_query(
        db_path,
        "INSERT INTO users (name, email) VALUES ('VerifyMe', 'verify@test.com')",
    )

    assert result["error"] == ""
    assert result["rows"] == []

    # Verify the data was actually inserted
    verify = excute_db_query(
        db_path, "SELECT name, email FROM users WHERE email = 'verify@test.com'"
    )
    assert len(verify["rows"]) == 1
    assert verify["rows"][0][0] == "VerifyMe"


def test_excute_db_query_update_verifies(tmp_path: Path) -> None:
    """Test executing an UPDATE and verifying data was actually changed."""
    db_path = tmp_path / "test.db"
    db_init(db_path)

    excute_db_query(
        db_path,
        "INSERT INTO users (name, email) VALUES ('Original', 'update@test.com')",
    )
    result = excute_db_query(
        db_path, "UPDATE users SET name = 'UpdatedName' WHERE email = 'update@test.com'"
    )

    assert result["error"] == ""

    # Verify the data was actually updated
    verify = excute_db_query(
        db_path, "SELECT name FROM users WHERE email = 'update@test.com'"
    )
    assert len(verify["rows"]) == 1
    assert verify["rows"][0][0] == "UpdatedName"


def test_excute_db_query_delete_verifies(tmp_path: Path) -> None:
    """Test executing a DELETE and verifying data was actually removed."""
    db_path = tmp_path / "test.db"
    db_init(db_path)

    excute_db_query(
        db_path,
        "INSERT INTO users (name, email) VALUES ('ToDelete', 'delete@test.com')",
    )
    result = excute_db_query(
        db_path, "DELETE FROM users WHERE email = 'delete@test.com'"
    )

    assert result["error"] == ""

    # Verify the data was actually deleted
    verify = excute_db_query(
        db_path, "SELECT * FROM users WHERE email = 'delete@test.com'"
    )
    assert len(verify["rows"]) == 0


def test_excute_db_query_join(tmp_path: Path) -> None:
    """Test executing a JOIN query between multiple tables."""
    db_path = tmp_path / "test.db"
    schema_path = Path(__file__).parent.parent / "app" / "db" / "sql" / "schema.sql"
    data_path = Path(__file__).parent.parent / "app" / "db" / "sql" / "data.sql"
    db_init(db_path)

    query = "SELECT u.name, o.id as order_id FROM users u JOIN orders o ON u.id = o.user_id LIMIT 5"

    result = excute_db_query(db_path, query)

    assert result["error"] == ""


def test_excute_db_query_subquery(tmp_path: Path) -> None:
    """Test executing a subquery."""
    db_path = tmp_path / "test.db"
    db_init(db_path)

    query = "SELECT * FROM users WHERE id IN (SELECT user_id FROM orders LIMIT 5)"

    result = excute_db_query(db_path, query)

    assert result["error"] == ""
    assert isinstance(result["rows"], list)


def test_excute_db_query_order_by(tmp_path: Path) -> None:
    """Test ORDER BY clause."""
    db_path = tmp_path / "test.db"
    db_init(db_path)

    query = "SELECT name, age FROM users ORDER BY age DESC"

    result = excute_db_query(db_path, query)

    assert result["error"] == ""
    assert len(result["rows"]) > 0

    ages = [row[1] for row in result["rows"] if row[1] is not None]
    assert ages == sorted(ages, reverse=True)


def test_excute_db_query_distinct(tmp_path: Path) -> None:
    """Test DISTINCT keyword."""
    db_path = tmp_path / "test.db"
    db_init(db_path)

    query = "SELECT DISTINCT country FROM users"

    result = excute_db_query(db_path, query)

    assert result["error"] == ""
    countries = [row[0] for row in result["rows"]]
    assert len(countries) == len(set(countries))


def test_excute_db_query_case(tmp_path: Path) -> None:
    """Test CASE WHEN expressions."""
    db_path = tmp_path / "test.db"
    db_init(db_path)

    query = """
        SELECT name,
        CASE
            WHEN age > 30 THEN 'Old'
            WHEN age < 25 THEN 'Young'
            ELSE 'Middle'
        END as age_group
        FROM users
        LIMIT 10
    """

    result = excute_db_query(db_path, query)

    assert result["error"] == ""
    assert "age_group" in result["descriptions"]
    assert len(result["rows"]) > 0


def test_excute_db_query_where_and_or(tmp_path: Path) -> None:
    """Test WHERE with AND/OR operators."""
    db_path = tmp_path / "test.db"
    db_init(db_path)

    query = "SELECT * FROM users WHERE country = 'India' AND age > 25"

    result = excute_db_query(db_path, query)

    assert result["error"] == ""
    for row in result["rows"]:
        idx_country = result["descriptions"].index("country")
        idx_age = result["descriptions"].index("age")
        assert row[idx_country] == "India"
        assert row[idx_age] is not None and row[idx_age] > 25


def test_excute_db_query_limit_offset(tmp_path: Path) -> None:
    """Test LIMIT and OFFSET."""
    db_path = tmp_path / "test.db"
    db_init(db_path)

    query = "SELECT id FROM users ORDER BY id LIMIT 3 OFFSET 5"

    result = excute_db_query(db_path, query)

    assert result["error"] == ""
    assert len(result["rows"]) <= 3
