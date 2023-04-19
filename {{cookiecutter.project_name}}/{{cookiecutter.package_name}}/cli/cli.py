#! /usr/bin/env python3

import typer
from rich.console import Console

from {{cookiecutter.package_name}} import __version__
from {{cookiecutter.package_name}}.cli import {{cookiecutter.model_name}}_cli

app = typer.Typer(rich_markup_mode="markdown")
app.add_typer({{cookiecutter.model_name}}_cli.app, name="{{cookiecutter.model_name}}", help="{{cookiecutter.model_class_name}} CRUD")


@app.callback(invoke_without_command=True)
def callback(
    ctx: typer.Context,
    version: bool = typer.Option(False, help="Print the current version."),
) -> None:
    """{{cookiecutter.project_title}}"""
    if version:
        Console().print(__version__)
        return
    if ctx.invoked_subcommand is None:
        Console().print(ctx.get_help())
