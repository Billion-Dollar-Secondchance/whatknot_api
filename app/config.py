import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# pick up .env based on APP_ENV
ENV = os.getenv("APP_ENV", "local")
load_dotenv(dotenv_path=f".env.{ENV}")

class Settings(BaseSettings):
    APP_ENV: str           # ← add this line
    DATABASE_URL: str
    SECRET_KEY: str
    DEBUG: bool = False
    ALGORITHM: str = "HS256" 
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str  

    class Config:
        env_file = f".env.{ENV}"
        extra = "forbid"   
settings = Settings()
