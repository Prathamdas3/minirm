"""SQL Editor panel for writing and executing queries."""


from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Button, DataTable, RichLog, TextArea, TabbedContent
from typing import Any
from textual.reactive import reactive
from app.constant import CONFIG_DIR
from app.db import excute_db_query
from app.questions.runner import run_question,RunResult
from app.utils import ui_table_handler



class SqlEditorPanel(Container):
    """Panel for writing SQL queries and executing them against the database."""

    question: reactive[str] = reactive("")

    def on_mount(self) -> None:
        """Called when the panel is mounted."""
        self.border_title = "SQL Query"

    def compose(self) -> ComposeResult:
        """Compose the panel UI."""
        yield Button("Run Query", id="btn-run", classes="floating-run-btn")
        yield TextArea(
            language="sql", id="sql-editor", text="-- Write your query here --\n"
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press events to execute SQL queries."""
        if event.button.id != "btn-run":
            return
        sql_query = self.query_one("#sql-editor", TextArea).text
        db_path = CONFIG_DIR / "db.sqlite3"

        dt: DataTable[Any] = self.app.query_one("#console-table", DataTable)  # type: ignore[return-value]
        log = self.app.query_one("#console-log", RichLog)  # type: ignore
        dt.clear(columns=True)
        log.clear()

        if not self.question:
            try:
                results = excute_db_query(db_path, sql_query)
                rows = results.get("rows", [])
                descriptions = results.get("descriptions", [])
                error = results.get("error", "")
                if error:
                    log.write(f"[red]Error: {error}[/red]")
                elif rows:
                    log.write(f"[green]Query OK — {len(rows)} row(s) returned[/green]")
                    ui_table_handler(table=dt, headers=descriptions, rows=rows)
                    self.app.query_one(TabbedContent).active = "console-tab"  # type: ignore
                else:
                    log.write("[yellow]Query OK — no rows returned[/yellow]")
            except Exception as e:
                log.write(f"[red]Unexpected error: {e}[/red]")
            return

        try:
            result: RunResult = run_question(db_path, self.question, sql_query)

            if result.error:
                log.write(f"[red]Error: {result.error}[/red]")
                return

            if result.rows:
                log.write(
                    f"[green]Query OK — {len(result.rows)} row(s) returned[/green]"
                )
                ui_table_handler(
                    table=dt, headers=result.descriptions, rows=result.rows
                )
                self.app.query_one(TabbedContent).active = "console-tab"  # type: ignore
            else:
                log.write("[yellow]Query OK — no rows returned[/yellow]")

            # show test case results
            if result.test_results:
                log.write("\n[bold]Test Cases:[/bold]")
                for tr in result.test_results:
                    icon = "✅" if tr.passed else "❌"
                    log.write(f"  {icon} {tr.description}")
                    if tr.error:
                        log.write(f"     [red]{tr.error}[/red]")

                if result.all_passed:
                    log.write("\n[bold green]All test cases passed! 🎉[/bold green]")
                else:
                    log.write("\n[bold red]Some test cases failed.[/bold red]")

        except Exception as e:
            log.write(f"[red]Unexpected error: {e}[/red]")
