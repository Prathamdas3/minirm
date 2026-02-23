from app.questions.registry import register
from app.questions.schema import Question, TestCase

register(
    Question(
        id="avg_salary_by_dept",
        title="Average Salary by Department",
        difficulty="Medium",
        description="""
Find the average salary for each department.

Write a query to join employees and departments, then calculate average salary per department.
Expected columns: `department_name`, `avg_salary`
        """,
        hint="Use SELECT with JOIN and GROUP BY with AVG().",
        reference_query="""SELECT d.name as department_name, AVG(e.salary) as avg_salary 
FROM employees e 
INNER JOIN departments d ON e.department_id = d.id 
GROUP BY e.department_id;""",
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
