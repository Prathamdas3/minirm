from app.questions.registry import register
from app.questions.schema import Question, TestCase

register(
    Question(
        id="users_older_than_25",
        title="Users Older Than 25",
        difficulty="Easy",
        description="""
Find all users who are older than 25 years.

Write a query to retrieve users from the `users` table where age is greater than 25.
Expected columns: `id`, `name`, `email`, `age`
        """,
        hint="Use SELECT with WHERE clause and > operator.",
        reference_query="SELECT id, name, email, age FROM users WHERE age > 25;",
        test_cases=[
            TestCase(
                description="must return at least 1 row",
                validator=lambda rows: len(rows) > 0,
            ),
            TestCase(
                description="must return exactly 4 columns",
                validator=lambda rows: len(rows[0]) == 4 if rows else False,
            ),
            TestCase(
                description="all users must have age > 25",
                validator=lambda rows: (
                    all(row[3] > 25 for row in rows) if rows else False
                ),
            ),
        ],
    )
)
