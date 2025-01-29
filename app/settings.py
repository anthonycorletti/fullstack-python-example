import os
from enum import Enum, unique

from pydantic_settings import BaseSettings, SettingsConfigDict


@unique
class ResponseFormat(Enum):
    default = "*/*"
    html = "text/html"
    json = "application/json"


class Environment(str, Enum):
    test = "test"
    local = "local"
    preview = "preview"
    production = "production"


environment = Environment(os.getenv("APP_ENV", Environment.local.value))
environment_file = f".env.{environment.value}"


@unique
class LogLevel(Enum):
    NOTSET = 0
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50


class Settings(BaseSettings):
    ENV: Environment = Environment.local
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    API_SECRET_KEY: str = "secretkey"

    # sqlite
    SQLITE_SCHEME: str = "sqlite+aiosqlite"
    SQLITE_PATH: str = "db.sqlite3"

    model_config = SettingsConfigDict(
        env_prefix="app_",
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_file=environment_file,
        extra="allow",
    )

    @property
    def sqlite_dsn(self) -> str:
        return f"{self.SQLITE_SCHEME}:///{self.SQLITE_PATH}"

    def is_environment(self, environment: Environment) -> bool:
        return self.ENV == environment

    def is_test(self) -> bool:
        return self.is_environment(Environment.test)

    def is_local(self) -> bool:
        return self.is_environment(Environment.local)

    def is_preview(self) -> bool:
        return self.is_environment(Environment.preview)

    def is_production(self) -> bool:
        return self.is_environment(Environment.production)


settings = Settings()
