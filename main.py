import typer
from typing import Annotated
from pathlib import Path
import shutil
from rich import print
from db.init import db_init

app = typer.Typer()
HOME_DIR = str(Path.home())
APP_NAME = "miniorm"


@app.command(name="init")
def init(
    path: Annotated[
        str, typer.Argument(help="Path for the sqlite initialization")
    ] = HOME_DIR,
):
    """
    This command will initialize an temporary sqlite file. It will also create the tables along with filling it with temporary custom data.
    """
    if path != HOME_DIR:
        app_dir = Path(f"{HOME_DIR}/.{APP_NAME}")
        app_dir.mkdir(parents=True, exist_ok=True)
        with open(f"{HOME_DIR}/.{APP_NAME}/.metadata.txt", "w", encoding="UTF8") as f:
            f.write(f"{path}\n")

    app_dir = Path(f"{path}/.{APP_NAME}")
    app_dir.mkdir(parents=True, exist_ok=True)
    db_path = app_dir / "db.sqlite3"
    db_init(path=db_path)

    print("✔ Database initialized")
    print(f"✔ Location: {db_path}")


@app.command(name="destroy")
def destroy():
    """
    This command will destroy the preset sqlite file and remove it along with the data
    """
    with open(f"{HOME_DIR}/.{APP_NAME}/.metadata.txt", "r") as f:
        path = f.readline()
        path = path.strip()

    if not path:
        print("No path found ")
        raise typer.Exit(1)

    path = HOME_DIR if path == HOME_DIR else path
    app_dir = Path(f"{path}/.{APP_NAME}")

    if not app_dir.exists():
        print("No path directory found")
        raise typer.Exit(1)

    shutil.rmtree(app_dir)
    print("✔ Database removed successfully")


@app.command(name="refresh")
def refresh():
    """
    This command will reseed your sqlite database with data
    """
    with open(f"{HOME_DIR}/.{APP_NAME}/.metadata.txt", "r") as f:
        path = f.readline()
        path = path.strip()

    if not path:
        print("No path found ")
        raise typer.Exit(1)

    path = HOME_DIR if path == HOME_DIR else path
    app_dir = Path(f"{path}/.{APP_NAME}")
    if not app_dir.exists():
        print("No path directory found")
        raise typer.Exit(1)
    db_path = app_dir / "db.sqlite3"
    if db_path.exists():
        db_path.unlink()

    db_init(path=db_path)
    print("Successfully refeshed the db")


@app.command(name="db-docs")
def db_docs():
    """
    This command is for getting tables and table structure
    """


if __name__ == "__main__":
    app()
