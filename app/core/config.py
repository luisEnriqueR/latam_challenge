import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

os.get("DATABASE_URL")


class Settings(BaseSettings):
    APP_NAME: str = os.get("APP_NAME")
    DATABASE_URL: str = os.get("DATABASE_URL")

    class Config:
        env_file = ".env"


settings = Settings()
