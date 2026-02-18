from app.cli.init import init_app
from app.cli.destroy import destroy_app
from app.cli.refresh import refresh_app
from app.cli.docs import doc_app
from app.cli.query import query_app
from app.cli.qa import qa_app
from typer import Typer

cli_app = Typer()

cli_app.add_typer(init_app)
cli_app.add_typer(destroy_app)
cli_app.add_typer(refresh_app)
cli_app.add_typer(doc_app)
cli_app.add_typer(query_app)
cli_app.add_typer(qa_app)