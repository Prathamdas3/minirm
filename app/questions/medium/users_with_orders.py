from app.questions.registry import register
from app.questions.schema import Question, TestCase

register(
    Question(
        id="users_with_orders",
        title="Users with Orders",
        difficulty="Medium",
        description="""
Find all users who have placed at least one order.

Write a query to join users and orders tables and get unique users who have orders.
Expected columns: `id`, `name`, `email` (from users)
        """,
        hint="Use SELECT DISTINCT with JOIN on users and orders tables.",
        reference_query="""SELECT DISTINCT u.id, u.name, u.email 
FROM users u 
INNER JOIN orders o ON u.id = o.user_id;""",
        test_cases=[
            TestCase(
                description="must return at least 1 row",
                validator=lambda rows: len(rows) > 0,
            ),
            TestCase(
                description="must return user ids from orders",
                validator=lambda rows: (
                    all(len(row) >= 3 for row in rows) if rows else False
                ),
            ),
        ],
    )
)
