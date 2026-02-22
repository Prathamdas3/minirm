from textual.widgets import DataTable
from typing import List, Any



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
