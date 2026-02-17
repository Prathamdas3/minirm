from app.constant import APP_NAME
from app.utils.handle_config_file import get_selected_db_path
import typer
from app.db.init import db_init
from rich import print

refresh_app = typer.Typer()


@refresh_app.command(name="refresh")
def refresh():
    """
    This command will reseed your sqlite database with data
    """
    project_path = get_selected_db_path()
    app_dir = project_path / f".{APP_NAME}"
    db_path = app_dir / "db.sqlite3"

    if not app_dir.exists():
        print("No path directory found")
        raise typer.Exit(1)

    if db_path.exists():
        db_path.unlink()

    db_init(path=db_path)
    print("Successfully refeshed the db")
