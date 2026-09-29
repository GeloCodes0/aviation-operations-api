from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Airline
from app.schemas import AirlineCreate, AirlineResponse


# Create a router specifically for airline-related endpoints.
# All routes in this file will start with /airlines.
router = APIRouter(
    prefix="/airlines",
    tags=["Airlines"]
)


@router.post("/", response_model=AirlineResponse)
def create_airline(
    airline: AirlineCreate,
    db: Session = Depends(get_db)
):
    # Check whether an airline with the same code already exists.
    # Airline codes must be unique in the database.
    existing_airline = (
        db.query(Airline)
        .filter(Airline.code == airline.code)
        .first()
    )

    # Return a 400 error if the airline code is already being used.
    if existing_airline:
        raise HTTPException(
            status_code=400,
            detail="Airline code already exists."
        )

    # Create a new SQLAlchemy Airline object using the
    # validated data received from the API request.
    new_airline = Airline(
        name=airline.name,
        code=airline.code
    )

    # Add the new airline to the current database session.
    db.add(new_airline)

    # Commit the transaction so the airline is permanently
    # saved to the database.
    db.commit()

    # Refresh the object so generated values such as the
    # database ID are available.
    db.refresh(new_airline)

    # Return the newly created airline.
    return new_airline


@router.get("/", response_model=list[AirlineResponse])
def get_airlines(
    db: Session = Depends(get_db)
):
    # Retrieve all airline records from the database.
    return db.query(Airline).all()


@router.get("/{airline_id}", response_model=AirlineResponse)
def get_airline(
    airline_id: int,
    db: Session = Depends(get_db)
):
    # Search for an airline using the ID provided in the URL.
    airline = (
        db.query(Airline)
        .filter(Airline.id == airline_id)
        .first()
    )

    # Return a 404 error if no airline with that ID exists.
    if not airline:
        raise HTTPException(
            status_code=404,
            detail="Airline not found."
        )

    # Return the airline record.
    return airline


@router.put("/{airline_id}", response_model=AirlineResponse)
def update_airline(
    airline_id: int,
    airline_data: AirlineCreate,
    db: Session = Depends(get_db)
):
    # Find the airline that needs to be updated.
    airline = (
        db.query(Airline)
        .filter(Airline.id == airline_id)
        .first()
    )

    # Return a 404 error if the airline does not exist.
    if not airline:
        raise HTTPException(
            status_code=404,
            detail="Airline not found."
        )

    # Update the existing airline with the new request data.
    airline.name = airline_data.name
    airline.code = airline_data.code

    # Save the changes to the database.
    db.commit()

    # Refresh the object so the response contains the
    # latest database values.
    db.refresh(airline)

    # Return the updated airline.
    return airline


@router.delete("/{airline_id}")
def delete_airline(
    airline_id: int,
    db: Session = Depends(get_db)
):
    # Find the airline that needs to be deleted.
    airline = (
        db.query(Airline)
        .filter(Airline.id == airline_id)
        .first()
    )

    # Return a 404 error if the airline does not exist.
    if not airline:
        raise HTTPException(
            status_code=404,
            detail="Airline not found."
        )

    # Mark the airline for deletion from the database.
    db.delete(airline)

    # Commit the transaction to permanently delete the record.
    db.commit()

    # Return a confirmation message to the client.
    return {
        "message": "Airline deleted successfully."
    }