from typing import Any, Dict, List

from pydantic import PostgresDsn,validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_PASSWORD_PLAIN: str
    DB_NAME: str
    DATABASE_URI: PostgresDsn | None = None
    
    @validator('DATABASE_URI', pre=True)
    def assemble_db_connection(
        cls, value: str | None, values: Dict[str, Any],  # noqa: N805, WPS110
    ) -> str:
        if isinstance(value, str):
            return value

        return PostgresDsn.build(
            scheme='postgresql+asyncpg',
            username=values.get('DB_USER'),
            password=values.get('DB_PASSWORD'),
            host=values.get('DB_HOST'),
            port=values.get('DB_PORT'),
            path='{0}'.format(values.get('DB_NAME')),
        )

    REDIS_HOST: str = 'localhost'
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str = ''
    REDIS_DB: int = 0
    REDIS_MAX_CONN_POOL: int = 10

    ENVIRONMENT: str

    class Config:
        env_file = ".env"
        extra = 'allow'


settings = Settings()