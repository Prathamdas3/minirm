import typer
from app.utils.handle_config_file import get_selected_db_path
from app.constant import APP_NAME
from app.db.engin import db_session
from app.utils.table import cli_table_handler
from rich import print
import sqlite3
from typing import Optional

doc_app = typer.Typer()


@doc_app.command(name="docs")
def docs(
    table_name: Optional[str] = typer.Argument(
        None, help="The name of the table to visualize"
    ),
    all_tables: bool = typer.Option(
        False, "--all", "-a", help="Show all tables and the relations"
    ),
    relation: bool = typer.Option(
        False, "--relation", "-r", help="Show only the relations"
    ),
):
    """
    This command is for getting tables and table structure and example data
    """
    project_path = get_selected_db_path()
    db_path = project_path / f".{APP_NAME}" / "db.sqlite3"

    if not db_path.exists():
        print("[bold red]Error:[/] Database not found. Please run 'init' first.")
        raise typer.Exit(1)

    with db_session(path=db_path) as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables_data = cursor.fetchall()
        tables = [t[0] for t in tables_data if t[0] != "sqlite_sequence"]

        if not tables:
            print("[yellow]No tables found in the database.[/yellow]")
            return

        # Case: Show only relations
        if relation:
            relations_list:list[list[str]] = []
            target_tables = [table_name] if table_name else tables

            # If table_name provided, check if it exists
            if table_name and table_name not in tables:
                print(f"[bold red]Error:[/] Table '{table_name}' not found.")
                return

            for t_name in target_tables:
                cursor.execute(f"PRAGMA foreign_key_list({t_name});")
                fks = cursor.fetchall()
                # fk structure: (id, seq, table, from, to, on_update, on_delete, match)
                # Relationship: ReferencedTable -> CurrentTable (One-to-Many usually)
                for fk in fks:
                    referenced_table = fk[2]
                    # Attempt to describe the relationship
                    # Parent (referenced) -> Child (current)
                    relations_list.append(
                        [f"{referenced_table} -> {t_name} (One-to-Many)"]
                    )

            if relations_list:
                cli_table_handler(
                    title="Database Relationships",
                    headers=["Relationship"],
                    rows=relations_list,
                )
            else:
                print("[yellow]No relationships found for selected table(s).[/yellow]")
            return

        # Case: List available tables (Default if no args)
        if not table_name and not all_tables:
            cli_table_handler(
                title="Available Tables",
                headers=["Table Name"],
                rows=[[t] for t in tables],
            )
            return

        # Case: Show details (All or Specific Table)
        target_tables_list = []
        if all_tables:
            target_tables_list = tables
        elif table_name:
            if table_name not in tables:
                print(f"[bold red]Error:[/] Table '{table_name}' not found.")
                return
            target_tables_list = [table_name]

        for t_name in target_tables_list:
            print(f"\n[bold green]Table: {t_name}[/bold green]")

            # Display Schema
            cli_table_handler(
                title=f"Schema for {t_name}",
                headers=["Column", "Type", "Nullable", "Primary Key"],
                rows=[
                    [
                        col[1],  # name
                        col[2],  # type
                        "YES" if not col[3] else "NO",  # notnull
                        "YES" if col[5] else "NO",  # pk
                    ]
                    for col in cursor.execute(
                        f"PRAGMA table_info({t_name});"
                    ).fetchall()
                ],
            )

            # Display Relationships (Foreign Keys)
            cursor.execute(f"PRAGMA foreign_key_list({t_name});")
            fks = cursor.fetchall()
            if fks:
                cli_table_handler(
                    title=f"Relationships for {t_name}",
                    headers=[
                        "Column",
                        "References Table",
                        "References Column",
                        "On Delete",
                    ],
                    rows=[
                        [
                            fk[3],  # from
                            fk[2],  # table
                            fk[4],  # to
                            fk[5],  # on_delete
                        ]
                        for fk in fks
                    ],
                )
            else:
                print(
                    f"[yellow]No foreign key relationships found for {t_name}.[/yellow]"
                )

            # Display Example Data
            try:
                cursor.execute(f"SELECT * FROM {t_name} LIMIT 3;")
                rows = cursor.fetchall()
                if rows:
                    cli_table_handler(
                        title=f"Example Data for {t_name}",
                        headers=[description[0] for description in cursor.description],
                        rows=rows,
                    )
                else:
                    print(f"[yellow]No example data found for {t_name}.[/yellow]")
            except sqlite3.OperationalError as e:
                print(
                    f"[bold red]Error fetching example data for {t_name}:[/bold red] {e}"
                )
