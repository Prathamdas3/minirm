from rich.table import Table
from rich import print as rprint
from textual.widgets import DataTable
from typing import List, Any


def cli_table_handler(
    title: str, headers: List[str], rows: List[List[Any]], style: str = "bold green"
) -> None:
    """
    Renders a table in the CLI using rich.

    Args:
        title (str): The title of the table.
        headers (List[str]): A list of column headers.
        rows (List[List[Any]]): A list of rows, where each row is a list of values.
        style (str, optional): The style for the title. Defaults to "bold green".
    """
    table = Table(title=title)

    for header in headers:
        table.add_column(header, style="cyan")

    for row in rows:
        table.add_row(*[str(item) for item in row])

    rprint(f"[{style}]\nTable: {title}[/{style}]")
    rprint(table)


def ui_table_handler(
    table: DataTable[Any], headers: List[str], rows: List[List[Any]]
) -> None:
    """
    Renders a table in the TUI using textual.

    Args:
        table (DataTable): The DataTable widget to populate.
        headers (List[str]): A list of column headers.
        rows (List[List[Any]]): A list of rows, where each row is a list of values.
    """
    table.clear(columns=True)
    table.add_columns(*headers)
    table.add_rows(rows)
