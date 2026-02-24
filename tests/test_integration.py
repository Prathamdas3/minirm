"""Integration tests for the minirm application."""

import pytest
from pathlib import Path
from app.questions.schema import Question, TestCase
from app.questions.registry import register, get_all, get_by_difficulty, clear_registry
from app.questions.runner import run_question
from app.db.utils import db_init, excute_db_query


@pytest.fixture(autouse=True)
def clear_questions() -> None:
    """Clear registry before and after each test."""
    clear_registry()
    yield
    clear_registry()


def test_full_question_flow(tmp_path: Path) -> None:
    """Test full flow: register question -> run query -> validate."""
    db_path = tmp_path / "test.db"
    db_init(db_path)

    question = Question(
        id="flow_test",
        title="Flow Test",
        description="Test flow",
        difficulty="Easy",
        hint="Hint",
        reference_query="SELECT * FROM users",
        test_cases=[
            TestCase(
                description="must return rows", validator=lambda rows: len(rows) > 0
            )
        ],
    )
    register(question)

    assert "flow_test" in get_all()

    result = run_question(db_path, "flow_test", "SELECT * FROM users")

    assert result.error == ""
    assert result.all_passed is True
    assert len(result.rows) > 0


def test_easy_question_validation(tmp_path: Path) -> None:
    """Test with actual easy question."""
    db_path = tmp_path / "test.db"
    schema_path = Path(__file__).parent.parent / "app" / "db" / "sql" / "schema.sql"
    data_path = Path(__file__).parent.parent / "app" / "db" / "sql" / "data.sql"
    db_init(db_path)

    question = Question(
        id="easy_select",
        title="Select All Users",
        description="Select all users from users table",
        difficulty="Easy",
        hint="Use SELECT *",
        reference_query="SELECT * FROM users",
        test_cases=[
            TestCase(
                description="must return all columns",
                validator=lambda rows: len(rows[0]) == 7 if rows else False,
            ),
            TestCase(
                description="must return at least 1 row",
                validator=lambda rows: len(rows) > 0,
            ),
        ],
    )
    register(question)

    result = run_question(db_path, "easy_select", "SELECT * FROM users")

    assert result.error == ""
    assert result.all_passed is True


def test_question_reference_query(tmp_path: Path) -> None:
    """Test executing reference query."""
    db_path = tmp_path / "test.db"
    db_init(db_path)

    question = Question(
        id="ref_test",
        title="Reference Test",
        description="Test reference query",
        difficulty="Easy",
        hint="Hint",
        reference_query="SELECT COUNT(*) FROM users",
        test_cases=[],
    )
    register(question)

    result = excute_db_query(db_path, question.reference_query)

    assert result["error"] == ""
    assert len(result["rows"]) > 0


def test_get_by_difficulty_empty() -> None:
    """Test get_by_difficulty with empty registry."""
    grouped = get_by_difficulty()

    assert grouped == {}


def test_get_by_difficulty_with_questions() -> None:
    """Test get_by_difficulty with questions."""
    q1 = Question(
        id="q1",
        title="Q1",
        description="Q1",
        difficulty="Easy",
        hint="H",
        reference_query="SELECT 1",
    )
    q2 = Question(
        id="q2",
        title="Q2",
        description="Q2",
        difficulty="Medium",
        hint="H",
        reference_query="SELECT 2",
    )
    q3 = Question(
        id="q3",
        title="Q3",
        description="Q3",
        difficulty="Easy",
        hint="H",
        reference_query="SELECT 3",
    )

    register(q1)
    register(q2)
    register(q3)

    grouped = get_by_difficulty()

    assert "Easy" in grouped
    assert "Medium" in grouped
    assert len(grouped["Easy"]) == 2
    assert len(grouped["Medium"]) == 1


def test_multiple_joins_query(tmp_path: Path) -> None:
    """Test query with multiple JOINs."""
    db_path = tmp_path / "test.db"
    schema_path = Path(__file__).parent.parent / "app" / "db" / "sql" / "schema.sql"
    data_path = Path(__file__).parent.parent / "app" / "db" / "sql" / "data.sql"
    db_init(db_path)

    query = """
        SELECT u.name, p.name as product_name, o.quantity
        FROM users u
        JOIN orders o ON u.id = o.user_id
        JOIN products p ON o.product_id = p.id
        LIMIT 5
    """

    result = excute_db_query(db_path, query)

    assert result["error"] == ""
    assert len(result["rows"]) > 0
    assert len(result["descriptions"]) == 3


def test_aggregation_with_having(tmp_path: Path) -> None:
    """Test aggregation with HAVING clause."""
    db_path = tmp_path / "test.db"
    schema_path = Path(__file__).parent.parent / "app" / "db" / "sql" / "schema.sql"
    data_path = Path(__file__).parent.parent / "app" / "db" / "sql" / "data.sql"
    db_init(db_path)

    query = """
        SELECT country, COUNT(*) as cnt
        FROM users
        GROUP BY country
        HAVING COUNT(*) > 3
    """

    result = excute_db_query(db_path, query)

    assert result["error"] == ""
    for row in result["rows"]:
        assert row[1] > 3
