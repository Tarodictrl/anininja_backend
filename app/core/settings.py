from typing_extensions import Annotated, Doc

from pydantic import Field
from pydantic_settings import BaseSettings
import toml


class Settings(BaseSettings):
    app_title: Annotated[str, Doc("The current project outer name")]
    app_description: Annotated[str, Doc("The current project description")]
    postgres_url: Annotated[str, Doc("Postgres url for connection.")]
    cloudflare_turnstile_key: Annotated[str, Doc("Cloudflare turnstile key.")]
    password_secret_key: Annotated[str, Doc("Password secret key.")]
    http_timeout: Annotated[int, Doc("HTTP timeout.")] = Field(default=60 * 10)
    client_id: Annotated[str, Doc("VK client id.")]
    secret_key: Annotated[str, Doc("VK secret key.")]
    redirect_auth_uri: Annotated[str, Doc("VK redirect auth uri.")]
    redirect_connect_uri: Annotated[str, Doc("VK redirect connect uri.")]
    host: Annotated[str, Doc("Host for redirect.")]
    telegram_token: Annotated[str, Doc("Telegram token.")]
    telegram_bot_id: Annotated[str, Doc("Telegram bot id.")]
    avatar_path: Annotated[str, Doc("Path to save avatar.")]

    @property
    def api_version(self) -> Annotated[str, Doc("The current project version")]:
        with open("pyproject.toml", "r") as file:
            pyproject_contents = file.read()
        return toml.loads(pyproject_contents)["tool"]["poetry"]["version"]


settings = Settings()
