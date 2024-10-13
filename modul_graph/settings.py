from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    NEO4J_URI: str = "bolt://neo4j:password@localhost:7687"
    DEV: bool = False
