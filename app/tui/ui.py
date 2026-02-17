from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.widgets import (
    Button,
    Footer,
    Header,
    Label,
    TextArea,
    Collapsible,
    ListView,
    ListItem,
    DataTable,
    RichLog,
    Markdown,
)
from textual.binding import Binding


class Question(ListItem):
    def __init__(self, title: str) -> None:
        super().__init__()
        self.title = title

    def compose(self) -> ComposeResult:
        yield Label(self.title)


class SchemaDisplay(Collapsible):
    def __init__(self, table_name: str) -> None:
        super().__init__(title=f"Schema: {table_name}")
        self.table_name = table_name

    def compose(self) -> ComposeResult:
        # Placeholder for schema table
        dt = DataTable()
        dt.add_columns("Column", "Type", "Nullable")
        dt.add_rows(
            [
                ("id", "INTEGER", "NO"),
                ("name", "TEXT", "YES"),
                ("created_at", "DATETIME", "YES"),
            ]
        )
        yield dt
        yield Button(
            "See Sample Data", id=f"btn_sample_{self.table_name}", classes="sample-btn"
        )


class SQLApp(App):
    CSS = """
    Screen {
        layout: grid;
        grid-size: 3;
        grid-columns: 20% 40% 40%;
        background: $surface;
    }

    /* Left Sidebar - Questions */
    #sidebar {
        dock: left;
        width: 100%;
        height: 100%;
        border-right: solid $primary;
        background: $surface-darken-1;
        padding: 1;
    }

    .sidebar-title {
        text-align: center;
        text-style: bold;
        background: $primary;
        color: $text;
        padding: 1;
        margin-bottom: 1;
    }

    #sidebar ListView {
        height: auto;
        margin-bottom: 1; 
        border: solid $secondary;
        background: $surface;
    }

    /* Center Panel - Context */
    #center-panel {
        height: 100%;
        padding: 1 2;
        border-right: solid $primary;
        overflow-y: auto;
    }

    .topic-title {
        text-align: center;
        text-style: bold;
        background: $secondary;
        color: $text;
        padding: 1;
        margin-bottom: 1;
        border: wide $primary;
    }

    .problem-desc {
        background: $surface-lighten-1;
        padding: 1;
        margin-bottom: 2;
        border: solid $accent;
        height: auto;
        min-height: 10;
    }

    .section-title {
        text-style: bold;
        color: $accent;
        margin-top: 1;
        margin-bottom: 1;
    }

    /* Right Panel - Execution */
    #right-panel {
        height: 100%;
        padding: 1 2;
        display: flex;
        flex-direction: column;
    }

    #sql-editor {
        height: 1fr;
        min-height: 10;
        border: solid $accent;
        margin-bottom: 1;
    }

    #console-log {
        height: 1fr;
        min-height: 10;
        border: solid $success;
        background: $surface-darken-1;
        overflow-y: auto;
    }

    .button-row {
        height: auto;
        margin-bottom: 1;
        align: center middle;
    }

    #btn-run {
        width: 45%;
        background: $success;
        color: $text;
        margin-right: 2;
    }

    #btn-hints {
        width: 45%;
        background: $warning;
        color: $surface;
    }
    
    .sample-btn {
        margin-top: 1;
        width: 100%;
    }
    """

    BINDINGS = [
        Binding("q", "quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()

        # Left Sidebar: Questions
        with Vertical(id="sidebar"):
            yield Label("Questions List", classes="sidebar-title")
            with VerticalScroll():
                with Collapsible(title="Easy", collapsed=False):
                    yield ListView(
                        Question("Select All Users"),
                        Question("Find User by ID"),
                        Question("Count Users"),
                    )
                with Collapsible(title="Medium", collapsed=True):
                    yield ListView(
                        Question("Join Tables"),
                        Question("Group By"),
                    )

        # Center Panel: Problem, Topic, Schemas
        with Vertical(id="center-panel"):
            yield Label("Topic: Select Data", classes="topic-title")

            yield Markdown(
                """# Problem Description
Write a query to select all users from the `users` table.

### Expected Output
- **id** (Integer)
- **name** (String)
- **email** (String)
                """,
                classes="problem-desc",
            )

            yield Label("Database Schemas", classes="section-title")
            yield SchemaDisplay("users")
            yield SchemaDisplay("posts")

        # Right Panel: SQL Editor, Console
        with Vertical(id="right-panel"):
            yield Label("SQL Query", classes="section-title")
            yield TextArea(language="sql", id="sql-editor", text="SELECT * FROM users;")

            with Horizontal(classes="button-row"):
                yield Button("Run Query", id="btn-run")
                yield Button("Show Hints", id="btn-hints")

            yield Label("Query Response Console", classes="section-title")
            yield RichLog(id="console-log", markup=True)

        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-run":
            query = self.query_one("#sql-editor", TextArea).text
            log = self.query_one("#console-log", RichLog)
            log.write(f"[bold green]Running Query:[/]\n{query}")
            # Mock execution
            log.write(
                "[bold cyan]Result:[/]\n(1, 'Alice', 'alice@example.com')\n(2, 'Bob', 'bob@example.com')"
            )

        elif event.button.id == "btn-hints":
            log = self.query_one("#console-log", RichLog)
            log.write("[bold yellow]Hint:[/] Try using the SELECT statement.")

        elif "sample" in str(event.button.id):
            log = self.query_one("#console-log", RichLog)
            log.write("[bold magenta]Showing sample data for table...[/]")


if __name__ == "__main__":
    app = SQLApp()
    app.run()
