from functools import lru_cache

from pydantic import BaseSettings, PostgresDsn


class Settings(BaseSettings):
    database_url: PostgresDsn


@lru_cache(maxsize=128, typed=False)
def get_settings() -> Settings:
    settings = Settings(database_url="postgresql://postgres:mypassword@localhost:2345/user_db")
    return settings
