import pathlib
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
    web_api_key: str
    web_client_id: str
    service_account_key_json: str
    frontend_url: List[str] = ["127.0.0.1:300", "localhost:9000"]
    backend_host: str = "https://qr-code-file-downloader.onrender.com"
    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env", extra="allow")


# @lru_cache
# def db_settings():
#     return DataBaseSettings()


@lru_cache
def settings():
    return Settings()
