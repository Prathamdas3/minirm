from textual.app import App, ComposeResult
from textual.containers import Container, VerticalScroll
from app.ui.styles import CSS
from app.constant import SCHEMAS, RELATIONSHIPS
from app.utils.handle_config_file import load_config
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
# import random


# class DBInputScreen(Screen):
#     def compose(self) -> ComposeResult:
#         yield Grid(
#             Label("Enter new Database Path:", id="dialog-title"),
#             Input(placeholder="/path/to/new.db", id="path-input"),
#             Button("Create/Open DB", variant="primary", id="btn-submit-db"),
#             Button("Cancel", variant="error", id="btn-cancel-db"),
#             id="dialog",
#         )

#     def on_button_pressed(self, event: Button.Pressed) -> None:
#         if event.button.id == "btn-submit-db":
#             path = self.query_one("#path-input", Input).value
#             if path:
#                 self.dismiss(path)
#             else:
#                 self.dismiss(None)
#         elif event.button.id == "btn-cancel-db":
#             self.dismiss(None)


class Question(ListItem):
    def __init__(self, title: str) -> None:
        super().__init__()
        self.title = title

    def compose(self) -> ComposeResult:
        yield Label(self.title)


class SchemaDisplay(Collapsible):
    def __init__(self, table_name: str, row_count: int = 0) -> None:
        super().__init__(
            title=f"{table_name} ({row_count} rows)",
            classes="collapsible",
            collapsed=True,
        )
        self.table_name = table_name

    def compose(self) -> ComposeResult:
        dt: DataTable[Any] = DataTable()
        dt.add_columns("Column", "Type", "Constraints")

        schema_data = SCHEMAS.get(self.table_name, [])
        for col in schema_data:
            dt.add_row(col["column"], col["type"], col["constraints"])

        yield dt
        with Container(classes="sample-btn-container"):
            yield Button(
                "See Sample Data",
                id=f"btn_sample_{self.table_name}",
                classes="sample-btn",
            )


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


class SQLApp(App):
    CSS = CSS
    TITLE = "minirm"
    BINDINGS = [
        Binding("q", "quit", "Quit"),
    ]

    # def _on_mount(self) -> None:
    #     self.databases = load_config()["databases"]
    #     self.current_db = self.databases[0]
    #     self.refresh_db_list()

    def refresh_db_list(self):
        ...
        # try:
        #     db_list = self.query_one("#db-list", VerticalScroll)
        #     db_list.remove_children()

        #     dbs = self.config.get("dbs", [])
        #     for i, db_path in enumerate(dbs):
        #         label_str = db_path
        #         if len(label_str) > 25:
        #             label_str = "..." + label_str[-22:]

        #         # Visual indicator for selection
        #         btn_classes = "db-path-label"
        #         if db_path == self.current_db:
        #             label_str = f"-> {label_str}"
        #             btn_classes += " selected-db"  # Can add style if needed

        #         with db_list:
        #             with Container(classes="db-item-row", id=f"db-row-{i}"):
        #                 yield Button(
        #                     label_str, id=f"btn-select-db-{i}", classes=btn_classes
        #                 )
        #                 yield Button(
        #                     "X", id=f"btn-remove-db-{i}", classes="remove-db-btn"
        #                 )
        # except Exception:
        #     pass

    def compose(self) -> ComposeResult:
        self.databases = load_config()["databases"]

        yield Header(show_clock=False)

        c_sidebar = Container(id="sidebar", classes="card")
        c_dblist = Container(id="db_list", classes="card")
        c_questions = Container(id="questions", classes="card")
        c_btns = Container(id="sidebar_buttons_container")
        c_sidebar.border_title = "Welcome!!"
        c_dblist.border_title = "Avaliable Databases"
        c_questions.border_title = "Questions"

        with c_sidebar:
            with c_btns:
                yield Button("Init New DB", id="btn-init-db", classes="sidebar_btn")
                yield Button("Refresh DB", id="btn-refresh", classes="sidebar_btn")

            with c_dblist:
                with VerticalScroll(id="db-list"):
                    Label("Hello world")
                    for idx, db in enumerate(self.databases):
                        yield Label(f"{idx + 1}. {db}")

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
        c_sql = Container(id="sql-area", classes="card")
        c_sql.border_title = "SQL Query"
        with c_sql:
            yield Button("Run Query", id="btn-run", classes="floating-run-btn")
            yield TextArea(language="sql", id="sql-editor", text="SELECT * FROM users;")

        # 4. Schemas Area (Middle Bottom)
        c_schemas = Container(id="schemas-area", classes="card")
        c_schemas.border_title = "Database Schemas"
        with c_schemas:
            with VerticalScroll():
                for table_name in SCHEMAS.keys():
                    yield SchemaDisplay(table_name)

                yield Label("Relationships", classes="section-header")
                with Container(classes="relationships-container"):
                    for rel in RELATIONSHIPS:
                        yield Label(f"• {rel}", classes="relationship-item")

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

    # def on_button_pressed(self, event: Button.Pressed) -> None:
    #     btn_id = event.button.id or ""

    #     if btn_id == "btn-init-db":
    #         def open_db(path: str | None) -> None:
    #             if path:
    #                 # Logic to check existing? helper handles it
    #                 try:
    #                     db_helper.init_new_db(path)
    #                     self.config = db_helper.load_config()
    #                     self.current_db = str(Path(path).expanduser().resolve()) # Ensure path match
    #                     self.refresh_db_list()
    #                     self.update_schema_display()
    #                 except Exception as e:
    #                     # Log error?
    #                     pass
    #         self.push_screen(DBInputScreen(), open_db)

    #     elif btn_id == "btn-refresh":
    #         self.refresh_db_list()
    #         self.update_schema_display()

    #     elif btn_id.startswith("btn-select-db-"):
    #         try:
    #             idx = int(btn_id.split("-")[-1])
    #             dbs = self.config.get("dbs", [])
    #             if 0 <= idx < len(dbs):
    #                 self.current_db = dbs[idx]
    #                 db_helper.set_current_db(self.current_db)
    #                 self.config = db_helper.load_config()
    #                 self.refresh_db_list()
    #                 self.update_schema_display()
    #         except:
    #             pass

    #     elif btn_id.startswith("btn-remove-db-"):
    #         try:
    #             idx = int(btn_id.split("-")[-1])
    #             dbs = self.config.get("dbs", [])
    #             if 0 <= idx < len(dbs):
    #                 path_to_remove = dbs[idx]
    #                 db_helper.remove_db(path_to_remove)
    #                 self.config = db_helper.load_config()
    #                 self.current_db = self.config.get("current_db")
    #                 self.refresh_db_list()
    #                 if self.current_db:
    #                     self.update_schema_display()
    #         except:
    #             pass

    #     elif btn_id == "btn-run":
    #         query = self.query_one("#sql-editor", TextArea).text
    #         log = self.query_one("#console-log", RichLog)
    #         log.clear()

    #         headers, rows, error = db_helper.execute_query(self.current_db, query)
    #         if error:
    #             log.write(f"[bold red]Error:[/]\n{error}")
    #         else:
    #             table = Table(title="Query Result")
    #             if headers:
    #                 for h in headers:
    #                     table.add_column(h, style="cyan")
    #                 for row in rows:
    #                     table.add_row(*[str(r) for r in row])
    #             else:
    #                  table.add_column("Info", style="green")
    #                  table.add_row("Success")

    #             log.write(table)

    #     elif "sample" in btn_id:
    #         table_name = btn_id.replace("btn_sample_", "")
    #         self.query_one(TabbedContent).active = "sample-data-tab"
    #         log = self.query_one("#console-log", RichLog)
    #         log.clear()

    #         query = f"SELECT * FROM {table_name} LIMIT 5"

    #         headers, rows, error = db_helper.execute_query(self.current_db, query)

    #         table_widget = self.query_one("#sample-data-table", DataTable)
    #         if error:
    #              log.write(f"[bold red]Error:[/]\n{error}")
    #         else:
    #              table_widget.clear(columns=True)
    #              table_widget.add_columns(*headers)
    #              table_widget.add_rows(rows)

    #              table = Table(title=f"Sample Data: {table_name}")
    #              for h in headers:
    #                  table.add_column(h, style="cyan")
    #              for row in rows:
    #                  table.add_row(*[str(r) for r in row])
    #              log.write(table)
