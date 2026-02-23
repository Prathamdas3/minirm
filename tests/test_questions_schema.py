"""Tests for questions schema module."""

import pytest
from app.questions.schema import Question, TestCase


def test_question_with_test_cases() -> None:
    """Test creating a Question with test_cases."""
    test_cases = [
        TestCase(
            description="must return at least 1 row",
            validator=lambda rows: len(rows) > 0,
        ),
        TestCase(
            description="must return exactly 3 columns",
            validator=lambda rows: len(rows[0]) == 3 if rows else False,
        ),
    ]

    question = Question(
        id="test_q",
        title="Test Question",
        description="Test description",
        difficulty="Easy",
        hint="Test hint",
        reference_query="SELECT 1",
        test_cases=test_cases,
    )

    assert question.id == "test_q"
    assert question.title == "Test Question"
    assert question.difficulty == "Easy"
    assert len(question.test_cases) == 2


def test_question_without_test_cases() -> None:
    """Test creating a Question without test_cases."""
    question = Question(
        id="test_q2",
        title="Test Question 2",
        description="Test description 2",
        difficulty="Medium",
        hint="Test hint 2",
        reference_query="SELECT 2",
    )

    assert question.id == "test_q2"
    assert question.test_cases == []


def test_test_case_creation() -> None:
    """Test TestCase dataclass."""
    validator = lambda rows: len(rows) > 0
    test_case = TestCase(
        description="must return at least 1 row",
        validator=validator,
    )

    assert test_case.description == "must return at least 1 row"
    assert test_case.validator == validator
    assert test_case.validator([]) is False
    assert test_case.validator([[1, 2, 3]]) is True
