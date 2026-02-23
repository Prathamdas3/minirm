"""Tests for questions registry module."""

import pytest
from app.questions.registry import register, get_all, get_by_difficulty
from app.questions.schema import Question, TestCase


def test_register() -> None:
    """Test registering a question."""
    question = Question(
        id="test_question",
        title="Test Question",
        description="Test description",
        difficulty="Easy",
        hint="Test hint",
        reference_query="SELECT 1",
        test_cases=[],
    )

    register(question)

    assert "test_question" in get_all()


def test_get_all() -> None:
    """Test getting all questions."""
    questions = get_all()

    assert isinstance(questions, dict)


def test_get_by_difficulty() -> None:
    """Test getting questions grouped by difficulty."""
    grouped = get_by_difficulty()

    assert isinstance(grouped, dict)
