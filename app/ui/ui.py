from textual.app import App, ComposeResult
from textual.containers import Container, VerticalScroll, Horizontal
from app.ui.styles import CSS
from textual.widgets import (
    Button,
    Label,
    TextArea,
    Collapsible,
    ListView,
    ListItem,
    DataTable,
    RichLog,
    Markdown,
    TabbedContent,
    TabPane,
    Header,
    Footer,
)
from textual.binding import Binding
from typing import Any


class Question(ListItem):
    def __init__(self, title: str) -> None:
        super().__init__()
        self.title = title

    def compose(self) -> ComposeResult:
        yield Label(self.title)


class SchemaDisplay(Collapsible):
    def __init__(self, table_name: str, row_count: int = 0) -> None:
        super().__init__(
            title=f"Schema: {table_name} ({row_count} rows)",
            classes="collapsible",
            collapsed=True,
        )
        self.table_name = table_name

    def compose(self) -> ComposeResult:
        # Placeholder for schema table
        dt: DataTable[Any] = DataTable()
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


QUESTIONS:dict[str,dict[str,Any]] = {
    "Easy": {
        "questions": ["Select All Users", "Find User by Id", "Count Users"],
        "options": {"collapsed": False},
    },
    "Medium": {
        "questions": ["Select All Users", "Find User by Id", "Count Users"],
        "options": {"collapsed": True},
    },
}


class SQLApp(App):
    CSS = CSS
    TITLE = "minirm"
    BINDINGS = [
        Binding("q", "quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=False)

        c_sidebar = Container(id="sidebar", classes="card")
        c_sidebar.border_title = "Questions"
        with c_sidebar:
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
                        yield ListView(*[Question(title=q) for q in questions_list])

        # 2. Topic Area (Middle Top)
        c_topic = Container(id="topic-area", classes="card")
        c_topic.border_title = "Topic: Select Data"
        with c_topic:
            yield Markdown(
                """**Problem Description**
                
Write a query to select all users from the `users` table.

Expected: `id`, `name`, `email`
                """
            )
            with Collapsible(title="Show Hints", collapsed=True):
                yield Label("Hint: Try using the SELECT statement.")

        # 3. SQL Area (Right Top)
        c_sql=TextArea(classes="card", language="sql",text="SELECT * FROM users;")
        c_sql.border_title="SQL Query"
        yield c_sql
        # c_sql = Container(id="sql-area", classes="card")
        # c_sql.border_title = "SQL Query"
        # with c_sql:
        #     # with Horizontal(classes="sql-toolbar"):
        #     #     yield Button("Run Query", id="btn-run")
        #     yield TextArea(language="sql", id="sql-editor", text="SELECT * FROM users;")

        # 4. Schemas Area (Middle Bottom) Need to fix the schema section 
        # c_schemas = Container(id="schemas-area", classes="card")
        # c_schemas.border_title = "Database Schemas"
        # with c_schemas:
        #     with VerticalScroll():
        #         yield SchemaDisplay("users", row_count=150)
        #         yield SchemaDisplay("posts", row_count=5000)

        # 5. Console Area (Right Bottom)
        c_console = Container(id="console-area", classes="card")
        c_console.border_title = "Results"
        with c_console:
            with TabbedContent(initial="console-tab"):
                with TabPane("Console", id="console-tab"):
                    yield RichLog(id="console-log", markup=True)

                with TabPane("Sample Data", id="sample-data-tab"):
                    yield DataTable(id="sample-data-table")


        yield Footer()

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        question = event.item
        if isinstance(question, Question):
            self.query_one(
                "#topic-area", Container
            ).border_title = f"Topic: {question.title}"

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-run":
            query = self.query_one("#sql-editor", TextArea).text
            log = self.query_one("#console-log", RichLog)
            log.write(f"[bold green]Running Query:[/]\n{query}")
            # Mock execution
            log.write(
                "[bold cyan]Result:[/]\n(1, 'Alice', 'alice@example.com')\n(2, 'Bob', 'bob@example.com')"
            )

        elif "sample" in str(event.button.id):
            # Extract table name from button id
            table_name = str(event.button.id).replace("btn_sample_", "")

            # Switch to Sample Data tab
            self.query_one(TabbedContent).active = "sample-data-tab"

            # Populate table (mock)
            table = self.query_one("#sample-data-table", DataTable)
            table.clear(columns=True)
            if table_name == "users":
                table.add_columns("ID", "Name", "Email")
                table.add_rows(
                    [(1, "Alice", "alice@example.com"), (2, "Bob", "bob@example.com")]
                )
            elif table_name == "posts":
                table.add_columns("ID", "Title", "Content")
                table.add_rows([(1, "Post 1", "Content 1"), (2, "Post 2", "Content 2")])

            log = self.query_one("#console-log", RichLog)
            log.write(f"[bold magenta]Showing sample data for {table_name}...[/]")
