from pydantic import BaseModel, ConfigDict


# Base schema containing the fields shared by the
# airline creation and response schemas.
class AirlineBase(BaseModel):
    """Shared fields for an airline."""

    name: str
    code: str


# Schema used when receiving data to create a new airline.
# It inherits name and code from AirlineBase.
class AirlineCreate(AirlineBase):
    """Data required to create an airline."""

    pass


# Schema used when returning an airline through the API.
# It includes the database-generated ID.
class AirlineResponse(AirlineBase):
    """Data returned by the API for an airline."""

    id: int

    # Allows Pydantic to create the response from a SQLAlchemy
    # model object rather than requiring a normal dictionary.
    model_config = ConfigDict(
        from_attributes=True
    )


# Base schema containing the fields shared by the
# airport creation and response schemas.
class AirportBase(BaseModel):
    """Shared fields for an airport."""

    name: str
    iata_code: str
    city: str
    country: str


# Schema used when receiving data to create a new airport.
# It inherits all airport fields from AirportBase.
class AirportCreate(AirportBase):
    """Data required to create an airport."""

    pass


# Schema used when returning an airport through the API.
# It adds the database-generated ID.
class AirportResponse(AirportBase):
    """Data returned by the API for an airport."""

    id: int

    # Allows Pydantic to read values directly from
    # SQLAlchemy model attributes when creating the response.
    model_config = ConfigDict(
        from_attributes=True
    )


# Base schema containing the fields shared by the
# flight creation and response schemas.
class FlightBase(BaseModel):
    """Shared fields for a flight."""

    flight_number: str
    status: str
    airline_id: int
    departure_airport_id: int
    arrival_airport_id: int


# Schema used when receiving data to create a new flight.
# It inherits all flight fields from FlightBase.
class FlightCreate(FlightBase):
    """Data required to create a flight."""

    pass


# Schema used when returning a flight through the API.
# It adds the database-generated ID.
class FlightResponse(FlightBase):
    """Data returned by the API for a flight."""

    id: int

    # Allows Pydantic to create the response from
    # the SQLAlchemy Flight model.
    model_config = ConfigDict(
        from_attributes=True
    )