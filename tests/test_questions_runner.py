"""Tests for questions runner module."""

import pytest
from pathlib import Path
from app.questions.runner import run_question, RunResult, TestResult
from app.questions.schema import Question, TestCase
from app.questions.registry import register, clear_registry
from app.db.utils import db_init


def test_run_result_all_passed() -> None:
    """Test RunResult.all_passed property."""
    result = RunResult(
        rows=[],
        descriptions=[],
        test_results=[TestResult(description="test", passed=True)],
    )
    assert result.all_passed is True

    result_with_error = RunResult(rows=[], descriptions=[], error="some error")
    assert result_with_error.all_passed is False

    result_with_failed = RunResult(
        rows=[],
        descriptions=[],
        test_results=[TestResult(description="test", passed=False)],
    )
    assert result_with_failed.all_passed is False


def test_run_question_not_found(tmp_path: Path) -> None:
    """Test run_question with non-existent question."""
    result = run_question(tmp_path / "test.db", "nonexistent", "SELECT 1")

    assert result.error != ""
    assert result.rows == []


def test_run_question_success(tmp_path: Path) -> None:
    """Test run_question with valid query."""
    db_path = tmp_path / "test.db"
    schema_path = Path(__file__).parent.parent / "app" / "db" / "sql" / "schema.sql"
    data_path = Path(__file__).parent.parent / "app" / "db" / "sql" / "data.sql"
    db_init(db_path)

    question = Question(
        id="test_q",
        title="Test",
        description="Test",
        difficulty="Easy",
        hint="Hint",
        reference_query="SELECT * FROM users",
        test_cases=[
            TestCase(
                description="must return at least 1 row",
                validator=lambda rows: len(rows) > 0,
            )
        ],
    )
    register(question)

    result = run_question(db_path, "test_q", "SELECT * FROM users")

    assert result.error == ""
    assert len(result.rows) > 0
    assert len(result.test_results) == 1
    assert result.test_results[0].passed is True


def test_run_question_wrong_answer(tmp_path: Path) -> None:
    """Test run_question with incorrect query."""
    db_path = tmp_path / "test.db"
    schema_path = Path(__file__).parent.parent / "app" / "db" / "sql" / "schema.sql"
    data_path = Path(__file__).parent.parent / "app" / "db" / "sql" / "data.sql"
    db_init(db_path)

    question = Question(
        id="test_q2",
        title="Test",
        description="Test",
        difficulty="Easy",
        hint="Hint",
        reference_query="SELECT * FROM users",
        test_cases=[
            TestCase(
                description="must return 0 rows", validator=lambda rows: len(rows) == 0
            )
        ],
    )
    register(question)

    result = run_question(db_path, "test_q2", "SELECT * FROM users")

    assert result.error == ""
    assert len(result.test_results) == 1
    assert result.test_results[0].passed is False


def test_validator_exception(tmp_path: Path) -> None:
    """Test validator exception handling in run_question."""
    db_path = tmp_path / "test.db"
    schema_path = Path(__file__).parent.parent / "app" / "db" / "sql" / "schema.sql"
    data_path = Path(__file__).parent.parent / "app" / "db" / "sql" / "data.sql"
    db_init(db_path)

    question = Question(
        id="test_validator_error",
        title="Test",
        description="Test",
        difficulty="Easy",
        hint="Hint",
        reference_query="SELECT * FROM users",
        test_cases=[
            TestCase(description="will raise exception", validator=lambda rows: 1 / 0)
        ],
    )
    register(question)

    result = run_question(db_path, "test_validator_error", "SELECT * FROM users")

    assert result.error == ""
    assert len(result.test_results) == 1
    assert result.test_results[0].passed is False
    assert "division" in result.test_results[0].error.lower()


def test_run_question_empty_test_cases(tmp_path: Path) -> None:
    """Test run_question with no test cases."""
    db_path = tmp_path / "test.db"
    schema_path = Path(__file__).parent.parent / "app" / "db" / "sql" / "schema.sql"
    data_path = Path(__file__).parent.parent / "app" / "db" / "sql" / "data.sql"
    db_init(db_path)

    question = Question(
        id="test_no_test_cases",
        title="Test",
        description="Test",
        difficulty="Easy",
        hint="Hint",
        reference_query="SELECT * FROM users",
        test_cases=[],
    )
    register(question)

    result = run_question(db_path, "test_no_test_cases", "SELECT * FROM users")

    assert result.error == ""
    assert len(result.rows) > 0
    assert result.test_results == []
    assert result.all_passed is True


def test_run_question_sql_error(tmp_path: Path) -> None:
    """Test SQL error handling in runner."""
    db_path = tmp_path / "test.db"
    schema_path = Path(__file__).parent.parent / "app" / "db" / "sql" / "schema.sql"
    db_init(db_path)

    question = Question(
        id="test_sql_error",
        title="Test",
        description="Test",
        difficulty="Easy",
        hint="Hint",
        reference_query="SELECT * FROM users",
        test_cases=[TestCase(description="test case", validator=lambda rows: True)],
    )
    register(question)

    result = run_question(db_path, "test_sql_error", "SELECT * FROM nonexistent")

    assert result.error != ""
    assert result.rows == []
    assert result.descriptions == []
