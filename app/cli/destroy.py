import typer
from app.utils.handle_config_file import load_config, save_config
from app.constant import APP_NAME, HOME_DIR
import shutil
from rich import print
from rich.prompt import Prompt
from pathlib import Path

destroy_app = typer.Typer()


def _delete_db(project_path: Path) -> None:
    """
    Deletes the internal DB folder inside project_path.
    If the project folder was created solely for the DB (nothing else inside),
    removes the project folder too. Never removes HOME_DIR.
    """
    internal_db_path = project_path / f".{APP_NAME}"

    if not internal_db_path.exists():
        print(f"[yellow]Internal DB not found at: {internal_db_path}. Skipping.[/yellow]")
        return

    # Check what else lives in the project folder (ignore .DS_Store)
    other_contents = [
        f for f in project_path.iterdir()
        if f.name != ".DS_Store" and f != internal_db_path
    ]

    # Always remove the internal DB folder
    shutil.rmtree(internal_db_path)
    print(f"✔ Removed internal DB at {internal_db_path}")

    # If nothing else was in the project folder, remove it too
    # (but never remove HOME_DIR)
    if not other_contents and project_path != Path(HOME_DIR):
        shutil.rmtree(project_path)
        print(f"✔ Removed project directory {project_path} (it only contained the DB)")
    elif other_contents:
        print(f"[yellow]Kept project directory {project_path} (contains other files)[/yellow]")


@destroy_app.command(name="destroy")
def destroy(
    all_dbs: bool = typer.Option(
        False, "--all", "-a", help="Destroy all databases without prompting"
    ),
):
    """
    Destroy one or more tracked sqlite databases.
    If the project folder only contained the DB, it is removed too.
    If the project folder has other content, only the DB folder is removed.
    """
    config = load_config()
    databases = config.get("databases", [])

    if not databases:
        print("[red]No databases found to destroy.[/red]")
        raise typer.Exit()

    # ── Case: --all flag ──────────────────────────────────────────────────────
    if all_dbs:
        print(f"[bold red]Destroying ALL {len(databases)} databases...[/bold red]")
        for db_path_str in databases:
            _delete_db(Path(db_path_str))

        config["databases"] = []
        save_config(config)
        print("[bold green]All databases destroyed successfully.[/bold green]")
        return

    # ── Case: Interactive selection ───────────────────────────────────────────
    print("[cyan]Found the following databases:[/cyan]")
    for idx, path in enumerate(databases):
        print(f"{idx + 1}. {path}")

    choice = Prompt.ask(
        "Enter the numbers of the databases to destroy (separated by space, e.g., '1 3')",
        default="",
    )

    if not choice.strip():
        print("[yellow]No selection made. Exiting.[/yellow]")
        return

    try:
        selected_indices = [
            int(x.strip()) - 1 for x in choice.replace(",", " ").split()
        ]

        valid_indices = [i for i in selected_indices if 0 <= i < len(databases)]
        if len(valid_indices) != len(selected_indices):
            print("[yellow]Warning: Some invalid indices were ignored.[/yellow]")

        if not valid_indices:
            print("[red]No valid databases selected.[/red]")
            return

        for idx in valid_indices:
            db_path_str = databases[idx]
            _delete_db(Path(db_path_str))
            config["databases"].remove(db_path_str)

        save_config(config)
        print("[bold green]Selected databases destroyed successfully.[/bold green]")

    except ValueError:
        print("[bold red]Invalid input. Please enter numbers separated by spaces.[/bold red]")
        raise typer.Exit(1)
