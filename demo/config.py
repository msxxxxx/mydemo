from pydantic import RedisDsn
from pydantic_settings import BaseSettings

from passlib.context import CryptContext
from redis import Redis

from demo.session_storage import RedisSessionStorage


class Config(BaseSettings):
    SESSION_STORAGE_URL: RedisDsn
    JWT_SECRET_KEY: str = "76f19ce3b85e31383aaf59009e722a296a254d125e2622efd1727e0e9570d44d"
    JWT_EXP: int = 30


config = Config()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
session_storage = RedisSessionStorage(redis=Redis.from_url(url=config.SESSION_STORAGE_URL.unicode_string()))