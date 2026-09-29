from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


# SQLite database file used by the API.
# The database will be created as aviation.db in the project folder.
DATABASE_URL = "sqlite:///./aviation.db"


# Create the SQLAlchemy database engine.
# The engine manages connections between the application and database.
engine = create_engine(
    DATABASE_URL,
    # SQLite normally restricts database connections to the thread
    # that created them. This allows the FastAPI application to use
    # the database connection across different threads.
    connect_args={"check_same_thread": False},
)


# Create a session factory.
# Each API request can create its own database session using this.
SessionLocal = sessionmaker(
    # The application explicitly controls when transactions are committed.
    autocommit=False,

    # Prevent SQLAlchemy from automatically flushing changes
    # before every query.
    autoflush=False,

    # Connect sessions to the database engine created above.
    bind=engine,
)


# Base class used by SQLAlchemy database models.
# Models such as Airline, Airport, and Flight inherit from this class.
class Base(DeclarativeBase):
    pass


def get_db():
    """Provide a database session for an API request."""

    # Create a new database session for the request.
    db = SessionLocal()

    try:
        # Yield the database session to the API endpoint.
        # FastAPI's dependency injection system uses this function
        # whenever an endpoint requires a database connection.
        yield db

    finally:
        # Always close the database session after the request finishes.
        # This prevents database connections from being left open.
        db.close()