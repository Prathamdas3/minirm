from app.questions.registry import register
from app.questions.schema import Question, TestCase

register(
    Question(
        id="find_user_by_id",
        title="Find User by ID",
        difficulty="Easy",
        description="""
Find a user by their ID.

Find the user with id = 1 from the `users` table.
Expected columns: `id`, `name`, `email`
        """,
        hint="Use SELECT with WHERE clause to filter by id.",
        reference_query="SELECT id, name, email FROM users WHERE id = 1;",
        test_cases=[
            TestCase(
                description="must return exactly 1 row",
                validator=lambda rows: len(rows) == 1,
            ),
            TestCase(
                description="must return user with id = 1",
                validator=lambda rows: rows[0][0] == 1 if rows else False,
            ),
        ],
    )
)
