import os
from typing import Optional
from pydantic import ValidationError

from pydantic_settings import BaseSettings,  SettingsConfigDict


def get_db_uri(POSTGRES_USER:str, POSTGRES_PASSWORD:str, POSTGRES_HOST:str, POSTGRES_PORT:str, POSTGRES_DB:str):
    DB_URI:str = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    return DB_URI

class APISettings(BaseSettings):
    API_KEY: str = "secret"
    ALG: str = "HS512"
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', case_sensitive=True, extra='ignore')

class DBSettings(BaseSettings):
    POSTGRES_HOST: str = "172.17.0.1"
    POSTGRES_PORT: str = "5432"
    POSTGRES_USER: str = "dev"
    POSTGRES_PASSWORD: str = "dev"
    POSTGRES_DB: str = "dev"
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', case_sensitive=True,extra='ignore')

class Settings(BaseSettings, extra = 'ignore'):
    db: DBSettings = DBSettings()
    api: APISettings = APISettings()
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


try:
    settings = Settings()
    print(settings.model_dump())
except ValidationError as e:
    print(e)