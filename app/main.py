from fastapi import FastAPI

from app.database import Base, engine
from app import models
from app.routers import airlines
from app.routers import airports
from app.routers import flights


# Create all database tables defined in models.py.
# SQLAlchemy uses the imported models to determine which
# tables and columns need to exist in the database.
Base.metadata.create_all(bind=engine)


# Create the main FastAPI application.
app = FastAPI(
    title="Aviation Operations API",
    description=(
        "REST API for managing aviation operations, "
        "flights, airlines, and airports."
    ),
    version="1.0.0",
)


# Register the airline router with the main application.
# This makes all airline endpoints available under /airlines.
app.include_router(airlines.router)

# Register the airport router with the main application.
# This makes all airport endpoints available under /airports.
app.include_router(airports.router)

# Register the flight router with the main application.
# This makes all flight endpoints available under /flights.
app.include_router(flights.router)


@app.get("/")
def root():
    """Return basic information about the API."""

    # Basic endpoint used to confirm that the API is online
    # and responding to requests.
    return {
        "message": "Aviation Operations API",
        "version": "1.0.0",
        "status": "online",
    }


@app.get("/health")
def health_check():
    """Check whether the API is running."""

    # Simple health-check endpoint that can be used to verify
    # that the FastAPI application is responding correctly.
    return {
        "status": "healthy"
    }