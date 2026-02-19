from typer.testing import CliRunner
from app.cli.destroy import destroy_app
from app.cli.init import init_app
from app.utils.handle_config_file import load_config
from pathlib import Path

runner = CliRunner()


def test_destroy_one(tmp_path: Path):
    runner.invoke(init_app, [str(tmp_path)])
    config = load_config()
    assert str(tmp_path) in config["databases"]

    index = config["databases"].index(str(tmp_path)) + 1

    result = runner.invoke(destroy_app, input=str(index))
    if result.exception:
        raise result.exception
    assert result.exit_code == 0

    config = load_config()
    assert str(tmp_path) not in config["databases"]


def test_destroy_pre_selected():
    config = load_config()
    old_str = config["databases"][1]
    runner.invoke(destroy_app, input=str(2))
    config = load_config()
    new_str = config["databases"][1]
    assert old_str.lower() != new_str.lower()


def test_no_db_found():
    config = load_config()
    result = runner.invoke(destroy_app, input=str(len(config["databases"]) + 1))
    assert "No valid databases selected." in result.output


def test_no_selection():
    result = runner.invoke(destroy_app, input=" ")
    if result.exception:
        raise result.exception
    assert result.exit_code == 0
    assert "No selection made. Exiting." in result.output


def test_out_of_index():
    result = runner.invoke(destroy_app, input="1 2 5")
    assert result.exit_code == 0


def test_multiple_db():
    config = load_config()
    old_db_len = len(config["databases"])
    result = runner.invoke(destroy_app, input="1 3")
    config = load_config()
    new_db_len = len(config["databases"])
    assert result.exit_code == 0
    assert old_db_len != new_db_len


def test_destroy_all():
    runner.invoke(destroy_app, ["-a"])
    config = load_config()
    assert len(config["databases"]) == 0
