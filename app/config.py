from functools import lru_cache

from pydantic import BaseSettings, PostgresDsn


class Settings(BaseSettings):
    database_url: PostgresDsn


@lru_cache(maxsize=128, typed=False)
def get_settings() -> Settings:
    settings = Settings()
    return settings
