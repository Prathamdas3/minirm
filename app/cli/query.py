from typing import Annotated
import typer
from app.utils.handle_config_file import get_selected_db_path
from app.db.engin import db_session
from app.constant import APP_NAME

query_app = typer.Typer()


@query_app.command(name="query")
def query(
    query: Annotated[str, typer.Argument(help="SQL query to execute")],
    sql: Annotated[bool, typer.Option(help="SQL query to execute")] = False,
):
    """
    This command is for executing SQL queries
    """
    project_path = get_selected_db_path()
    db_path = project_path / f".{APP_NAME}" / "db.sqlite3"

    if not db_path.exists():
        print("[bold red]Error:[/] Database not found. Please run 'init' first.")
        raise typer.Exit(1)

    if sql:
        print(f"DEBUG: db_path={db_path}")
        print(f"DEBUG: query={query}")
        with db_session(path=db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            print(f"DEBUG: rows count={len(rows)}")
            if rows:
                # Add columns based on cursor description
                # for description in cursor.description:
                #     example_data_table.add_column(description[0], style="bold cyan")
                # for row in rows:
                #     example_data_table.add_row(*[str(item) for item in row])
                # print(example_data_table)
                print(rows)
            else:
                print("[yellow]No data found for the query.[/yellow]")
