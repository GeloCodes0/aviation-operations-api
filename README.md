# Aviation Operations API

A REST API built with Python and FastAPI for managing aviation operations, including airlines, airports, and flights.

The project uses SQLAlchemy for database interaction, SQLite for data storage, Pydantic for request/response validation, and Pytest for automated testing.

## Features

* Create, retrieve, update, and delete airlines
* Create, retrieve, update, and delete airports
* Create, retrieve, update, and delete flights
* SQLite database integration using SQLAlchemy
* Pydantic request and response validation
* Foreign-key relationships between flights, airlines, and airports
* Validation for duplicate airline codes
* Validation for duplicate airport IATA codes
* Validation for duplicate flight numbers
* Validation for non-existent airlines and airports
* Validation preventing the same airport from being used for departure and arrival
* Automated API testing with Pytest
* Interactive API documentation through Swagger UI
* Health-check endpoint

## Technologies

* Python
* FastAPI
* Uvicorn
* SQLAlchemy
* SQLite
* Pydantic
* Pytest
* HTTPX

## Project Structure

```text
aviation-operations-api/
│
├── app/
│   ├── routers/
│   │   ├── airlines.py
│   │   ├── airports.py
│   │   └── flights.py
│   │
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   └── schemas.py
│
├── tests/
│   ├── conftest.py
│   ├── test_airlines.py
│   ├── test_airports.py
│   └── test_flights.py
│
├── .gitignore
├── README.md
└── requirements.txt
```

## Database Design

The API uses three main database tables:

### Airlines

Stores airline information.

* `id`
* `name`
* `code`

Each airline can have multiple flights.

### Airports

Stores airport information.

* `id`
* `name`
* `iata_code`
* `city`
* `country`

An airport can be associated with multiple departing and arriving flights.

### Flights

Stores flight information.

* `id`
* `flight_number`
* `status`
* `airline_id`
* `departure_airport_id`
* `arrival_airport_id`

Flights use foreign keys to connect them to their airline and departure/arrival airports.

## API Endpoints

### Airlines

| Method | Endpoint                 | Description               |
| ------ | ------------------------ | ------------------------- |
| POST   | `/airlines/`             | Create an airline         |
| GET    | `/airlines/`             | Retrieve all airlines     |
| GET    | `/airlines/{airline_id}` | Retrieve an airline by ID |
| PUT    | `/airlines/{airline_id}` | Update an airline         |
| DELETE | `/airlines/{airline_id}` | Delete an airline         |

### Airports

| Method | Endpoint                 | Description               |
| ------ | ------------------------ | ------------------------- |
| POST   | `/airports/`             | Create an airport         |
| GET    | `/airports/`             | Retrieve all airports     |
| GET    | `/airports/{airport_id}` | Retrieve an airport by ID |
| PUT    | `/airports/{airport_id}` | Update an airport         |
| DELETE | `/airports/{airport_id}` | Delete an airport         |

### Flights

| Method | Endpoint               | Description             |
| ------ | ---------------------- | ----------------------- |
| POST   | `/flights/`            | Create a flight         |
| GET    | `/flights/`            | Retrieve all flights    |
| GET    | `/flights/{flight_id}` | Retrieve a flight by ID |
| PUT    | `/flights/{flight_id}` | Update a flight         |
| DELETE | `/flights/{flight_id}` | Delete a flight         |

### System Endpoints

| Method | Endpoint  | Description      |
| ------ | --------- | ---------------- |
| GET    | `/`       | API information  |
| GET    | `/health` | API health check |

## Validation

The API performs validation before modifying the database.

Examples include:

* Airline codes must be unique.
* Airport IATA codes must be unique.
* Flight numbers must be unique.
* Flights must reference an existing airline.
* Flights must reference existing departure and arrival airports.
* Departure and arrival airports must be different.
* Requests for non-existent resources return a `404` response.
* Invalid duplicate resources return a `400` response.

## Running the API

### 1. Clone the repository

```bash
git clone https://github.com/GeloCodes0/aviation-operations-api.git
cd aviation-operations-api
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Start the API

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

## API Documentation

FastAPI automatically provides interactive documentation.

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

Alternative ReDoc documentation:

```text
http://127.0.0.1:8000/redoc
```

The Swagger interface can be used to send requests directly to the API and test the available endpoints.

## Running Tests

The project includes automated tests using Pytest.

Run all tests with:

```bash
pytest
```

The tests use a separate in-memory SQLite database so that testing does not modify the application's main database.

The test suite covers:

* Airline CRUD operations
* Airport CRUD operations
* Flight CRUD operations
* Duplicate resource validation
* Invalid airline references
* Invalid airport references
* Invalid flight configurations

Current test suite:

```text
22 tests
```

## Example Flight Request

Example request for creating a flight:

```json
{
    "flight_number": "BA201",
    "status": "Scheduled",
    "airline_id": 1,
    "departure_airport_id": 1,
    "arrival_airport_id": 2
}
```

Example response:

```json
{
    "id": 1,
    "flight_number": "BA201",
    "status": "Scheduled",
    "airline_id": 1,
    "departure_airport_id": 1,
    "arrival_airport_id": 2
}
```

## Purpose

This project was developed as a portfolio project to demonstrate practical experience with:

* REST API development
* Python
* FastAPI
* SQL databases
* SQLAlchemy ORM
* API validation
* Database relationships
* Automated testing
* Software project structure
* Git and GitHub
