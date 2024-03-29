from pathlib import Path

from pydantic import PostgresDsn, SecretStr
from pydantic_settings import BaseSettings
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

__all__ = [
    "config",
    "async_engine",
    "async_session_maker",
    "templating",
    "static",
]



class Config(BaseSettings):
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    DATABASE_URL: PostgresDsn
    SECRET_KEY: SecretStr


MANAGE_APP_MIGRATIONS = [
    "demo",
]

config = Config()
async_engine = create_async_engine(url=config.DATABASE_URL.unicode_string())
async_session_maker = async_sessionmaker(bind=async_engine)
templating = Jinja2Templates(directory=config.BASE_DIR / "templates")
static = StaticFiles(directory=config.BASE_DIR / "static", check_dir=False)



