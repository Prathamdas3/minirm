from app.questions.registry import register
from app.questions.schema import Question, TestCase

register(
    Question(
        id="select_all_users",
        title="Select All Users",
        difficulty="Easy",
        description="""
Write a query to retrieve all users from the `users` table.
Expected columns: `id`, `name`, `email`
    """,
        hint="Use SELECT with * or specify column names.",
        reference_query="SELECT id, name, email FROM users;",
        test_cases=[
            TestCase(
                description="must return at least 1 row",
                validator=lambda rows: len(rows) > 0,
            ),
            TestCase(
                description="must return exactly 3 columns",
                validator=lambda rows: len(rows[0]) == 3 if rows else False,
            ),
        ],
    )
)
