from functools import lru_cache

from pychu import load
from pychu.env import env
from pydantic import BaseModel


class Config(BaseModel):
    host: str
    port: int = 8000


@lru_cache
def get_config() -> Config:
    return load(Config, providers=[env(prefix="BROKEN_API_")])
