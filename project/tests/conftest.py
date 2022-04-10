import os
import pytest
from fastapi.testclient import TestClient
from sqlmodel import create_engine, Session
from sqlmodel.pool import StaticPool
from app.models import *
from app.main import create_app
from app.db import get_session
from app.config import Settings, get_settings


@pytest.fixture(name="session")
def session_fixture(settings) -> Session:
    if settings.database_url:
        engine = create_engine(settings.database_url)
    else:
        engine = create_engine("sqlite://",
                               connect_args={"check_same_thread": False},
                               poolclass=StaticPool)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(name="settings")
def settings_fixture():
    settings = Settings(testing=1, environment="test", database_url=os.getenv("DATABASE_TEST_URL"))
    return settings


@pytest.fixture(name="client")
def client_fixture(session, settings) -> TestClient:
    def get_session_override():
        return session

    def get_settings_override():
        return settings

    app = create_app()
    app.dependency_overrides[get_session] = get_session_override
    app.dependency_overrides[get_settings] = get_settings_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
