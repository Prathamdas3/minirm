from app.questions.registry import register
from app.questions.schema import Question, TestCase

register(
    Question(
        id="top_3_spending_users",
        title="Top 3 Spending Users",
        difficulty="Hard",
        description="""
Find the top 3 users who have spent the most money.

Write a query to join users, orders, and products tables, calculate total spending per user, and return top 3.
Expected columns: `user_name`, `total_spent`
        """,
        hint="Use JOINs between users, orders, and products. Then SUM(price * quantity) with GROUP BY user, ORDER BY total_spent DESC, and LIMIT 3.",
        reference_query="SELECT u.name as user_name, SUM(o.quantity * p.price) as total_spent FROM users u JOIN orders o ON u.id = o.user_id JOIN products p ON o.product_id = p.id GROUP BY u.id, u.name ORDER BY total_spent DESC LIMIT 3;",
        test_cases=[
            TestCase(
                description="must return exactly 3 rows",
                validator=lambda rows: len(rows) == 3,
            ),
            TestCase(
                description="each row must have 2 columns",
                validator=lambda rows: (
                    all(len(row) == 2 for row in rows) if rows else False
                ),
            ),
            TestCase(
                description="must be sorted by total_spent descending",
                validator=lambda rows: (
                    all(rows[i][1] >= rows[i + 1][1] for i in range(len(rows) - 1))
                    if len(rows) > 1
                    else True
                ),
            ),
        ],
    )
)
