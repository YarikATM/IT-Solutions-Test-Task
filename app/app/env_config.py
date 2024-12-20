from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class Settings(BaseSettings):

    SECRET_KEY: SecretStr
    DEBUG: bool
    DB_PORT: str
    DB_NAME: str
    DB_HOST: SecretStr
    DB_USER: SecretStr
    DB_PASSWORD: SecretStr

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


config = Settings()
