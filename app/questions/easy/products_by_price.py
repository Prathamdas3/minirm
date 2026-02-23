from app.questions.registry import register
from app.questions.schema import Question, TestCase

register(
    Question(
        id="products_by_price",
        title="Products Sorted by Price",
        difficulty="Easy",
        description="""
List all products sorted by price in ascending order.

Write a query to retrieve products from the `products` table ordered by price from lowest to highest.
Expected columns: `id`, `name`, `price`
        """,
        hint="Use SELECT with ORDER BY clause and ASC (or no suffix as ASC is default).",
        reference_query="SELECT id, name, price FROM products ORDER BY price ASC;",
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
                description="must be sorted by price ascending",
                validator=lambda rows: (
                    all(rows[i][2] <= rows[i + 1][2] for i in range(len(rows) - 1))
                    if len(rows) > 1
                    else True
                ),
            ),
        ],
    )
)
