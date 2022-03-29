import os
import logging
from functools import lru_cache
from pydantic import BaseSettings

log = logging.getLogger("uvicorn")


class Settings(BaseSettings):
    environement: str = os.getenv("ENVIRONMENT", "dev")
    testing: bool = os.getenv("TESTING", 0)


@lru_cache(maxsize=1)
async def get_settings() -> BaseSettings:
    log.info("Loading settings from the environment...")
    return Settings()
