from pathlib import Path
from app.db.engin import db_session


def seed_db(db_path: Path, seed_path: Path, schema_path: Path):
    with db_session(path=db_path) as conn:
        cursor = conn.cursor()

        cursor.executescript(schema_path.read_text())

        if seed_path:
            cursor.executescript(seed_path.read_text())
