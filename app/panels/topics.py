from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Collapsible, Label, Markdown


class TopicPanel(Container):
    def on_mount(self) -> None:
        self.border_title = "Topic: Select Data"

    def compose(self) -> ComposeResult:
        yield Markdown(
            """**Problem Description**
                
Write a query to select all users from the `users` table.

Expected: `id`, `name`, `email`
            """
        )
        with Collapsible(title="Show Hints", collapsed=True):
            yield Label("Hint: Try using the SELECT statement.")