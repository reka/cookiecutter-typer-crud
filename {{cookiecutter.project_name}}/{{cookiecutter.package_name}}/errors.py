class {{cookiecutter.project_camel_case}}Error(Exception):
    """The base exception class."""


class {{cookiecutter.model_class_name}}ValidationError({{cookiecutter.project_camel_case}}Error):
    pass


class {{cookiecutter.model_class_name}}NotFound({{cookiecutter.project_camel_case}}Error):
    pass


class {{cookiecutter.model_class_name}}AlreadyExists({{cookiecutter.project_camel_case}}Error):
    pass
