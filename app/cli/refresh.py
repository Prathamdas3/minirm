from app.constant import APP_NAME
from app.utils.handle_config_file import load_config
from pathlib import Path
from rich.prompt import Prompt
import typer
from app.db.init import db_init
from rich import print

refresh_app = typer.Typer()


@refresh_app.command(name="refresh")
def refresh(
    all_dbs: bool = typer.Option(
        False, "--all", "-a", help="Refresh all database without prompting"
    ),
):
    """
    This command will reseed your sqlite database with data
    """

    config = load_config()
    databases = config.get("databases", [])

    if not databases:
        print("[red]No databases found to refresh.[/red]")
        raise typer.Exit()

    if all_dbs:
        print(f"[bold red]Refreshing ALL {len(databases)} databases...[/bold red]")
        for db_path_str in databases:
            app_dir = Path(f"{db_path_str}/.{APP_NAME}")
            db_path = Path("f{app_dir}/db.sqlite3")

            if not app_dir.exists():
                print("No path directory found")
                raise typer.Exit(1)
            if db_path.exists():
                db_path.unlink()

            db_init(path=db_path)

        print("Successfully refeshed all the databases")
        return 
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

        # Validate indices
        valid_indices = [i for i in selected_indices if 0 <= i < len(databases)]
        if len(valid_indices) != len(selected_indices):
            print("[yellow]Warning: Some invalid indices were ignored.[/yellow]")

        if not valid_indices:
            print("[red]No valid databases selected.[/red]")
            return

        # Process deletion
        paths_to_refresh: list[str] = []
        for idx in valid_indices:
            paths_to_refresh.append(databases[idx])
        for db_path_str in databases:
            app_dir = Path(f"{db_path_str}/.{APP_NAME}")
            db_path = Path("f{app_dir}/db.sqlite3")

            if not app_dir.exists():
                print("No path directory found")
                raise typer.Exit(1)
            if db_path.exists():
                db_path.unlink()

            db_init(path=db_path)
            print("Successfully refeshed all the databases")
    except ValueError:
        print(
            "[bold red]Invalid input. Please enter numbers separated by spaces.[/bold red]"
        )
        raise typer.Exit(1)
