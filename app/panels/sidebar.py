from textual.app import ComposeResult
from textual.containers import Container, VerticalScroll
from textual.widgets import Button, Collapsible, ListView, ListItem, Label
from typing import Any

# Keep QUESTIONS here or move to app/constant.py
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
    def __init__(self, title: str) -> None:
        super().__init__()
        self.title = title

    def compose(self) -> ComposeResult:
        yield Label(self.title)


class Sidebar(Container):
    def on_mount(self) -> None:
        self.border_title = "Welcome!!"

    def compose(self) -> ComposeResult:
        yield Button("Refresh DB", id="btn-refresh", classes="sidebar_btn")

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
                        yield ListView(
                            *[Question(title=q) for q in questions_list]
                        )