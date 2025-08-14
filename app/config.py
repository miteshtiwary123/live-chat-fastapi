import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://postgres:monu1234@localhost:5432/live_chat"

    class Config:
        env_file = ".env"

settings = Settings()
