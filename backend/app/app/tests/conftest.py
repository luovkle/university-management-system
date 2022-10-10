import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session
from sqlmodel.pool import StaticPool

from app.api.deps import get_session
from app.main import app


@pytest.fixture(name="session")
def session_fixture():
    connect_args = {
        "check_same_thread": False,
    }
    engine = create_engine("sqlite://", connect_args=connect_args, poolclass=StaticPool)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    app.dependency_overrides[get_session] = lambda: session
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
