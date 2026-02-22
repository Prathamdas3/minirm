"""Database utility functions for the minirm application."""

from typing import Any

from app.constant import CONFIG_DIR
from app.db.seed import seed_db
from pathlib import Path
import shutil


def db_init(path: Path) -> None:
    """Initialize the database with schema and seed data.

    Args:
        path: Path to the SQLite database file.
    """
    package_dir = Path(__file__).parent
    try:
        seed_db(
            db_path=path,
            schema_path=package_dir / "sql/schema.sql",
            seed_path=package_dir / "sql/data.sql",
        )
    except Exception:
        raise


def create_or_refresh_db() -> None:
    """Create a fresh database or refresh the existing one by deleting and recreating."""
    if CONFIG_DIR.exists():
        shutil.rmtree(CONFIG_DIR)

    CONFIG_DIR.mkdir(exist_ok=True, parents=True)
    db_path = CONFIG_DIR / "db.sqlite3"
    db_init(db_path)


def excute_db_query(db_path: Path, query: str) -> dict[str, Any]:
    """Execute a SQL query against the database.

    Args:
        db_path: Path to the SQLite database file.
        query: The SQL query string to execute.

    Returns:
        A dictionary containing:
        - rows: List of result rows
        - descriptions: List of column names
        - error: Error message if query failed, empty string otherwise
    """
    from app.db.engin import db_session

    error = ""
    rows = []
    descriptions:list[str] = []

    with db_session(path=db_path) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(query)
            rows = cursor.fetchall()
            descriptions = (
                [desc[0] for desc in cursor.description] if cursor.description else []
            )
        except Exception as e:
            error = str(e)

    return {"rows": rows, "descriptions": descriptions, "error": error}
