"""SQL Editor panel for writing and executing queries."""

from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Button, DataTable, RichLog, TextArea, TabbedContent
from typing import Any

from app.constant import CONFIG_DIR
from app.db import excute_db_query
from app.utils import ui_table_handler


class SqlEditorPanel(Container):
    """Panel for writing SQL queries and executing them against the database."""

    def on_mount(self) -> None:
        """Called when the panel is mounted."""
        self.border_title = "SQL Query"

    def compose(self) -> ComposeResult:
        """Compose the panel UI."""
        yield Button("Run Query", id="btn-run", classes="floating-run-btn")
        yield TextArea(language="sql", id="sql-editor", text="SELECT * FROM users;")

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
        try:
            results = excute_db_query(db_path, sql_query)
            rows = results.get("rows", [])
            descriptions = results.get("descriptions", [])
            error = results.get("error", "")
            if error:
                log.write(f"[red]Error executing SQL Query: {error}[/red]")
            elif rows:
                log.write(f"[green]Query OK — {len(rows)} row(s) returned[/green]")
                ui_table_handler(table=dt, headers=descriptions, rows=rows)
                self.app.query_one(TabbedContent).active = "console-tab"  # type: ignore[return-value]
            else:
                log.write("[yellow]Query OK — no rows returned[/yellow]")
        except Exception as e:
            log.write(f"[red]Unexpected error: {e}[/red]")
