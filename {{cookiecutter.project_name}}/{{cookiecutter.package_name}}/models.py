from pydantic import BaseModel, Field, ValidationError


class Base{{cookiecutter.project_camel_case}}Model(BaseModel):
    @classmethod
    def non_id_further_fields(cls):
        all_further_fields = set(cls.schema()["properties"].keys())
        all_further_fields.remove("id")
        return all_further_fields

    @classmethod
    def all_simple_field_errors(cls, validation_error: ValidationError):
        return all(cls.is_simple_field_error(e) for e in validation_error.errors())

    @classmethod
    def is_simple_field_error(cls, e: dict) -> bool:
        return len(e["loc"]) == 1 and e["loc"][0] in cls.non_id_further_fields()


class {{cookiecutter.model_class_name}}(Base{{cookiecutter.project_camel_case}}Model):
    id_: int | None = Field(None, alias="id")
    {{cookiecutter.unique_field}}: str = Field(min_length=5, max_length=64)
    {% for field_name, details in cookiecutter.further_fields|dictsort %}
    {{field_name}}: {{details.type}} | None
    {% endfor %}

    def get_markdown(self) -> str:
        return f"""# {self.{{cookiecutter.unique_field}}}

* ID: {self.id_}
{% for field_name, _ in cookiecutter.further_fields|dictsort %}
* {{field_name}}: {self.{{field_name}}}
{% endfor %}
"""

    def get_plain(self) -> str:
        return f"""ID: {self.id_}
{{cookiecutter.unique_field}}: {self.{{cookiecutter.unique_field}}}
{% for field_name, _ in cookiecutter.further_fields|dictsort %}
{{field_name}}: {self.{{field_name}}}{% endfor %}
"""
