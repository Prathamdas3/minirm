"""Question registry for managing SQL practice questions."""

from app.questions.schema import Question

_questions: dict[str, Question] = {}


def register(question: Question) -> None:
    _questions[question.id] = question


def get_all() -> dict[str, Question]:
    return _questions


def get_by_difficulty() -> dict[str, list[Question]]:
    grouped: dict[str, list[Question]] = {}
    for q in _questions.values():
        grouped.setdefault(q.difficulty, []).append(q)
    return grouped


def clear_registry() -> None:
    """Clear all registered questions. Used for testing."""
    _questions.clear()
