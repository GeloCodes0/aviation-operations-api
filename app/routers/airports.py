from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Airport
from app.schemas import AirportCreate, AirportResponse


# Create a router specifically for airport-related endpoints.
# All routes in this file will start with /airports.
router = APIRouter(
    prefix="/airports",
    tags=["Airports"]
)


@router.post("/", response_model=AirportResponse)
def create_airport(
    airport: AirportCreate,
    db: Session = Depends(get_db)
):
    # Check whether an airport with the same IATA code already exists.
    # IATA codes must be unique in the database.
    existing_airport = (
        db.query(Airport)
        .filter(Airport.iata_code == airport.iata_code)
        .first()
    )

    # Return a 400 error if the IATA code is already being used.
    if existing_airport:
        raise HTTPException(
            status_code=400,
            detail="Airport IATA code already exists."
        )

    # Create a new SQLAlchemy Airport object using the
    # validated data received from the API request.
    new_airport = Airport(
        name=airport.name,
        iata_code=airport.iata_code,
        city=airport.city,
        country=airport.country
    )

    # Add the new airport to the current database session.
    db.add(new_airport)

    # Commit the transaction so the airport is saved
    # permanently to the database.
    db.commit()

    # Refresh the object so generated values such as the
    # database ID are available.
    db.refresh(new_airport)

    # Return the newly created airport.
    return new_airport


@router.get("/", response_model=list[AirportResponse])
def get_airports(
    db: Session = Depends(get_db)
):
    # Retrieve all airport records from the database.
    return db.query(Airport).all()


@router.get("/{airport_id}", response_model=AirportResponse)
def get_airport(
    airport_id: int,
    db: Session = Depends(get_db)
):
    # Search for an airport using the ID provided in the URL.
    airport = (
        db.query(Airport)
        .filter(Airport.id == airport_id)
        .first()
    )

    # Return a 404 error if no airport with that ID exists.
    if not airport:
        raise HTTPException(
            status_code=404,
            detail="Airport not found."
        )

    # Return the airport record.
    return airport


@router.put("/{airport_id}", response_model=AirportResponse)
def update_airport(
    airport_id: int,
    airport_data: AirportCreate,
    db: Session = Depends(get_db)
):
    # Find the airport that needs to be updated.
    airport = (
        db.query(Airport)
        .filter(Airport.id == airport_id)
        .first()
    )

    # Return a 404 error if the airport does not exist.
    if not airport:
        raise HTTPException(
            status_code=404,
            detail="Airport not found."
        )

    # Update the existing airport with the new request data.
    airport.name = airport_data.name
    airport.iata_code = airport_data.iata_code
    airport.city = airport_data.city
    airport.country = airport_data.country

    # Save the changes to the database.
    db.commit()

    # Refresh the object so the response contains the
    # latest database values.
    db.refresh(airport)

    # Return the updated airport.
    return airport


@router.delete("/{airport_id}")
def delete_airport(
    airport_id: int,
    db: Session = Depends(get_db)
):
    # Find the airport that needs to be deleted.
    airport = (
        db.query(Airport)
        .filter(Airport.id == airport_id)
        .first()
    )

    # Return a 404 error if the airport does not exist.
    if not airport:
        raise HTTPException(
            status_code=404,
            detail="Airport not found."
        )

    # Mark the airport for deletion from the database.
    db.delete(airport)

    # Commit the transaction to permanently delete the record.
    db.commit()

    # Return a confirmation message to the client.
    return {
        "message": "Airport deleted successfully."
    }