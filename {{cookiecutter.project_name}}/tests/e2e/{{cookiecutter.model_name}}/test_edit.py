from typer.testing import CliRunner

from {{cookiecutter.package_name}}.cli.cli import app
from {{cookiecutter.package_name}}.crud import {{cookiecutter.model_name}}_crud

runner = CliRunner(mix_stderr=False)


def test_non_interactive_update_{{cookiecutter.unique_field}}(create_basic_{{cookiecutter.model_name}}):
    {{cookiecutter.model_name}}_id = create_basic_{{cookiecutter.model_name}}.id_

    result = runner.invoke(
        app,
        [
            "{{cookiecutter.model_name}}",
            "edit",
            str({{cookiecutter.model_name}}_id),
            "--no-input",
            "--{{cookiecutter.unique_field.replace('_','-')}}",
            "updated {{cookiecutter.unique_field}}",
        ],
    )

    assert result.exit_code == 0

    updated_{{cookiecutter.model_name}} = {{cookiecutter.model_name}}_crud().read({{cookiecutter.model_name}}_id)
    assert updated_{{cookiecutter.model_name}}.{{cookiecutter.unique_field}} == "updated {{cookiecutter.unique_field}}"


def test_non_interactive_no_options(create_basic_{{cookiecutter.model_name}}):
    result = runner.invoke(
        app, ["{{cookiecutter.model_name}}", "edit", str(create_basic_{{cookiecutter.model_name}}.id_), "--no-input"]
    )

    assert result.exit_code == 1
    assert result.stderr == "Nothing to update.\n"


def test_not_existing():
    result = runner.invoke(app, ["{{cookiecutter.model_name}}", "edit", "42"])

    assert result.exit_code == 1
    assert not result.stdout
    assert result.stderr == "{{cookiecutter.model_class_name}} with ID 42 not found.\n"
