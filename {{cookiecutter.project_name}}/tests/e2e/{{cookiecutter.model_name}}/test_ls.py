from typer.testing import CliRunner

from {{cookiecutter.package_name}}.cli.cli import app

runner = CliRunner(mix_stderr=False)


def test_empty_db():
    result = runner.invoke(app, ["{{cookiecutter.model_name}}", "ls"])

    assert result.exit_code == 0


def test_1_existing_{{cookiecutter.model_name}}(create_basic_{{cookiecutter.model_name}}):
    result = runner.invoke(app, ["{{cookiecutter.model_name}}", "ls"])

    assert result.exit_code == 0
    assert create_basic_{{cookiecutter.model_name}}.{{cookiecutter.unique_field}} in result.stdout


def test_1_existing_{{cookiecutter.model_name}}_plain(create_basic_{{cookiecutter.model_name}}):
    result = runner.invoke(app, ["{{cookiecutter.model_name}}", "ls", "--plain"])

    assert result.exit_code == 0
    assert len(result.stdout.splitlines()) == 1
    assert create_basic_{{cookiecutter.model_name}}.{{cookiecutter.unique_field}} in result.stdout

    # In the test,
    # the header and separator rows aren't printed.
    assert not result.stderr


def test_1_existing_{{cookiecutter.model_name}}_json(create_basic_{{cookiecutter.model_name}}):
    result = runner.invoke(app, ["{{cookiecutter.model_name}}", "ls", "--json"])

    assert result.exit_code == 0
    assert create_basic_{{cookiecutter.model_name}}.{{cookiecutter.unique_field}} in result.stdout
