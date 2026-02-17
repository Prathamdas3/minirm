import typer
from app.utils.handle_config_file import get_selected_db_path
from app.constant import APP_NAME
from app.db.engin import db_session
from rich.table import Table
from rich import print
import sqlite3

doc_app = typer.Typer()


@doc_app.command(name="docs")
def db_docs():
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
        tables = cursor.fetchall()

        for table_name_tuple in tables:
            table_name = table_name_tuple[0]
            if table_name == "sqlite_sequence":  # Skip internal SQLite table
                continue

            print(f"[bold green]\nTable: {table_name}[/bold green]")

            # Display Schema
            schema_table = Table(title=f"Schema for {table_name}")
            schema_table.add_column("Column", style="cyan", no_wrap=True)
            schema_table.add_column("Type", style="magenta")
            schema_table.add_column("Nullable", style="blue")
            schema_table.add_column("Primary Key", style="green")

            cursor.execute(f"PRAGMA table_info({table_name});")
            for col in cursor.fetchall():
                schema_table.add_row(
                    col[1],  # name
                    col[2],  # type
                    "YES" if not col[3] else "NO",  # notnull
                    "YES" if col[5] else "NO",  # pk
                )
            print(schema_table)

            # Display Relationships (Foreign Keys)
            foreign_key_table = Table(title=f"Relationships for {table_name}")
            foreign_key_table.add_column("Column", style="cyan", no_wrap=True)
            foreign_key_table.add_column("References Table", style="magenta")
            foreign_key_table.add_column("References Column", style="blue")
            foreign_key_table.add_column("On Delete", style="green")

            cursor.execute(f"PRAGMA foreign_key_list({table_name});")
            fks = cursor.fetchall()
            if fks:
                for fk in fks:
                    foreign_key_table.add_row(
                        fk[3],  # from (column in current table)
                        fk[2],  # table (referenced table)
                        fk[4],  # to (column in referenced table)
                        fk[5],  # on_delete
                    )
                print(foreign_key_table)
            else:
                print(
                    f"[yellow]No foreign key relationships found for {table_name}.[/yellow]"
                )

            # Display Example Data
            example_data_table = Table(title=f"Example Data for {table_name}")
            try:
                cursor.execute(f"SELECT * FROM {table_name} LIMIT 3;")
                rows = cursor.fetchall()
                if rows:
                    # Add columns based on cursor description
                    for description in cursor.description:
                        example_data_table.add_column(description[0], style="bold cyan")
                    for row in rows:
                        example_data_table.add_row(*[str(item) for item in row])
                    print(example_data_table)
                else:
                    print(f"[yellow]No example data found for {table_name}.[/yellow]")
            except sqlite3.OperationalError as e:
                print(
                    f"[bold red]Error fetching example data for {table_name}:[/bold red] {e}"
                )
