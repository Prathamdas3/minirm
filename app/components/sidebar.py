"""Sidebar panel for displaying questions and database controls."""

from textual.app import ComposeResult
from textual.containers import Container, VerticalScroll
from textual.widgets import (
    Collapsible,
    ListView,
    ListItem,
    Label,
    DataTable,
    RichLog,
    TabbedContent,
)
from typing import Any

from app.components.topics import TopicPanel
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


class Sidebar(Container):
    """Sidebar panel containing questions list and refresh button."""

    def on_mount(self) -> None:
        """Called when the panel is mounted."""
        self.border_title = "Welcome!!"
        first_question = next(iter(QUESTIONS.values()))["questions"][0]
        self.app.query_one(  # type: ignore
            "#topic-area", TopicPanel
        ).border_title = f"Topic: {first_question}"

    def compose(self) -> ComposeResult:
        """Compose the sidebar UI."""
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

    def _reset_console(self) -> None:
        """Clear all console widgets and reset to console tab."""
        dt: DataTable[Any] = self.app.query_one("#console-table", DataTable)  # type: ignore
        sample_dt: DataTable[Any] = self.app.query_one("#sample-table", DataTable)  # type: ignore
        self.app.query_one("#console-log", RichLog).clear()  # type: ignore
        dt.clear(columns=True)
        dt.cursor_type = "none"
        dt.display = False
        sample_dt.clear(columns=True)
        sample_dt.cursor_type = "none"
        sample_dt.display = False
        tc = self.app.query_one(TabbedContent)  # type: ignore
        if tc.active == "sample-data-tab":
            tc.active = "console-tab"

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """Handle question selection to update topic and reset console."""
        create_or_refresh_db()
        label = event.item.query_one(Label)
        self.app.query_one(  # type: ignore
            "#topic-area", TopicPanel
        ).border_title = f"Topic: {label.render()}"
        self._reset_console()
