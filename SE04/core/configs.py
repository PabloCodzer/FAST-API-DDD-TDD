from pydantic_settings import BaseSettings # type: ignore
from dotenv import load_dotenv # type: ignore
import os

load_dotenv()

USUARIO_PG   = os.getenv('USUARIO_PG')
PASSWORD_PG  = os.getenv('PASSWORD_PG')
BANCO        = os.getenv('BANCO')

class Settings(BaseSettings):
    API_V1_STR: str = '/api/v1'
    DB_URL: str = f"postgresql+asyncpg://{USUARIO_PG}:{PASSWORD_PG}@34.132.30.21:5432/{BANCO}"

    class Config:
        case_sensitive = True

settings: Settings = Settings()