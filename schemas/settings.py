import pathlib
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

# from pydantic import Field


BASE_DIR = pathlib.Path(__file__).resolve().parent.parent



class DataBaseSettings(BaseSettings):
    local_hostname: str
    local_db_user: str
    local_db_name: str
    local_db_password: str

    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env")


@lru_cache
def db_settings():
    return DataBaseSettings()


print(db_settings())
