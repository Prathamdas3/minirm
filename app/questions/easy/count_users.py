from app.questions.registry import register
from app.questions.schema import Question, TestCase

register(
    Question(
        id="count_users",
        title="Count Users",
        difficulty="Easy",
        description="""
Count the total number of users.

Write a query to count all rows in the `users` table.
Expected columns: `count`
        """,
        hint="Use SELECT COUNT(*) to count rows.",
        reference_query="SELECT COUNT(*) as count FROM users;",
        test_cases=[
            TestCase(
                description="must return exactly 1 row",
                validator=lambda rows: len(rows) == 1,
            ),
            TestCase(
                description="must return count greater than 0",
                validator=lambda rows: rows[0][0] > 0 if rows else False,
            ),
        ],
    )
)
