def create_test_data(client):
    # Create an airline that can be associated with the test flights.
    airline_response = client.post(
        "/airlines/",
        json={
            "name": "British Airways",
            "code": "BA"
        }
    )

    # Create the departure airport.
    airport1_response = client.post(
        "/airports/",
        json={
            "name": "O.R. Tambo International Airport",
            "iata_code": "JNB",
            "city": "Johannesburg",
            "country": "South Africa"
        }
    )

    # Create the arrival airport.
    airport2_response = client.post(
        "/airports/",
        json={
            "name": "Cape Town International Airport",
            "iata_code": "CPT",
            "city": "Cape Town",
            "country": "South Africa"
        }
    )

    # Return the database IDs of the airline,
    # departure airport, and arrival airport.
    # These IDs are required when creating a flight.
    return (
        airline_response.json()["id"],
        airport1_response.json()["id"],
        airport2_response.json()["id"]
    )


def test_create_flight(client):
    # Create the airline and airports required by the flight.
    airline_id, departure_id, arrival_id = create_test_data(client)

    # Send a POST request to create a new flight.
    response = client.post(
        "/flights/",
        json={
            "flight_number": "BA201",
            "status": "Scheduled",
            "airline_id": airline_id,
            "departure_airport_id": departure_id,
            "arrival_airport_id": arrival_id
        }
    )

    # The flight should be created successfully.
    assert response.status_code == 200

    # Convert the JSON response into a Python dictionary.
    data = response.json()

    # Verify that all submitted flight information
    # was returned correctly.
    assert data["flight_number"] == "BA201"
    assert data["status"] == "Scheduled"
    assert data["airline_id"] == airline_id
    assert data["departure_airport_id"] == departure_id
    assert data["arrival_airport_id"] == arrival_id

    # The database should automatically generate an ID.
    assert "id" in data


def test_get_flights(client):
    # Create the airline and airports required by the flight.
    airline_id, departure_id, arrival_id = create_test_data(client)

    # Create a flight so there is data to retrieve.
    client.post(
        "/flights/",
        json={
            "flight_number": "BA201",
            "status": "Scheduled",
            "airline_id": airline_id,
            "departure_airport_id": departure_id,
            "arrival_airport_id": arrival_id
        }
    )

    # Request all flights from the API.
    response = client.get("/flights/")

    # The request should be successful.
    assert response.status_code == 200

    # Convert the JSON response into a Python list.
    data = response.json()

    # Verify that exactly one flight was returned.
    assert len(data) == 1

    # Verify that the correct flight was returned.
    assert data[0]["flight_number"] == "BA201"


def test_get_flight_by_id(client):
    # Create the airline and airports required by the flight.
    airline_id, departure_id, arrival_id = create_test_data(client)

    # Create a flight first.
    create_response = client.post(
        "/flights/",
        json={
            "flight_number": "BA201",
            "status": "Scheduled",
            "airline_id": airline_id,
            "departure_airport_id": departure_id,
            "arrival_airport_id": arrival_id
        }
    )

    # Get the automatically generated flight ID.
    flight_id = create_response.json()["id"]

    # Request the specific flight using its ID.
    response = client.get(
        f"/flights/{flight_id}"
    )

    # The request should be successful.
    assert response.status_code == 200

    # Verify that the correct flight was returned.
    assert response.json()["flight_number"] == "BA201"


def test_update_flight(client):
    # Create the airline and airports required by the flight.
    airline_id, departure_id, arrival_id = create_test_data(client)

    # Create the flight that will be updated.
    create_response = client.post(
        "/flights/",
        json={
            "flight_number": "BA201",
            "status": "Scheduled",
            "airline_id": airline_id,
            "departure_airport_id": departure_id,
            "arrival_airport_id": arrival_id
        }
    )

    # Store the ID of the created flight.
    flight_id = create_response.json()["id"]

    # Update the flight status from Scheduled to Delayed.
    response = client.put(
        f"/flights/{flight_id}",
        json={
            "flight_number": "BA201",
            "status": "Delayed",
            "airline_id": airline_id,
            "departure_airport_id": departure_id,
            "arrival_airport_id": arrival_id
        }
    )

    # The update should be successful.
    assert response.status_code == 200

    # Verify that the flight status was updated correctly.
    assert response.json()["status"] == "Delayed"


def test_delete_flight(client):
    # Create the airline and airports required by the flight.
    airline_id, departure_id, arrival_id = create_test_data(client)

    # Create the flight that will be deleted.
    create_response = client.post(
        "/flights/",
        json={
            "flight_number": "BA201",
            "status": "Scheduled",
            "airline_id": airline_id,
            "departure_airport_id": departure_id,
            "arrival_airport_id": arrival_id
        }
    )

    # Store the ID of the created flight.
    flight_id = create_response.json()["id"]

    # Send a DELETE request for the flight.
    response = client.delete(
        f"/flights/{flight_id}"
    )

    # The deletion should be successful.
    assert response.status_code == 200

    # Verify that the expected confirmation message was returned.
    assert response.json()["message"] == "Flight deleted successfully."


def test_flight_with_invalid_airline(client):
    # Create valid airports but intentionally ignore
    # the valid airline ID.
    _, departure_id, arrival_id = create_test_data(client)

    # Attempt to create a flight using an airline ID
    # that does not exist in the database.
    response = client.post(
        "/flights/",
        json={
            "flight_number": "BA201",
            "status": "Scheduled",
            "airline_id": 999,
            "departure_airport_id": departure_id,
            "arrival_airport_id": arrival_id
        }
    )

    # The API should return a 404 because the airline
    # could not be found.
    assert response.status_code == 404

    # Verify the expected error message.
    assert response.json()["detail"] == "Airline not found."


def test_flight_with_invalid_departure_airport(client):
    # Create a valid airline and arrival airport,
    # but intentionally ignore the valid departure airport.
    airline_id, _, arrival_id = create_test_data(client)

    # Attempt to create a flight using an airport ID
    # that does not exist as the departure airport.
    response = client.post(
        "/flights/",
        json={
            "flight_number": "BA201",
            "status": "Scheduled",
            "airline_id": airline_id,
            "departure_airport_id": 999,
            "arrival_airport_id": arrival_id
        }
    )

    # The API should return a 404 because the departure
    # airport could not be found.
    assert response.status_code == 404

    # Verify the expected error message.
    assert response.json()["detail"] == "Departure airport not found."


def test_flight_with_invalid_arrival_airport(client):
    # Create a valid airline and departure airport,
    # but intentionally ignore the valid arrival airport.
    airline_id, departure_id, _ = create_test_data(client)

    # Attempt to create a flight using an airport ID
    # that does not exist as the arrival airport.
    response = client.post(
        "/flights/",
        json={
            "flight_number": "BA201",
            "status": "Scheduled",
            "airline_id": airline_id,
            "departure_airport_id": departure_id,
            "arrival_airport_id": 999
        }
    )

    # The API should return a 404 because the arrival
    # airport could not be found.
    assert response.status_code == 404

    # Verify the expected error message.
    assert response.json()["detail"] == "Arrival airport not found."


def test_same_departure_and_arrival_airport(client):
    # Create the airline and get a valid departure airport.
    airline_id, departure_id, _ = create_test_data(client)

    # Attempt to create a flight where the departure
    # and arrival airports are the same.
    response = client.post(
        "/flights/",
        json={
            "flight_number": "BA201",
            "status": "Scheduled",
            "airline_id": airline_id,
            "departure_airport_id": departure_id,
            "arrival_airport_id": departure_id
        }
    )

    # The API should reject the request with a
    # 400 Bad Request response.
    assert response.status_code == 400

    # Verify the expected validation message.
    assert response.json()["detail"] == (
        "Departure and arrival airports must be different."
    )


def test_duplicate_flight_number(client):
    # Create the airline and airports required by the flights.
    airline_id, departure_id, arrival_id = create_test_data(client)

    # Create the first flight using flight number BA201.
    client.post(
        "/flights/",
        json={
            "flight_number": "BA201",
            "status": "Scheduled",
            "airline_id": airline_id,
            "departure_airport_id": departure_id,
            "arrival_airport_id": arrival_id
        }
    )

    # Attempt to create a second flight using the same
    # flight number.
    response = client.post(
        "/flights/",
        json={
            "flight_number": "BA201",
            "status": "Delayed",
            "airline_id": airline_id,
            "departure_airport_id": departure_id,
            "arrival_airport_id": arrival_id
        }
    )

    # The API should reject the duplicate flight number
    # with a 400 Bad Request response.
    assert response.status_code == 400

    # Verify the expected error message.
    assert response.json()["detail"] == "Flight number already exists."