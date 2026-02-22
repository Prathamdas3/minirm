from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import DataTable, RichLog, TabbedContent, TabPane


class ConsolePanel(Container):
    def on_mount(self) -> None:
        self.border_title = "Results"

    def compose(self) -> ComposeResult:
        with TabbedContent(initial="console-tab"):
            with TabPane("Console", id="console-tab"):
                yield RichLog(id="console-log", markup=True)

            with TabPane("Sample Data", id="sample-data-tab"):
                yield DataTable(id="sample-data-table")