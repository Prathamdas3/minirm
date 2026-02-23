"""Database seeding functionality."""

from pathlib import Path
from typing import Optional
from app.db.engin import db_session


def seed_db(db_path: Path, seed_path: Optional[Path], schema_path: Path) -> None:
    """Seed the database with schema and initial data.

    Args:
        db_path: Path to the SQLite database file.
        seed_path: Path to the SQL file containing seed data.
        schema_path: Path to the SQL file containing schema definitions.
    """
    with db_session(path=db_path) as conn:
        cursor = conn.cursor()

        cursor.executescript(schema_path.read_text())

        if seed_path:
            cursor.executescript(seed_path.read_text())
