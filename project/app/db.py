from sqlmodel import create_engine, Session
from app.models import *
from .config import get_settings, Settings
from fastapi import Depends


def get_engine(settings: Settings = Depends(get_settings)):
    return create_engine(settings.database_url, echo=True)


def get_session(engine=Depends(get_engine)):
    with Session(engine) as session:
        yield session


def create_db_tables() -> None:
    engine = create_engine(get_settings().database_url)
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    create_db_tables()
