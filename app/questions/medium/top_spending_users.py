from app.questions.registry import register
from app.questions.schema import Question, TestCase

register(
    Question(
        id="top_spending_users",
        title="Top Spending Users",
        difficulty="Medium",
        description="""
Find the top 5 users who have spent the most.

Write a query to join users, orders, and products, calculate total spending per user, and get top 5.
Expected columns: `user_name`, `total_spent`
        """,
        hint="Use JOIN with GROUP BY and ORDER BY with LIMIT.",
        reference_query="""SELECT u.name as user_name, SUM(p.price * o.quantity) as total_spent 
FROM users u 
INNER JOIN orders o ON u.id = o.user_id 
INNER JOIN products p ON o.product_id = p.id 
GROUP BY u.id 
ORDER BY total_spent DESC 
LIMIT 5;""",
        test_cases=[
            TestCase(
                description="must return at most 5 rows",
                validator=lambda rows: len(rows) <= 5,
            ),
            TestCase(
                description="must return exactly 2 columns",
                validator=lambda rows: (
                    all(len(row) == 2 for row in rows) if rows else False
                ),
            ),
        ],
    )
)
