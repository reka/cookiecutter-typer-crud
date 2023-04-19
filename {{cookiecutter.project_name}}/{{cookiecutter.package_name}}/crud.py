from sqlite_utils.db import NotFoundError
from sqlite_utils import Database

from {{cookiecutter.package_name}}.errors import {{cookiecutter.model_class_name}}NotFound
from {{cookiecutter.package_name}}.models import {{cookiecutter.model_class_name}}
from {{cookiecutter.package_name}}.config import settings


def {{cookiecutter.model_name}}_crud():
    return Crud(settings.db(), "{{cookiecutter.model_name}}s", {{cookiecutter.model_class_name}})


class Crud:
    def __init__(self, db: Database, table_name: str, model) -> None:
        self.table = db.table(table_name)
        if not self.table.exists():
            self._init_table()
        self.model = model

    def read_items(self):
        return list(self.table.rows)

    def create(self, properties: dict):
        model = self.model(**properties)
        self.table.insert(model.dict(exclude={"id_"}))
        inserted_id = self.table.last_pk
        return self.read(inserted_id)

    def read(self, identifier: int | str):
        if isinstance(identifier, int) or identifier.isdigit():
            try:
                return self.model(**self.table.get(identifier))
            except NotFoundError as e:
                raise {{cookiecutter.model_class_name}}NotFound(f"{{cookiecutter.model_class_name}} with ID {identifier} not found.") from e
        query_result = list(self.table.rows_where("short_name = ?", [identifier]))
        if len(query_result) != 1:
            raise {{cookiecutter.model_class_name}}NotFound(f"{{cookiecutter.model_class_name}} with short_name {identifier} not found.")
        return self.model(**query_result[0])

    def update(self, item_id: int, properties: dict):
        try:
            self.table.update(item_id, properties)
            return self.read(item_id)
        except NotFoundError as e:
            raise {{cookiecutter.model_class_name}}NotFound(f"{{cookiecutter.model_class_name}} with ID {item_id} not found.") from e

    def delete(self, item_id: int):
        try:
            self.table.delete(item_id)
        except NotFoundError as e:
            raise {{cookiecutter.model_class_name}}NotFound(f"{{cookiecutter.model_class_name}} with ID {item_id} not found.") from e

    def _init_table(self):
        self.table.create(
            {
                "id": int,
                "{{cookiecutter.unique_field}}": str,
            {% for field_name, details in cookiecutter.further_fields|dictsort %}
                "{{field_name}}": {{details.type}},
            {% endfor %}
            },
            pk="id",
        )
        self.table.create_index(["{{cookiecutter.unique_field}}"], unique=True)
