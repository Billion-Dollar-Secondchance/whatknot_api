# app/core/config.py
import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

ENV = os.getenv("APP_ENV", "local")
load_dotenv(dotenv_path=f".env.{ENV}")

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DEBUG: bool = False

    # Add these three!
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str

    # Add APP_ENV to the settings
    APP_ENV: str

    class Config:
        env_file = f".env.{ENV}"
        extra = "forbid"

settings = Settings()
