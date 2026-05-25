from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn
from typing import Optional

class Settings(BaseSettings):
    APP_NAME: str = "Sheber API"
    DEBUG: bool = True
    
    # Настройки базы данных (будут подтягиваться из файла .env)
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/sheber_db"
    
    # CORS настройки
    ALLOWED_ORIGINS: list[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()