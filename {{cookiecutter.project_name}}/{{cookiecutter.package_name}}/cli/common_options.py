import typer


class FormatOptions:
    PLAIN: bool = typer.Option(False, "--plain", help="Output plain text")
    JSON: bool = typer.Option(False, "--json", help="Output JSON format")


INTERACTIVE_OPTION: bool = typer.Option(
    True,
    "--interactive/--no-interactive",
    "--input/--no-input",
    help="Switch whether interactive prompts are shown. Use `--no-input` when you call this command from scripts.",
)
