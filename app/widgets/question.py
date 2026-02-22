from textual.app import ComposeResult
from textual.widgets import Label, ListItem

class Question(ListItem):
    def __init__(self, title: str) -> None:
        super().__init__()
        self.title = title

    def compose(self) -> ComposeResult:
        yield Label(self.title)