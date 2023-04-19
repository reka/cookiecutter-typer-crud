import typer
from rich.console import Console


def exit_with_error(error_msg: str, code: int = 1) -> typer.Exit:
    stderr_console = Console(stderr=True, style="bold red")
    stderr_console.print(error_msg)
    return typer.Exit(code=code)


def get_from_options(ctx, field_names):
    # None: The option wasn't provided.
    # empty str: The option was provided with an empty string.
    return {
        key: value
        for (key, value) in ctx.params.items()
        if key in field_names and value is not None
    }
