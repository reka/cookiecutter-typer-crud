# Cookiecutter Typer CRUD

Generates an application with basic create, read, update, and delete functionality for a model.

Data storage: [sqlite](https://www.sqlite.org/index.html)

## Properties

Besides the usual cookiecutter properties, you also need to provide:

* the name of the model: preferably a single noun
* the name of a unique field of the model
* a realistic test value for this unique field

## Fields of the Model

* ID: `int` *added automatically*
* a unique, short (easy to type) name *configured via the `unique_field` property*
  
### Further Fields

You can use the optional `further_fields` property to add more fields to your model.

An example:

```json
{
    "language": {
        "type": "str",
        "test_value": "Python"
    },
    "number": {
        "type": "int",
        "test_value": 42
    }
}
```

Note:

`further_fields` is a [dictionary variable](https://cookiecutter.readthedocs.io/en/2.1.1/advanced/dict_variables.html)

To provide it, you might prefer using the [`--replay` option](https://cookiecutter.readthedocs.io/en/2.1.1/advanced/replay.html) instead of specifying it via the CLI prompt.

## Libraries Used

* [typer](https://typer.tiangolo.com/)
* [Pydantic](https://docs.pydantic.dev/)
* [sqlite-utils](https://sqlite-utils.datasette.io/en/stable/)
* [Rich](https://rich.readthedocs.io/en/latest/index.html)