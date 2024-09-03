from typing_extensions import Annotated, Doc

from pydantic import Field
from pydantic_settings import BaseSettings
import toml


class Settings(BaseSettings):
    app_title: Annotated[str, Doc("The current project outer name")]
    app_description: Annotated[str, Doc("The current project description")]
    postgres_url: Annotated[str, Doc("Postgres url for connection.")]
    http_timeout: Annotated[int, Doc("HTTP timeout.")] = Field(default=60 * 10)

    @property
    def api_version(self) -> Annotated[str, Doc("The current project version")]:
        with open("pyproject.toml", "r") as file:
            pyproject_contents = file.read()
        return toml.loads(pyproject_contents)["tool"]["poetry"]["version"]


settings = Settings()
