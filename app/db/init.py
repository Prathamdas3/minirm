from app.db.seed import seed_db
from pathlib import Path


def db_init(path: Path):
    package_dir = Path(__file__).parent
    try:
        seed_db(
            db_path=path,
            schema_path=package_dir / "sql/schema.sql",
            seed_path=package_dir / "sql/data.sql",
        )
    except Exception:
        raise
