import pytest
from typer.testing import CliRunner

from {{cookiecutter.package_name}}.cli.cli import app

runner = CliRunner(mix_stderr=False)


@pytest.mark.parametrize(
    ("cmd_parts"),
    [
        (["{{cookiecutter.model_name}}", "create", "--{{cookiecutter.unique_field.replace('_','-')}}", "{{cookiecutter.unique_field_test_value}}"]),
    ],
)
def test_success(cmd_parts):
    result = runner.invoke(app, cmd_parts)

    assert result.exit_code == 0

    assert result.stdout

    # stderr
    assert "New {{cookiecutter.model_name}} created. 🪅" in result.stderr


def test_no_further_fields_no_input():
    result = runner.invoke(app, ["{{cookiecutter.model_name}}", "create", "--no-input"])

    assert result.exit_code == 1
    assert result.stderr == "Can't create a {{cookiecutter.model_name}}. No further_fields provided.\n"


def test_empty_{{cookiecutter.unique_field}}():
    result = runner.invoke(app, ["{{cookiecutter.model_name}}", "create", "--{{cookiecutter.unique_field.replace('_','-')}}", "", "--no-input"])

    assert result.exit_code == 1
    assert not result.stdout
    assert result.stderr.startswith("Can't create a {{cookiecutter.model_name}}.")
    assert "validation error" in result.stderr
