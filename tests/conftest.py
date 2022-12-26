import os

os.environ['JWT_SECRET_KEY'] = '09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7'

from typing import Any, Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.db.models.base import Base
from app.db.session import create_session
from app.main import app


@pytest.fixture(scope="session")
def db() -> Session:
    db_session = create_session()
    engine = db_session.bind
    Base.metadata.bind = engine
    Base.metadata.drop_all()
    Base.metadata.create_all()
    return db_session


@pytest.fixture()
def cleanup_db(db: Session) -> None:
    for table in reversed(Base.metadata.sorted_tables):
        db.execute(table.delete())


@pytest.fixture()
def app_client(cleanup_db: Any) -> Generator[TestClient, None, None]:
    yield TestClient(app)
