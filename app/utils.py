"""Utility functions for the minirm application."""

from textual.widgets import DataTable
from typing import List, Any


def ui_table_handler(
    table: DataTable[Any], headers: List[str], rows: List[List[Any]]
) -> DataTable[Any]:
    """Render a table in the TUI using textual.

    Args:
        table: The DataTable widget to populate.
        headers: A list of column headers.
        rows: A list of rows, where each row is a list of values.

    Returns:
        The populated DataTable widget.
    """
    table.clear(columns=True)
    table.add_columns(*headers)
    table.add_rows(rows)
    return table
