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
from app.questions.registry import get_by_difficulty


class Sidebar(Container):
    """Sidebar panel containing questions list and refresh button."""

    def on_mount(self) -> None:
        """Called when the panel is mounted."""
        self.border_title = "Welcome!!"

        by_difficulty = get_by_difficulty()
        if by_difficulty:
            first_question = next(iter(by_difficulty.values()))[0]
            self.app.query_one(  # type: ignore
                "#topic-area", TopicPanel
            ).load_question(
                title=first_question.title,
                description=first_question.description,
                hint=first_question.hint,
            )

    def compose(self) -> ComposeResult:
        DIFFICULTY_ORDER = ["Easy", "Medium", "Hard"]
        with VerticalScroll(id="questions-scroll"):
            questions = get_by_difficulty()
            if not questions:
                yield Label("No questions available.")
                return

            for difficulty in DIFFICULTY_ORDER:
                qs = questions.get(difficulty, [])
                if not qs:
                    continue
                with Collapsible(
                    title=difficulty,
                    collapsed=difficulty != "Easy",
                    classes="collapsible",
                    id=f"collapsible_{difficulty.lower()}",
                ):
                    with ListView():
                        for q in qs:
                            yield ListItem(Label(q.title))

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
        ).load_question(title=f"Topic: {label.render()}")
        self._reset_console()
