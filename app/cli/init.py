import typer
from pathlib import Path
from app.constant import HOME_DIR, APP_NAME
from typing import Annotated
from app.db.init import db_init
from app.utils.handle_config_file import load_config, save_config
from rich import print

init_app = typer.Typer()


@init_app.command(name="init")
def init(
    paths: Annotated[
        list[str], typer.Argument(help="Path for the sqlite initialization")
    ] = [HOME_DIR],
):
    """
    This command will initialize an temporary sqlite file. It will also create the tables along with filling it with temporary custom data.
    """
    for path in paths:
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

