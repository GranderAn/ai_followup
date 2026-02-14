from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl
from functools import lru_cache

import os




class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Follow-Up System"
    API_V1_STR: str = "/api/v1"

    DATABASE_URL: str

    OPENAI_API_KEY: str
    EMAIL_FROM: str
    SENDGRID_API_KEY: str

    CALENDLY_WEBHOOK_SECRET: str | None = None

    FOLLOWUP_CHECK_INTERVAL_SECONDS: int = 300  # 5 minutes

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()