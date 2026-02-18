from typing import Annotated
import typer
from app.utils.handle_config_file import get_selected_db_path
from app.db.engin import db_session
from app.constant import APP_NAME
from app.utils.table import cli_table_handler

query_app = typer.Typer()


@query_app.command(name="query")
def query(
    query: Annotated[str, typer.Argument(help="SQL query to execute")],
    sql: Annotated[
        bool, typer.Option("--sql", "-s", help="SQL query to execute")
    ] = False,
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
        with db_session(path=db_path) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(query)
            except Exception as e:
                print(f"[yellow]Query failed due to {str(e)}.[/yellow]")
            rows = cursor.fetchall()
            if rows:
                cli_table_handler(
                    title="",
                    headers=[description[0] for description in cursor.description],
                    rows=rows,
                )
                
    