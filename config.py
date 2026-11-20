import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "MICRONAUT API")
    APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: str = os.getenv("DB_PORT", "3306")
    DB_USER: str = os.getenv("DB_USER", "root")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
    DB_NAME: str = os.getenv("DB_NAME", "micronaut_db")
    SQL_ECHO: bool = os.getenv("SQL_ECHO", "false").lower() == "true"
    API_PREFIX: str = "/api/v1"

settings = Settings()
