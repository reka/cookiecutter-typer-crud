from typer.testing import CliRunner

from {{cookiecutter.package_name}}.cli.cli import app

runner = CliRunner(mix_stderr=False)


def test_existing_by_id(create_basic_{{cookiecutter.model_name}}):
    result = runner.invoke(app, ["{{cookiecutter.model_name}}", "view", str(create_basic_{{cookiecutter.model_name}}.id_)])

    assert result.exit_code == 0
    assert result.stdout

def test_existing_by_{{cookiecutter.unique_field}}(create_basic_{{cookiecutter.model_name}}):
    result = runner.invoke(app, ["{{cookiecutter.model_name}}", "view", str(create_basic_{{cookiecutter.model_name}}.{{cookiecutter.unique_field}})])

    assert result.exit_code == 0
    assert result.stdout


def test_existing_plain(create_basic_{{cookiecutter.model_name}}):
    result = runner.invoke(app, ["{{cookiecutter.model_name}}", "view", str(create_basic_{{cookiecutter.model_name}}.id_), "--plain"])

    assert result.exit_code == 0
    assert result.stdout


def test_existing_json(create_basic_{{cookiecutter.model_name}}):
    result = runner.invoke(app, ["{{cookiecutter.model_name}}", "view", str(create_basic_{{cookiecutter.model_name}}.id_), "--json"])

    assert result.exit_code == 0
    assert result.stdout


def test_not_existing():
    result = runner.invoke(app, ["{{cookiecutter.model_name}}", "view", "42"])

    assert result.exit_code == 1
    assert not result.stdout
    assert result.stderr == "{{cookiecutter.model_class_name}} with ID 42 not found.\n"
