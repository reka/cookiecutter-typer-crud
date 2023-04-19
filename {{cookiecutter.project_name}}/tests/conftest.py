from pathlib import Path
import pytest

from {{cookiecutter.package_name}} import config
from {{cookiecutter.package_name}}.crud import {{cookiecutter.model_name}}_crud


@pytest.fixture(autouse=True)
def app_db_path(tmpdir):
    config.settings.db_path = Path(tmpdir / "pycon_test.db")


@pytest.fixture()
def create_basic_{{cookiecutter.model_name}}():
    return {{cookiecutter.model_name}}_crud().create({"{{cookiecutter.unique_field}}": "{{cookiecutter.unique_field_test_value}}" })
