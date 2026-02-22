from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Footer, Header, ListView
from app.panels import (
    Sidebar,
    TopicPanel,
    SqlEditorPanel,
    SchemasPanel,
    ConsolePanel,
    Question,
)
from app.styles import CSS


class MainApp(App):
    CSS = CSS
    TITLE = "minirm"
    BINDINGS = [
        Binding("q", "quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=False)
        yield Sidebar(id="sidebar", classes="card")
        yield TopicPanel(id="topic-area", classes="card")
        yield SqlEditorPanel(id="sql-area", classes="card")
        yield SchemasPanel(id="schemas-area", classes="card")
        yield ConsolePanel(id="console-area", classes="card")
        yield Footer()

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        question = event.item
        if isinstance(question, Question):
            self.query_one(
                "#topic-area", TopicPanel
            ).border_title = f"Topic: {question.title}"


if __name__ == "__main__":
    app = MainApp()
    app.run()
