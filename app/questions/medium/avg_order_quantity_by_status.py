from app.questions.registry import register
from app.questions.schema import Question, TestCase

register(
    Question(
        id="avg_order_quantity_by_status",
        title="Average Order Quantity by Status",
        difficulty="Medium",
        description="""
Calculate the average quantity of orders for each status.

Write a query to group orders by status and calculate the average quantity.
Expected columns: `status`, `avg_quantity`
        """,
        hint="Use SELECT with GROUP BY status and AVG(quantity).",
        reference_query="SELECT status, AVG(quantity) as avg_quantity FROM orders GROUP BY status;",
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
