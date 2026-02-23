from app.questions.registry import register
from app.questions.schema import Question, TestCase

register(
    Question(
        id="top_5_users",
        title="Top 5 Users",
        difficulty="Easy",
        description="""
Get the first 5 users from the table.

Write a query to select only the first 5 users from the `users` table.
Expected columns: `id`, `name`, `email`
        """,
        hint="Use SELECT with LIMIT 5.",
        reference_query="SELECT id, name, email FROM users LIMIT 5;",
        test_cases=[
            TestCase(
                description="must return exactly 5 rows",
                validator=lambda rows: len(rows) == 5,
            ),
            TestCase(
                description="must return exactly 3 columns",
                validator=lambda rows: len(rows[0]) == 3 if rows else False,
            ),
        ],
    )
)
