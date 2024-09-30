import pytest
from fastapi.testclient import TestClient
from app import app as test_app
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker
from models.pdf import Document #noqa: F401
from models.users import User #noqa: F401

from database import get_db, Base

DATABASE_URL = "sqlite:///:memory:"


engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool
)

TestSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)

@pytest.fixture(scope='module', autouse=True)
def setup_database():
    # Initialize the test database schema
    Base.metadata.create_all(bind=engine)



def override_get_db():
    db = TestSession()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def client(setup_database):
    test_app.dependency_overrides[get_db] = override_get_db
    client = TestClient(test_app)
    return client


@pytest.fixture(scope="function")
def db_session():
    session = TestSession()
    Base.metadata.create_all(bind=engine)
    yield session