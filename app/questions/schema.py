"""Question data models for the minirm application."""

from typing import Any, Callable
from dataclasses import dataclass, field


@dataclass
class TestCase:
    description: str  # "should return 3 rows"
    validator: Callable[[list[Any]], bool]


@dataclass
class Question:
    id: str
    title: str
    description: str
    difficulty: str
    hint: str
    reference_query: str
    test_cases: list[TestCase] = field(default_factory=list[TestCase])
