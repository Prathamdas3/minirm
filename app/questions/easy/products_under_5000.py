from app.questions.registry import register
from app.questions.schema import Question, TestCase

register(
    Question(
        id="products_under_5000",
        title="Products Under 5000",
        difficulty="Easy",
        description="""
Find all products with a price less than 5000.

Write a query to retrieve products from the `products` table where price is under 5000.
Expected columns: `id`, `name`, `price`
        """,
        hint="Use SELECT with WHERE clause and < operator.",
        reference_query="SELECT id, name, price FROM products WHERE price < 5000;",
        test_cases=[
            TestCase(
                description="must return at least 1 row",
                validator=lambda rows: len(rows) > 0,
            ),
            TestCase(
                description="must return exactly 3 columns",
                validator=lambda rows: len(rows[0]) == 3 if rows else False,
            ),
            TestCase(
                description="all products must have price < 5000",
                validator=lambda rows: (
                    all(row[2] < 5000 for row in rows) if rows else False
                ),
            ),
        ],
    )
)
