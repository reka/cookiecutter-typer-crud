#! /usr/bin/env python3

import sys
from pydantic import ValidationError
import typer
from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt
from rich.table import Table


from {{cookiecutter.package_name}}.cli.utils import exit_with_error, get_from_options
from {{cookiecutter.package_name}}.cli.common_options import FormatOptions, INTERACTIVE_OPTION
from {{cookiecutter.package_name}}.crud import {{cookiecutter.model_name}}_crud
from {{cookiecutter.package_name}}.errors import {{cookiecutter.model_class_name}}NotFound
from {{cookiecutter.package_name}}.models import {{cookiecutter.model_class_name}}

app = typer.Typer(rich_markup_mode="markdown")

{{cookiecutter.unique_field}}_option: str = typer.Option(
    None,
    help="The {{cookiecutter.unique_field}} of the {{cookiecutter.model_name}}.",
)
{% for field_name, details in cookiecutter.further_fields|dictsort %}
{{field_name}}_option: {{details.type}} = typer.Option(
    None,
    help="The {{field_name}} of the {{cookiecutter.model_name}}.",
)
{% endfor %}

@app.command()
def create(
    ctx: typer.Context,
    {{cookiecutter.unique_field}}: str = {{cookiecutter.unique_field}}_option,
{% for field_name, details in cookiecutter.further_fields|dictsort %}
    {{field_name}}: {{details.type}} = {{field_name}}_option,
{% endfor %}
    interactive_flag: bool = INTERACTIVE_OPTION,
    plain: bool = FormatOptions.PLAIN,
    show_json: bool = FormatOptions.JSON,
):
    """Create a new {{cookiecutter.model_name}}"""
    interactive = sys.stdin.isatty() and interactive_flag

    stdout_console = Console()
    stderr_console = Console(stderr=True)

    provided_further_fields = _get_field_values(ctx, interactive, stderr_console)
    try:
        result = {{cookiecutter.model_name}}_crud().create(provided_further_fields)
    except ValidationError as e:
        if not interactive or not {{cookiecutter.model_class_name}}.all_simple_field_errors(e):
            raise exit_with_error(f"Can't create a {{cookiecutter.model_name}}. {e}") from e

        for error_data in e.errors():
            field_name = error_data["loc"][0]
            msg = error_data["msg"]
            stderr_console.print(f"Validation error. {field_name} {msg}")
            provided_further_fields[field_name] = Prompt.ask(field_name)
        try:
            result = {{cookiecutter.model_name}}_crud().create(provided_further_fields)
        except ValidationError as e_next:
            raise exit_with_error(f"{{cookiecutter.model_class_name}} still invalid. {e_next}") from e_next
    stderr_console.print("New {{cookiecutter.model_name}} created. 🪅")
    _print_{{cookiecutter.model_name}}(result, show_json, plain)

@app.command()
def ls(
    plain: bool = FormatOptions.PLAIN,
    show_json: bool = FormatOptions.JSON,
):
    """List all {{cookiecutter.model_name}}s"""
    result = {{cookiecutter.model_name}}_crud().read_items()

    stdout_console = Console()
    stderr_console = Console(stderr=True)

    if show_json:
        stdout_console.print_json(data=result)
        return

    if plain:
        # Define the maximum width of each column
        max_width = [5, 42]

        # Print a header & a separator row
        # if the output isn't redirected.
        if sys.stdout.isatty():
            # Print the header row
            header = ["ID", "{{cookiecutter.unique_field}}"]
            stderr_console.print(
                "|".join([f"{h:<{max_width[i]}}" for i, h in enumerate(header)])
            )
            # Print the separator row
            stderr_console.print(
                "|".join(["-" * max_width[i] for i in range(len(max_width))])
            )
        for item in result:
            id_str = f"{item['id']:<{max_width[0]}}"
            short_name_str = f"{item['{{cookiecutter.unique_field}}']:<{max_width[0]}}"
            stdout_console.print(f"{id_str}|{short_name_str}")
        return

    table = Table(show_header=True)
    table.add_column("ID")
    table.add_column("{{cookiecutter.unique_field}}")

    for item in result:
        table.add_row(str(item["id"]), item["{{cookiecutter.unique_field}}"])
    stdout_console.print(table)


@app.command()
def view(
    identifier: str = typer.Argument(
        None, help="This can be the ID or the {{cookiecutter.unique_field}} of the {{cookiecutter.model_name}}."
    ),
    plain: bool = FormatOptions.PLAIN,
    show_json: bool = FormatOptions.JSON,
):
    """Get a {{cookiecutter.model_name}} by ID or {{cookiecutter.unique_field}}."""
    try:
        {{cookiecutter.model_name}} = {{cookiecutter.model_name}}_crud().read(identifier)
    except {{cookiecutter.model_class_name}}NotFound as e:
        raise exit_with_error(str(e)) from e

    _print_{{cookiecutter.model_name}}({{cookiecutter.model_name}}, show_json, plain)


@app.command(name="delete")
def delete_{{cookiecutter.model_name}}({{cookiecutter.model_name}}_id: int):
    """Delete a {{cookiecutter.model_name}} by ID."""
    try:
        {{cookiecutter.model_name}}_crud().delete({{cookiecutter.model_name}}_id)
    except {{cookiecutter.model_class_name}}NotFound as e:
        raise exit_with_error(str(e)) from e

    console_stderr = Console(stderr=True)
    console_stderr.print("{{cookiecutter.model_class_name}} has been deleted.")


@app.command()
def edit(
    ctx: typer.Context,
    {{cookiecutter.model_name}}_id: int,
    {{cookiecutter.unique_field}}: str = {{cookiecutter.unique_field}}_option,
{% for field_name, details in cookiecutter.further_fields|dictsort %}
    {{field_name}}: {{details.type}} = {{field_name}}_option,
{% endfor %}
    plain: bool = FormatOptions.PLAIN,
    show_json: bool = FormatOptions.JSON,
    interactive_flag: bool = INTERACTIVE_OPTION,
):
    """Edit a {{cookiecutter.model_name}}."""
    interactive = sys.stdin.isatty() and interactive_flag

    try:
        current_{{cookiecutter.model_name}} = {{cookiecutter.model_name}}_crud().read({{cookiecutter.model_name}}_id).dict()
    except {{cookiecutter.model_class_name}}NotFound as e:
        raise exit_with_error(str(e)) from e

    {{cookiecutter.model_name}}_field_names = {{cookiecutter.model_class_name}}.non_id_further_fields()
    provided_further_fields = get_from_options(ctx, {{cookiecutter.model_name}}_field_names)

    # Ask for input values in interactive mode.
    if not provided_further_fields and interactive:
        for field_name in {{cookiecutter.model_name}}_field_names:
            updated_value = Prompt.ask(field_name, default=current_{{cookiecutter.model_name}}[field_name])
            if updated_value != current_{{cookiecutter.model_name}}[field_name]:
                provided_further_fields[field_name] = updated_value

    if not provided_further_fields:
        raise exit_with_error("Nothing to update.")

    {{cookiecutter.model_name}} = {{cookiecutter.model_name}}_crud().update({{cookiecutter.model_name}}_id, provided_further_fields)

    console_stderr = Console(stderr=True)
    console_stderr.print("{{cookiecutter.model_class_name}} has been updated.")

    _print_{{cookiecutter.model_name}}({{cookiecutter.model_name}}, show_json, plain)


def _print_{{cookiecutter.model_name}}({{cookiecutter.model_name}}: {{cookiecutter.model_class_name}}, show_json: bool, plain: bool):
    stdout_console = Console()

    if show_json:
        stdout_console.print_json({{cookiecutter.model_name}}.json())
    else:
        output = {{cookiecutter.model_name}}.get_plain() if plain else Markdown({{cookiecutter.model_name}}.get_markdown())
        stdout_console.print(output)


def _get_field_values(ctx, interactive, stderr_console):
    {{cookiecutter.model_name}}_field_names = {{cookiecutter.model_class_name}}.non_id_further_fields()
    if further_fields_from_options := get_from_options(ctx, {{cookiecutter.model_name}}_field_names):
        return further_fields_from_options

    if not interactive:
        raise exit_with_error("Can't create a {{cookiecutter.model_name}}. No further_fields provided.")

    stderr_console.print("Please enter the values for the further_fields of the {{cookiecutter.model_name}}.")
    entered_further_fields = {
        field_name: Prompt.ask(field_name) for field_name in {{cookiecutter.model_name}}_field_names
    }
    return entered_further_fields
