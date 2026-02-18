import typer
from rich import print
from pathlib import Path
from app.utils.handle_config_file import get_selected_db_path
from app.db.engin import db_session
from app.constant import APP_NAME
from rich.prompt import Prompt
import json
from typing import Any
from app.utils.table import cli_table_handler

qa_app = typer.Typer()


def execute_query(query: str, db_path: Path) -> list[Any]:
    with db_session(path=db_path) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(query)
        except Exception as e:
            print(f"[yellow]Query failed due to {str(e)}.[/yellow]")
            return []
        rows = cursor.fetchall()
        if rows:
            cli_table_handler(
                title="",
                headers=[description[0] for description in cursor.description],
                rows=rows,
            )
        return rows


@qa_app.command(name="qa", help="Test your sql knowledge")
def qa(
    questions: bool = typer.Option(
        False, "--questions", "-q", help="Visit the question list"
    ),
    all_questions: bool = typer.Option(
        False, "--all", "-a", help="Attempt all questions without asking"
    ),
):
    project_path = get_selected_db_path()
    db_path = project_path / f".{APP_NAME}" / "db.sqlite3"

    if not db_path.exists():
        print("[bold red]Error:[/] Database not found. Please run 'init' first.")
        raise typer.Exit(1)

    package_dir = Path(__file__).parent.parent
    with open(package_dir / "qa/question.json", "r") as f:
        files = json.load(f)

    question_list: list[dict[str, str]] = files.get("questions", [])

    for no, item in enumerate(question_list):
        question = item.get("question")
        expected_query: str = item.get("answer", "")

        print(f"{no + 1}. {question}")

        should_attempt = all_questions
        if not should_attempt and not questions:
            choice = Prompt.ask("Want to attempt this question?", choices=["y", "n"])
            if choice == "y":
                should_attempt = True

        if should_attempt:
            while True:
                user_query = Prompt.ask("Write the query \n")
                user_rows = execute_query(query=user_query, db_path=db_path)

                expected_rows = []
                with db_session(path=db_path) as conn:
                    cursor = conn.cursor()
                    try:
                        cursor.execute(expected_query)
                        expected_rows = cursor.fetchall()
                    except Exception:
                        pass  # Should happen if answer in json is valid

                if user_rows == expected_rows:
                    print("[bold green]Correct![/bold green]")
                    break
                else:
                    print("[bold red]Incorrect result.[/bold red]")
                    retry = Prompt.ask("Try again?", choices=["y", "n"])
                    if retry == "n":
                        print(f"The expected query was: [bold]{expected_query}[/bold]")
                        break
