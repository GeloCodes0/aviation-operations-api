import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db


# Use an in-memory SQLite database for testing.
# This database only exists while the tests are running,
# so the real aviation.db database is not affected.
TEST_DATABASE_URL = "sqlite:///:memory:"


# Create a separate SQLAlchemy engine for the test database.
engine = create_engine(
    TEST_DATABASE_URL,

    # Allow the SQLite database connection to be used
    # across different threads during testing.
    connect_args={"check_same_thread": False},

    # Keep the in-memory SQLite database available
    # throughout the test session.
    poolclass=StaticPool,
)


# Create a session factory specifically for the test database.
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


@pytest.fixture
def db_session():
    # Create all database tables required by the application
    # inside the temporary test database.
    Base.metadata.create_all(bind=engine)

    # Create a database session for the current test.
    db = TestingSessionLocal()

    try:
        # Provide the database session to the test.
        yield db

    finally:
        # Close the database session after the test finishes.
        db.close()

        # Remove all tables so the next test starts
        # with a clean database.
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db_session):
    # Replace the application's normal get_db dependency
    # with the temporary test database session.
    def override_get_db():
        yield db_session

    # Tell FastAPI to use the test database instead of
    # the real aviation.db database during these tests.
    app.dependency_overrides[get_db] = override_get_db

    # Create a FastAPI test client.
    # This allows the tests to make HTTP requests to the API
    # without starting a real web server.
    with TestClient(app) as test_client:
        yield test_client

    # Remove the dependency override after the test finishes
    # so it does not affect other tests or normal application use.
    app.dependency_overrides.clear()