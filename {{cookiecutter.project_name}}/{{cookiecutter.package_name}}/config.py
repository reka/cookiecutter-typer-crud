from pathlib import Path

from pydantic import BaseSettings, Field
from sqlite_utils import Database

class Settings(BaseSettings):
    db_path: Path = Field(
        Path.home() / "{{cookiecutter.project_name}}.db", env="{{cookiecutter.db_env_var}}"
    )

    def db(self) -> Database:
        return Database(self.db_path)


settings: Settings = Settings()
