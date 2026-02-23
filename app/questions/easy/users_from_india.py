from app.questions.registry import register
from app.questions.schema import Question, TestCase

register(
    Question(
        id="users_from_india",
        title="Users from India",
        difficulty="Easy",
        description="""
Find all users from India.

Write a query to select all users where country = 'India'.
Expected columns: `id`, `name`, `email`, `country`
        """,
        hint="Use SELECT with WHERE country = 'India'.",
        reference_query="SELECT id, name, email, country FROM users WHERE country = 'India';",
        test_cases=[
            TestCase(
                description="must return at least 1 row",
                validator=lambda rows: len(rows) > 0,
            ),
            TestCase(
                description="all rows must have country = India",
                validator=lambda rows: (
                    all(row[3] == "India" for row in rows) if rows else False
                ),
            ),
        ],
    )
)
