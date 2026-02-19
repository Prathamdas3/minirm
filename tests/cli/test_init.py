from typer.testing import CliRunner
from app.cli.init import init_app
from app.utils.handle_config_file import load_config
from app.constant import APP_NAME

from pathlib import Path


runner = CliRunner()


def test_init_default():
    result = runner.invoke(init_app, [])
    assert result.exit_code == 0, (
        f"Exit code: {result.exit_code}\nOutput: {result.output}"
    )


def test_init_custom_path():
    result = runner.invoke(init_app, [str(".")])
    if result.exception:
        raise result.exception
    assert result.exit_code == 0, (
        f"Exit code: {result.exit_code}\nOutput: {result.output}"
    )
    db_path = Path(".").resolve() / f".{APP_NAME}" / "db.sqlite3"
    assert f"✔ Location: \n{db_path}" in result.output, (
        f"Expected string not found in:\n{repr(result.output)}"
    )


def test_db_exists():
    runner.invoke(init_app, [str(".")])
    assert (Path(".").resolve() / f".{APP_NAME}" / "db.sqlite3").exists()


def test_app_dir():
    runner.invoke(init_app, [str(".")])
    assert (Path(".").resolve() / f".{APP_NAME}").is_dir()


def test_twice_same_path(tmp_path: Path):
    runner.invoke(init_app, [str(tmp_path)])
    result = runner.invoke(init_app, [str(tmp_path)])
    assert result.exit_code == 0


def test_init_updates_config(tmp_path: Path):
    runner.invoke(init_app, [str(tmp_path)])
    config = load_config()
    assert str(tmp_path) in config["databases"]


def test_path_exits_only_once(tmp_path: Path):
    runner.invoke(init_app, [str(tmp_path)])
    config = load_config()
    assert config["databases"].count(str(tmp_path))
