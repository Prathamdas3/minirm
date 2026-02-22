"""Schema display widget for showing table structure."""

from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Button, Collapsible, DataTable
from app.constant import SCHEMAS
from app.utils import ui_table_handler


class SchemaDisplay(Container):
    """Widget for displaying a database table's schema in a collapsible."""

    def __init__(self, table_name: str, row_count: int = 0) -> None:
        super().__init__()
        self.table_name = table_name
        self.row_count = row_count

    def compose(self) -> ComposeResult:
        """Compose the schema display widget."""
        dt: DataTable = DataTable()
        columns = ["Column", "Type", "Constraints"]
        rows = [
            [col["column"], col["type"], col["constraints"]]
            for col in SCHEMAS.get(self.table_name, [])
        ]
        ui_table_handler(dt, columns, rows)

        with Collapsible(
            title=f"{self.table_name} ({self.row_count} rows)",
            classes="collapsible",
            collapsed=True,
        ):
            with Container(classes="schema-inner"):
                yield dt
                with Container(classes="sample-btn-container"):
                    yield Button(
                        "See Sample Data",
                        id=f"btn_sample_{self.table_name}",
                        classes="sample-btn",
                    )
