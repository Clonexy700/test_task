from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    """Application settings, в том числе URL БД."""
    DATABASE_URL: str = Field(
        "sqlite:///./test.db",
        description="URL базы данных (например, SQLite или Postgres)"
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "allow"  # чтобы не падать на лишних переменных из .env

# Создаём экземпляр настроек
settings = Settings()
