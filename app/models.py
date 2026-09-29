from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Airline(Base):
    """Database model representing an airline."""

    # Name of the table in the SQLite database.
    __tablename__ = "airlines"

    # Primary key that uniquely identifies each airline.
    id = Column(Integer, primary_key=True, index=True)

    # Name of the airline.
    # nullable=False means this field is required.
    name = Column(String, nullable=False)

    # Airline code.
    # Each airline must have a unique code.
    code = Column(String(10), unique=True, nullable=False)

    # Define the relationship between Airline and Flight.
    # One airline can have many flights.
    flights = relationship(
        "Flight",
        back_populates="airline"
    )


class Airport(Base):
    """Database model representing an airport."""

    # Name of the table in the SQLite database.
    __tablename__ = "airports"

    # Primary key that uniquely identifies each airport.
    id = Column(Integer, primary_key=True, index=True)

    # Full name of the airport.
    name = Column(String, nullable=False)

    # Three-character IATA airport code, such as JNB or LHR.
    # Each airport must have a unique IATA code.
    iata_code = Column(String(3), unique=True, nullable=False)

    # City where the airport is located.
    city = Column(String, nullable=False)

    # Country where the airport is located.
    country = Column(String, nullable=False)

    # Relationship for flights departing from this airport.
    # An airport can have many departing flights.
    departing_flights = relationship(
        "Flight",
        # Tell SQLAlchemy which Flight foreign key represents
        # the departure airport.
        foreign_keys="Flight.departure_airport_id",
        back_populates="departure_airport"
    )

    # Relationship for flights arriving at this airport.
    # An airport can have many arriving flights.
    arriving_flights = relationship(
        "Flight",
        # Tell SQLAlchemy which Flight foreign key represents
        # the arrival airport.
        foreign_keys="Flight.arrival_airport_id",
        back_populates="arrival_airport"
    )


class Flight(Base):
    """Database model representing a flight."""

    # Name of the table in the SQLite database.
    __tablename__ = "flights"

    # Primary key that uniquely identifies each flight.
    id = Column(Integer, primary_key=True, index=True)

    # Flight number, such as SA123 or BA456.
    # Each flight number must be unique.
    flight_number = Column(
        String(20),
        unique=True,
        nullable=False
    )

    # Current status of the flight, such as scheduled,
    # boarding, delayed, or cancelled.
    status = Column(
        String(30),
        nullable=False
    )

    # Foreign key connecting the flight to an airline.
    # The value must match an ID in the airlines table.
    airline_id = Column(
        Integer,
        ForeignKey("airlines.id"),
        nullable=False
    )

    # Foreign key connecting the flight to its departure airport.
    # The value must match an ID in the airports table.
    departure_airport_id = Column(
        Integer,
        ForeignKey("airports.id"),
        nullable=False
    )

    # Foreign key connecting the flight to its arrival airport.
    # The value must match an ID in the airports table.
    arrival_airport_id = Column(
        Integer,
        ForeignKey("airports.id"),
        nullable=False
    )

    # Relationship back to the airline that operates this flight.
    # This is the other side of Airline.flights.
    airline = relationship(
        "Airline",
        back_populates="flights"
    )

    # Relationship connecting this flight to its departure airport.
    departure_airport = relationship(
        "Airport",
        # Specify that departure_airport_id is the foreign key
        # used for this relationship.
        foreign_keys=[departure_airport_id],
        back_populates="departing_flights"
    )

    # Relationship connecting this flight to its arrival airport.
    arrival_airport = relationship(
        "Airport",
        # Specify that arrival_airport_id is the foreign key
        # used for this relationship.
        foreign_keys=[arrival_airport_id],
        back_populates="arriving_flights"
    )