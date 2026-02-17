import typer
from app.utils.handle_config_file import get_selected_db_path, load_config, save_config
from app.constant import APP_NAME
import shutil
from rich import print


destroy_app = typer.Typer()


@destroy_app.command(name="destroy")
def destroy():
    """
    This command will destroy the preset sqlite file and remove it along with the data
    """
    try:
        project_path = get_selected_db_path()
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
