"""Sidebar panel for displaying questions and database controls."""

from textual.app import ComposeResult
from textual.containers import Container, VerticalScroll
from textual.widgets import Button, Collapsible, ListView, ListItem, Label
from typing import Any

from app.db.utils import create_or_refresh_db

QUESTIONS: dict[str, dict[str, Any]] = {
    "Easy": {
        "questions": ["Select All Users", "Find User by Id", "Count Users"],
        "options": {"collapsed": False},
    },
    "Medium": {
        "questions": ["Select All Users", "Find User by Id", "Count Users"],
        "options": {"collapsed": True},
    },
}


class Question(ListItem):
    """List item representing a SQL practice question."""

    def __init__(self, title: str) -> None:
        super().__init__()
        self.title = title

    def compose(self) -> ComposeResult:
        """Compose the question item."""
        yield Label(self.title)


class Sidebar(Container):
    """Sidebar panel containing questions list and refresh button."""

    def on_mount(self) -> None:
        """Called when the panel is mounted."""
        self.border_title = "Welcome!!"

    def compose(self) -> ComposeResult:
        """Compose the sidebar UI."""
        yield Button("Refresh DB", id="btn-refresh")

        c_questions = Container(id="questions", classes="card")
        c_questions.border_title = "Questions"
        with c_questions:
            with VerticalScroll():
                for key, data in QUESTIONS.items():
                    questions_list = data.get("questions", [])
                    collapsed = data.get("options", {}).get("collapsed", True)
                    with Collapsible(
                        title=str(key),
                        collapsed=collapsed,
                        classes="collapsible",
                        id=f"collapsible_{key.lower()}",
                    ):

                        with ListView():
                            for q in questions_list:
                                yield ListItem(Label(q))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press events to refresh the database."""
        if event.button.id == "btn-refresh":
            create_or_refresh_db()
            self.notify("Database refreshed successfully!",timeout=1)