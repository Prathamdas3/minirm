from db.seed import seed_db
from pathlib import Path


def db_init(path: Path):
    try:
        seed_db(
            db_path=path,
            schema_path=Path("db/sql/schema.sql"),
            seed_path=Path("db/sql/seed.sql"),
        )
    except Exception:
        raise
