from typer.testing import CliRunner

from {{cookiecutter.package_name}}.cli.cli import app

runner = CliRunner(mix_stderr=False)


def test_delete_existing_{{cookiecutter.model_name}}(create_basic_{{cookiecutter.model_name}}):
    result = runner.invoke(app, ["{{cookiecutter.model_name}}", "delete", str(create_basic_{{cookiecutter.model_name}}.id_)])

    assert result.exit_code == 0
    assert result.stderr == "{{cookiecutter.model_class_name}} has been deleted.\n"


def test_not_existing():
    result = runner.invoke(app, ["{{cookiecutter.model_name}}", "delete", "42"])

    assert result.exit_code == 1
    assert not result.stdout
    assert result.stderr == "{{cookiecutter.model_class_name}} with ID 42 not found.\n"
