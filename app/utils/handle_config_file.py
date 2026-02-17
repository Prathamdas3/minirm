from app.constant import CONFIG_DIR, CONFIG_FILE
import json
import typer
from pathlib import Path
from rich.prompt import Prompt


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


def get_selected_db_path(allow_destroy: bool = False):
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
