"""Schema panel for displaying database schemas."""

from textual.app import ComposeResult
from textual.containers import Container, VerticalScroll
from textual.widgets import Label
from app.widgets import SchemaDisplay
from app.constant import SCHEMAS, RELATIONSHIPS


class SchemasPanel(Container):
    """Panel for displaying database table schemas and relationships."""

    def on_mount(self) -> None:
        """Called when the panel is mounted."""
        self.border_title = "Database Schemas"

    def compose(self) -> ComposeResult:
        """Compose the panel UI."""
        with VerticalScroll():
            for table_name in SCHEMAS.keys():
                yield SchemaDisplay(
                    table_name=table_name, row_count=len(SCHEMAS.get(table_name, []))
                )

            yield Label("Relationships", classes="section-header")
            with Container(classes="relationships-container"):
                for rel in RELATIONSHIPS:
                    yield Label(f"• {rel}", classes="relationship-item")
