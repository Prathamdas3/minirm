import typer
from app.utils.handle_config_file import load_config, save_config
from app.constant import APP_NAME, HOME_DIR
import shutil
from rich import print
from rich.prompt import Prompt
from pathlib import Path

destroy_app = typer.Typer()


@destroy_app.command(name="destroy")
def destroy(
    all_dbs: bool = typer.Option(
        False, "--all", "-a", help="Destroy all databases without prompting"
    ),
):
    """
    This command will destroy the preset sqlite file and remove it along with the data.
    Supports deleting all databases or selecting multiple interactively.
    """
    config = load_config()
    databases = config.get("databases", [])

    if not databases:
        print("[red]No databases found to destroy.[/red]")
        raise typer.Exit()

    # Case: --all flag provided
    if all_dbs:
        print(f"[bold red]Destroying ALL {len(databases)} databases...[/bold red]")
        for db_path_str in databases:
            db_path = (
                Path(db_path_str)
                if Path(db_path_str) != Path(HOME_DIR)
                else Path(f"{db_path_str}/.{APP_NAME}")
            )
            if db_path.exists():
                shutil.rmtree(db_path)
                print(f"✔ Removed {db_path}")
            else:
                print(f"[yellow]Skipped (not found): {db_path}[/yellow]")

        # Clear config
        config["databases"] = []
        save_config(config)
        print("[bold green]All databases destroyed successfully.[/bold green]")
        return

    # Case: Interactive selection
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
        # Parse selection
        selected_indices = [
            int(x.strip()) - 1 for x in choice.replace(",", " ").split()
        ]

        # Validate indices
        valid_indices = [i for i in selected_indices if 0 <= i < len(databases)]
        if len(valid_indices) != len(selected_indices):
            print("[yellow]Warning: Some invalid indices were ignored.[/yellow]")

        if not valid_indices:
            print("[red]No valid databases selected.[/red]")
            return

        # Process deletion in reverse order to avoid index shifting issues during list modification
        # actually simpler: collect paths to remove, then remove from config

        paths_to_remove: list[str] = []
        for idx in valid_indices:
            paths_to_remove.append(databases[idx])

        for db_path_str in paths_to_remove:
            db_path = (
                Path(db_path_str)
                if Path(db_path_str) != Path(HOME_DIR)
                else Path(f"{db_path_str}/.{APP_NAME}")
            )
            if db_path.exists():
                shutil.rmtree(db_path)
                print(f"✔ Removed {db_path}")
            else:
                print(f"[yellow]Skipped (not found): {db_path}[/yellow]")

            # Remove from config list
            if db_path_str in config["databases"]:
                config["databases"].remove(db_path_str)

        save_config(config)
        print("[bold green]Selected databases destroyed successfully.[/bold green]")

    except ValueError:
        print(
            "[bold red]Invalid input. Please enter numbers separated by spaces.[/bold red]"
        )
        raise typer.Exit(1)
