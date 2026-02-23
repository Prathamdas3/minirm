from app.questions.registry import register
from app.questions.schema import Question, TestCase

register(
    Question(
        id="employees_with_managers",
        title="Employees with Their Managers",
        difficulty="Hard",
        description="""
List all employees along with their manager names using a self-join.

The employees table has a manager_id column that references another employee's id. Write a query to join the employees table with itself to get each employee's name along with their manager's name.
Expected columns: `employee_name`, `manager_name`
        """,
        hint="Use a self-join on employees table: SELECT e.name as employee_name, m.name as manager_name FROM employees e LEFT JOIN employees m ON e.manager_id = m.id;",
        reference_query="SELECT e.name as employee_name, m.name as manager_name FROM employees e LEFT JOIN employees m ON e.manager_id = m.id;",
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
            TestCase(
                description="must return all employees including those without managers",
                validator=lambda rows: len(rows) >= 10,
            ),
        ],
    )
)
