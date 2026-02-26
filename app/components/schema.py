"""Schema panel for displaying database schemas."""

from pathlib import Path

from textual.app import ComposeResult
from textual.containers import Container, VerticalScroll
from textual.widgets import Button, Collapsible, DataTable, Label, TabbedContent
from app.db import excute_db_query
from app.db.engin import db_session
from app.db.utils import create_or_refresh_db
from app.utils import ui_table_handler
from typing import Any
from app.constant import CONFIG_DIR


def get_db_schema(db_path: Path) -> tuple[dict[str, list[dict[str, str]]], list[str]]:
    """Get database schema dynamically from SQLite.

    Args:
        db_path: Path to the SQLite database file.

    Returns:
        A tuple of (schemas dict, relationships list).
    """
    schemas: dict[str, list[dict[str, str]]] = {}
    relationships: list[str] = []

    with db_session(path=db_path) as conn:
        cursor = conn.cursor()

        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';"
        )
        tables = [row[0] for row in cursor.fetchall()]

        for table in tables:
            cursor.execute(f"PRAGMA table_info({table})")
            columns: list[dict[str, Any]] = []
            for col in cursor.fetchall():
                col_name = col[1]
                col_type = col[2] or "TEXT"
                col_pk = "PRIMARY KEY" if col[5] else ""
                col_notnull = "NOT NULL" if col[3] else ""
                constraints = (
                    " ".join(filter(None, [col_pk, col_notnull])).strip() or "NULL"
                )
                columns.append(
                    {"column": col_name, "type": col_type, "constraints": constraints}
                )
            schemas[table] = columns

            cursor.execute(f"PRAGMA foreign_key_list({table})")
            fks = cursor.fetchall()
            for fk in fks:
                from_col = fk[3]
                to_table = fk[2]
                to_col = fk[4]
                relationships.append(f"{table}.{from_col} -> {to_table}.{to_col}")

    return schemas, relationships


class SchemasPanel(Container):
    """Panel for displaying database table schemas and relationships."""

    def on_mount(self) -> None:
        """Called when the panel is mounted."""
        self.border_title = "Database Schemas"

    def compose(self) -> ComposeResult:
        """Compose the panel UI."""
        create_or_refresh_db()
        db_path = CONFIG_DIR / "db.sqlite3"
        schemas, relationships = get_db_schema(db_path)
        
        with VerticalScroll(id="schemas-scroll"):
            for table_name in schemas.keys():
                with Collapsible(
                    title=f"{table_name} ({len(schemas.get(table_name, []))} columns)",
                    classes="collapsible",
                    collapsed=True,
                    id=f"collapsible_{table_name.lower()}",
                ):
                    dt: DataTable[Any] = DataTable(classes="schema-table")
                    columns = ["Column", "Type", "Constraints"]
                    rows = [
                        [col["column"], col["type"], col["constraints"]]
                        for col in schemas.get(table_name, [])
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
                for rel in relationships:
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
