from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    AUTH_SECRET = "devssecret"

    ADMIN_USER = "admin"
    ADMIN_PASSWORD = "admin"
