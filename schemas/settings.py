import pathlib
from datetime import timedelta
from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict

# from pydantic import Field


BASE_DIR = pathlib.Path(__file__).resolve().parent.parent


# class DataBaseSettings(BaseSettings):
#     local_hostname: str
#     local_db_user: str
#     local_db_name: str
#     local_db_password: str

#     model_config = SettingsConfigDict(env_file=BASE_DIR / ".env", extra="allow")


class Settings(BaseSettings):
    access_token_secret_key: str
    refresh_token_secret_key: str

    access_token_expires_min: timedelta = timedelta(minutes=5)
    refresh_token_expires_min: timedelta = timedelta(minutes=60)
    hash_salt: str
    web_api_key: str
    web_client_id: str
    service_account_key_json: str
    frontend_url: List[str] = ["127.0.0.1:300", "localhost:9000"]
    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env", extra="allow")


# @lru_cache
# def db_settings():
#     return DataBaseSettings()


@lru_cache
def settings():
    return Settings()
