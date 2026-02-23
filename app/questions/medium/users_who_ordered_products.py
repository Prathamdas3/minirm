from app.questions.registry import register
from app.questions.schema import Question, TestCase

register(
    Question(
        id="users_who_ordered_products",
        title="Users Who Ordered Products",
        difficulty="Medium",
        description="""
Find all users who have placed at least one order.

Write a query to get users who have orders in the orders table.
Expected columns: `user_id`, `user_name`
        """,
        hint="Use DISTINCT with JOIN or use EXISTS/IN subquery.",
        reference_query="SELECT DISTINCT u.id as user_id, u.name as user_name FROM users u JOIN orders o ON u.id = o.user_id;",
        test_cases=[
            TestCase(
                description="must return at least 1 row",
                validator=lambda rows: len(rows) > 0,
            ),
            TestCase(
                description="each row must have 2 columns",
                validator=lambda rows: (
                    all(len(row) == 2 for row in rows) if rows else False
                ),
            ),
        ],
    )
)
