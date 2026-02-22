from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Button, TextArea


class SqlEditorPanel(Container):
    def on_mount(self) -> None:
        self.border_title = "SQL Query"

    def compose(self) -> ComposeResult:
        yield Button("Run Query", id="btn-run", classes="floating-run-btn")
        yield TextArea(language="sql", id="sql-editor", text="SELECT * FROM users;")
