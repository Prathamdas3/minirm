from app.questions.registry import register
from app.questions.schema import Question, TestCase

register(
    Question(
        id="count_users_by_city",
        title="Count Users by City",
        difficulty="Easy",
        description="""
Count the number of users in each city.

Write a query to group users by city and count them.
Expected columns: `city`, `count`
        """,
        hint="Use SELECT COUNT(*) with GROUP BY city.",
        reference_query="SELECT city, COUNT(*) as count FROM users GROUP BY city;",
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
