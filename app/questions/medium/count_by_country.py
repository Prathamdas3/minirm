from app.questions.registry import register
from app.questions.schema import Question, TestCase

register(
    Question(
        id="count_by_country",
        title="Count Users by Country",
        difficulty="Medium",
        description="""
Count the number of users in each country.

Write a query to group users by country and count them.
Expected columns: `country`, `count`
        """,
        hint="Use SELECT COUNT(*) with GROUP BY country.",
        reference_query="SELECT country, COUNT(*) as count FROM users GROUP BY country;",
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
