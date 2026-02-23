"""Console panel for displaying query results."""

from textual.app import ComposeResult
from textual.widgets import DataTable, TabbedContent, TabPane, RichLog
from textual.containers import VerticalScroll,Container


class ConsolePanel(Container):
    """Panel for displaying query results with console and sample data tabs."""

    def on_mount(self) -> None:
        """Called when the panel is mounted."""
        self.border_title = "Results"

    def compose(self) -> ComposeResult:
        """Compose the panel UI."""
        with TabbedContent(initial="console-tab"):
            with TabPane("Console", id="console-tab"):
                yield RichLog(id="console-log", markup=True,max_lines=1)
                with VerticalScroll():
                    yield DataTable(id="console-table", classes="dt_table")

            with TabPane("Sample Data", id="sample-data-tab"):
                with VerticalScroll():
                    yield DataTable(id="sample-table",classes="dt_table")
