"""Question widget for displaying SQL practice questions."""

from textual.app import ComposeResult
from textual.widgets import Label, ListItem


class Question(ListItem):
    """List item representing a SQL practice question."""

    def __init__(self, title: str) -> None:
        super().__init__()
        self.title = title

    def compose(self) -> ComposeResult:
        """Compose the question item."""
        yield Label(self.title)
