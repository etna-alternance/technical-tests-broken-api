from functools import lru_cache

from pychu import load
from pychu.env import env
from pydantic import BaseModel


class DatabaseConfig(BaseModel):
    host: str
    port: int = 3306
    name: str
    user: str
    password: str


class Config(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000
    database: DatabaseConfig


@lru_cache
def get_config() -> Config:
    return load(Config, providers=[env(prefix="BROKEN_API_")])
