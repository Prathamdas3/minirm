from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from app.questions.registry import get_all
from app.db import excute_db_query


@dataclass
class TestResult:
    description: str
    passed: bool
    error: str = ""


@dataclass
class RunResult:
    rows: list[Any]
    descriptions: list[str]
    test_results: list[TestResult] = field(default_factory=list[TestResult])
    error: str = ""

    @property
    def all_passed(self) -> bool:
        return not self.error and all(t.passed for t in self.test_results)


def run_question(db_path: Path, question_id: str, user_query: str) -> RunResult:
    question = get_all().get(question_id)
    if not question:
        return RunResult(rows=[], descriptions=[], error=f"Question '{question_id}' not found")

    result = excute_db_query(db_path, user_query)
    error = result.get("error", "")
    rows = result.get("rows", [])
    descriptions = result.get("descriptions", [])

    if error:
        return RunResult(rows=[], descriptions=[], error=error)

    test_results: list[TestResult] = []
    for tc in question.test_cases:
        try:
            passed = tc.validator(rows)
            test_results.append(TestResult(description=tc.description, passed=passed))
        except Exception as e:
            test_results.append(TestResult(description=tc.description, passed=False, error=str(e)))

    return RunResult(rows=rows, descriptions=descriptions, test_results=test_results)