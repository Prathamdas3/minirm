from app.questions.registry import register
from app.questions.schema import Question, TestCase

register(
    Question(
        id="order_users_by_age",
        title="Order Users by Age",
        difficulty="Easy",
        description="""
Order users by age in descending order.

Write a query to select all users and order them by age from highest to lowest.
Expected columns: `id`, `name`, `age`
        """,
        hint="Use SELECT with ORDER BY age DESC.",
        reference_query="SELECT id, name, age FROM users ORDER BY age DESC;",
        test_cases=[
            TestCase(
                description="must return at least 1 row",
                validator=lambda rows: len(rows) > 0,
            ),
            TestCase(
                description="ages must be in descending order",
                validator=lambda rows: (
                    all(rows[i][2] >= rows[i + 1][2] for i in range(len(rows) - 1))
                    if len(rows) > 1
                    else True
                ),
            ),
        ],
    )
)
