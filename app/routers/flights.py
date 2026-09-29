from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Flight, Airline, Airport
from app.schemas import FlightCreate, FlightResponse


# Create a router specifically for flight-related endpoints.
# All routes in this file will start with /flights.
router = APIRouter(
    prefix="/flights",
    tags=["Flights"]
)


@router.post("/", response_model=FlightResponse)
def create_flight(
    flight: FlightCreate,
    db: Session = Depends(get_db)
):
    # Check that the airline associated with the flight exists.
    # This prevents a flight from referencing a nonexistent airline.
    airline = (
        db.query(Airline)
        .filter(Airline.id == flight.airline_id)
        .first()
    )

    if not airline:
        raise HTTPException(
            status_code=404,
            detail="Airline not found."
        )

    # Check that the departure airport exists.
    departure_airport = (
        db.query(Airport)
        .filter(Airport.id == flight.departure_airport_id)
        .first()
    )

    if not departure_airport:
        raise HTTPException(
            status_code=404,
            detail="Departure airport not found."
        )

    # Check that the arrival airport exists.
    arrival_airport = (
        db.query(Airport)
        .filter(Airport.id == flight.arrival_airport_id)
        .first()
    )

    if not arrival_airport:
        raise HTTPException(
            status_code=404,
            detail="Arrival airport not found."
        )

    # Prevent a flight from having the same airport
    # as both its departure and arrival location.
    if flight.departure_airport_id == flight.arrival_airport_id:
        raise HTTPException(
            status_code=400,
            detail="Departure and arrival airports must be different."
        )

    # Check whether another flight already uses the same
    # flight number, since flight numbers must be unique.
    existing_flight = (
        db.query(Flight)
        .filter(Flight.flight_number == flight.flight_number)
        .first()
    )

    if existing_flight:
        raise HTTPException(
            status_code=400,
            detail="Flight number already exists."
        )

    # Create a new SQLAlchemy Flight object using the
    # validated data received from the API request.
    new_flight = Flight(
        flight_number=flight.flight_number,
        status=flight.status,
        airline_id=flight.airline_id,
        departure_airport_id=flight.departure_airport_id,
        arrival_airport_id=flight.arrival_airport_id
    )

    # Add the flight to the current database session.
    db.add(new_flight)

    # Commit the transaction so the flight is saved
    # permanently to the database.
    db.commit()

    # Refresh the object so generated values such as the
    # database ID are available.
    db.refresh(new_flight)

    # Return the newly created flight.
    return new_flight


@router.get("/", response_model=list[FlightResponse])
def get_flights(
    db: Session = Depends(get_db)
):
    # Retrieve all flight records from the database.
    return db.query(Flight).all()


@router.get("/{flight_id}", response_model=FlightResponse)
def get_flight(
    flight_id: int,
    db: Session = Depends(get_db)
):
    # Search for a flight using the ID provided in the URL.
    flight = (
        db.query(Flight)
        .filter(Flight.id == flight_id)
        .first()
    )

    # Return a 404 error if no flight with that ID exists.
    if not flight:
        raise HTTPException(
            status_code=404,
            detail="Flight not found."
        )

    # Return the requested flight.
    return flight


@router.put("/{flight_id}", response_model=FlightResponse)
def update_flight(
    flight_id: int,
    flight_data: FlightCreate,
    db: Session = Depends(get_db)
):
    # Find the existing flight that needs to be updated.
    flight = (
        db.query(Flight)
        .filter(Flight.id == flight_id)
        .first()
    )

    # Return a 404 error if the flight does not exist.
    if not flight:
        raise HTTPException(
            status_code=404,
            detail="Flight not found."
        )

    # Check that the airline provided in the update exists.
    if not db.query(Airline).filter(
        Airline.id == flight_data.airline_id
    ).first():
        raise HTTPException(
            status_code=404,
            detail="Airline not found."
        )

    # Check that the departure airport provided in the update exists.
    if not db.query(Airport).filter(
        Airport.id == flight_data.departure_airport_id
    ).first():
        raise HTTPException(
            status_code=404,
            detail="Departure airport not found."
        )

    # Check that the arrival airport provided in the update exists.
    if not db.query(Airport).filter(
        Airport.id == flight_data.arrival_airport_id
    ).first():
        raise HTTPException(
            status_code=404,
            detail="Arrival airport not found."
        )

    # Prevent the same airport from being used
    # for both departure and arrival.
    if (
        flight_data.departure_airport_id
        == flight_data.arrival_airport_id
    ):
        raise HTTPException(
            status_code=400,
            detail="Departure and arrival airports must be different."
        )

    # Update the existing flight with the new request data.
    flight.flight_number = flight_data.flight_number
    flight.status = flight_data.status
    flight.airline_id = flight_data.airline_id
    flight.departure_airport_id = flight_data.departure_airport_id
    flight.arrival_airport_id = flight_data.arrival_airport_id

    # Save the changes to the database.
    db.commit()

    # Refresh the object so the response contains
    # the latest database values.
    db.refresh(flight)

    # Return the updated flight.
    return flight


@router.delete("/{flight_id}")
def delete_flight(
    flight_id: int,
    db: Session = Depends(get_db)
):
    # Find the flight that needs to be deleted.
    flight = (
        db.query(Flight)
        .filter(Flight.id == flight_id)
        .first()
    )

    # Return a 404 error if the flight does not exist.
    if not flight:
        raise HTTPException(
            status_code=404,
            detail="Flight not found."
        )

    # Mark the flight for deletion from the database.
    db.delete(flight)

    # Commit the transaction to permanently delete the record.
    db.commit()

    # Return a confirmation message to the client.
    return {
        "message": "Flight deleted successfully."
    }