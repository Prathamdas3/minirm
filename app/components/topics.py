"""Topic panel for displaying problem descriptions."""

from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Collapsible, Label, Markdown


class TopicPanel(Container):
    """Panel for displaying the current problem description and hints."""

    def on_mount(self) -> None:
        """Called when the panel is mounted."""
        self.border_title = "Topic: Select Data"

    def compose(self) -> ComposeResult:
        """Compose the panel UI."""
        yield Markdown(
            """**Problem Description**
                
Write a query to select all users from the `users` table.

Expected: `id`, `name`, `email`
            """
        )
        with Collapsible(title="Show Hints", collapsed=True):
            yield Label("Hint: Try using the SELECT statement.")
