from typer.testing import CliRunner

from {{cookiecutter.package_name}}.cli.cli import app

runner = CliRunner(mix_stderr=False)


def test_no_options():
    result = runner.invoke(app)

    assert result.exit_code == 0
    assert "help" in result.stdout
    assert not result.stderr


def test_version():
    result = runner.invoke(app, ["--version"])

    assert result.exit_code == 0
    assert result.stdout == "0.1.0\n"
    assert not result.stderr
