"""Schema panel for displaying database schemas."""

from textual.app import ComposeResult
from textual.containers import Container, VerticalScroll
from textual.widgets import Button, Collapsible, DataTable, Label, TabbedContent
from app.db import excute_db_query
from app.utils import ui_table_handler
from typing import Any
from app.constant import CONFIG_DIR, SCHEMAS, RELATIONSHIPS


class SchemasPanel(Container):
    """Panel for displaying database table schemas and relationships."""

    def on_mount(self) -> None:
        """Called when the panel is mounted."""
        self.border_title = "Database Schemas"

    def compose(self) -> ComposeResult:
        """Compose the panel UI."""
        with VerticalScroll(id="schemas-scroll"):
            for table_name in SCHEMAS.keys():
                with Collapsible(
                    title=f"{table_name} ({len(SCHEMAS.get(table_name, []))} rows)",
                    classes="collapsible",
                    collapsed=True,
                    id=f"collapsible_{table_name.lower()}",
                ):
                    dt: DataTable[Any] = DataTable(classes="schema-table")
                    columns = ["Column", "Type", "Constraints"]
                    rows = [
                        [col["column"], col["type"], col["constraints"]]
                        for col in SCHEMAS.get(table_name, [])
                    ]
                    ui_table_handler(dt, columns, rows)
                    yield dt
                    with Container(classes="sample-btn-container"):
                        yield Button(
                            "Run Sample Query",
                            id=f"btn-run-{table_name.lower()}",
                            classes="sample_btn",
                        )

            yield Label("Relationships", classes="section-header")
            with Container(classes="relationships-container"):
                for rel in RELATIONSHIPS:
                    yield Label(f"• {rel}", classes="relationship-item")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press events."""
        button_id = event.button.id
        if button_id and button_id.startswith("btn-run-"):
            db_path = CONFIG_DIR / "db.sqlite3"
            dt: DataTable[Any] = self.app.query_one("#sample-table", DataTable)  # type:ignore
            dt.clear(columns=True)
            table_name = button_id.replace("btn-run-", "").upper()
            sample_query = f"SELECT * FROM {table_name} LIMIT 5;"
            try:
                results = excute_db_query(db_path, sample_query)
                rows = results.get("rows", [])
                descriptions = results.get("descriptions", [])
                ui_table_handler(table=dt, headers=descriptions, rows=rows)

                self.app.query_one(TabbedContent).active = "sample-data-tab"  # type:ignore
            except Exception:
                pass
