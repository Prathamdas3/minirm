from app.questions.registry import register
from app.questions.schema import Question, TestCase

register(
    Question(
        id="products_never_ordered",
        title="Products Never Ordered",
        difficulty="Hard",
        description="""
Find all products that have never been ordered.

Write a query to find products that do not have any corresponding entries in the orders table.
Expected columns: `product_id`, `product_name`
        """,
        hint="Use LEFT JOIN with WHERE clause checking for NULL, or use NOT IN/NOT EXISTS subquery.",
        reference_query="SELECT p.id as product_id, p.name as product_name FROM products p LEFT JOIN orders o ON p.id = o.product_id WHERE o.id IS NULL;",
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
