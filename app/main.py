"""Main application module for minirm."""

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Footer
from app.db import create_or_refresh_db
from app.components import (
    Sidebar,
    TopicPanel,
    SqlEditorPanel,
    SchemasPanel,
    ConsolePanel,
)
from app.styles import CSS
from typing import Any



class MainApp(App[Any]):
    """Main application class for the minirm SQL practice TUI."""

    CSS = CSS
    TITLE = "minirm"
    BINDINGS = [
        Binding("q", "quit", "Quit"),
    ]

    def on_mount(self) -> None:
        """Called when the application is mounted."""
        create_or_refresh_db()

    def compose(self) -> ComposeResult:
        """Compose the application UI."""
        yield Sidebar(id="sidebar", classes="card")
        yield TopicPanel(id="topic-area", classes="card")
        yield SqlEditorPanel(id="sql-area", classes="card")
        yield SchemasPanel(id="schemas-area", classes="card")
        yield ConsolePanel(id="console-area", classes="card")
        yield Footer()


if __name__ == "__main__":
    app = MainApp()
    app.run()
