from app.questions.registry import register
from app.questions.schema import Question, TestCase

register(
    Question(
        id="products_with_categories",
        title="Products with Categories",
        difficulty="Medium",
        description="""
Find all products with their category names.

Write a query to join products and categories tables.
Expected columns: `product_name`, `category_name`
        """,
        hint="Use SELECT with JOIN on products and categories tables.",
        reference_query="""SELECT p.name as product_name, c.name as category_name 
FROM products p 
INNER JOIN categories c ON p.category_id = c.id;""",
        test_cases=[
            TestCase(
                description="must return at least 1 row",
                validator=lambda rows: len(rows) > 0,
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
