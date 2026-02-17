import typer
from app.cli import cli_app


app = typer.Typer()


@app.callback(invoke_without_command=True)
def main(
    ui: bool = typer.Option(False, "--ui", help="Launch the UI"),
):
    if ui:
        from app.ui.ui import SQLApp

        app_ui = SQLApp()
        app_ui.run()
        raise typer.Exit


app.add_typer(cli_app)

if __name__ == "__main__":
    app()
