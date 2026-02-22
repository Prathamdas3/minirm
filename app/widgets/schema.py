from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Button, Collapsible, DataTable
from typing import Any
from app.constant import SCHEMAS

class SchemaDisplay(Collapsible):
    def __init__(self, table_name: str, row_count: int = 0) -> None:
        super().__init__(
            title=f"{table_name} ({row_count} rows)",
            classes="collapsible",
            collapsed=True,
        )
        self.table_name = table_name

    def compose(self) -> ComposeResult:
        dt: DataTable[Any] = DataTable()
        dt.add_columns("Column", "Type", "Constraints")
        for col in SCHEMAS.get(self.table_name, []):
            dt.add_row(col["column"], col["type"], col["constraints"])
        yield dt
        with Container(classes="sample-btn-container"):
            yield Button(
                "See Sample Data",
                id=f"btn_sample_{self.table_name}",
                classes="sample-btn",
            )