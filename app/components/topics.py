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
        yield Markdown(id="topic-description")
        with Collapsible(title="Show Hints", collapsed=True):
            yield Label(id="topic-hints")

    def load_question(self, title: str, description: str, hint: str) -> None:
        """Update the panel with a new question."""
        self.border_title = f"Topic: {title}"
        self.query_one("#topic-description", Markdown).update(description)
        self.query_one("#topic-hints", Label).update(hint)
