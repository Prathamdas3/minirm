import typer
from typing import Annotated
from pathlib import Path
import shutil
import json
from rich import print
from rich.table import Table
from rich.prompt import Prompt

from db.init import db_init
from db.engin import db_session
import sqlite3

app = typer.Typer()
HOME_DIR = str(Path.home())
APP_NAME = "miniorm"
CONFIG_DIR = Path.home() / ".miniorm"
CONFIG_FILE = CONFIG_DIR / "config.json"


def load_config() -> dict[str, list[str]]:
    if not CONFIG_FILE.exists():
        return {"databases": []}
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {"databases": []}


def save_config(config: dict[str, list[str]]):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)


def _get_selected_db_path(allow_destroy: bool = False):
    config = load_config()
    databases = config.get("databases", [])

    if not databases:
        print("[red]No databases found. Run 'init' first.[/red]")
        raise typer.Exit(1)

    if len(databases) == 1:
        return Path(databases[0])

    print("[cyan]Multiple databases found. Please select one:[/cyan]")
    for idx, path in enumerate(databases):
        print(f"{idx + 1}. {path}")

    choice = Prompt.ask(
        "Enter the number of the database",
        choices=[str(i + 1) for i in range(len(databases))],
    )
    return Path(databases[int(choice) - 1])


@app.command(name="init")
def init(
    path: Annotated[
        str, typer.Argument(help="Path for the sqlite initialization")
    ] = HOME_DIR,
):
    """
    This command will initialize an temporary sqlite file. It will also create the tables along with filling it with temporary custom data.
    """
    target_path = Path(path).resolve()
    app_dir = target_path / f".{APP_NAME}"
    app_dir.mkdir(parents=True, exist_ok=True)
    db_path = app_dir / "db.sqlite3"

    # Initialize DB
    db_init(path=db_path)

    # Update Config
    config = load_config()
    str_path = str(target_path)
    if str_path not in config["databases"]:
        config["databases"].append(str_path)
        save_config(config)

    print("✔ Database initialized")
    print(f"✔ Location: {db_path}")


@app.command(name="destroy")
def destroy():
    """
    This command will destroy the preset sqlite file and remove it along with the data
    """
    try:
        project_path = _get_selected_db_path()
    except typer.Exit:
        return

    app_dir = project_path / f".{APP_NAME}"

    if not app_dir.exists():
        print("No path directory found on disk")
        # We might still want to remove it from config if it doesn't exist
    else:
        shutil.rmtree(app_dir)
        print("✔ Database removed successfully")

    # Remove from config
    config = load_config()
    str_path = str(project_path)
    if str_path in config["databases"]:
        config["databases"].remove(str_path)
        save_config(config)


@app.command(name="refresh")
def refresh():
    """
    This command will reseed your sqlite database with data
    """
    project_path = _get_selected_db_path()
    app_dir = project_path / f".{APP_NAME}"
    db_path = app_dir / "db.sqlite3"

    if not app_dir.exists():
        print("No path directory found")
        raise typer.Exit(1)

    if db_path.exists():
        db_path.unlink()

    db_init(path=db_path)
    print("Successfully refeshed the db")


@app.command(name="db-docs")
def db_docs():
    """
    This command is for getting tables and table structure and example data
    """
    project_path = _get_selected_db_path()
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


if __name__ == "__main__":
    app()
