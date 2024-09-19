import secrets
from pydantic import AnyHttpUrl, field_validator

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    API_STR: str = "/api"
    BACKEND_CORS_ORIGIN: list[AnyHttpUrl] | str = []

    @field_validator("BACKEND_CORS_ORIGIN", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: str | list[str]) -> list[str] | str:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, list | str):
            return v
        raise ValueError(v)

    DB_URL: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
