def test_create_airport(client):
    # Send a POST request to create a new airport.
    response = client.post(
        "/airports/",
        json={
            "name": "O.R. Tambo International Airport",
            "iata_code": "JNB",
            "city": "Johannesburg",
            "country": "South Africa"
        }
    )

    # The API should successfully create the airport.
    assert response.status_code == 200

    # Convert the JSON response into a Python dictionary.
    data = response.json()

    # Verify that the returned airport contains
    # the same information that was submitted.
    assert data["name"] == "O.R. Tambo International Airport"
    assert data["iata_code"] == "JNB"
    assert data["city"] == "Johannesburg"
    assert data["country"] == "South Africa"

    # The database should automatically generate an ID.
    assert "id" in data


def test_get_airports(client):
    # Create an airport first so there is data
    # available for the GET request.
    client.post(
        "/airports/",
        json={
            "name": "O.R. Tambo International Airport",
            "iata_code": "JNB",
            "city": "Johannesburg",
            "country": "South Africa"
        }
    )

    # Request all airports from the API.
    response = client.get("/airports/")

    # The request should be successful.
    assert response.status_code == 200

    # Convert the JSON response into a Python list.
    data = response.json()

    # Verify that exactly one airport was returned.
    assert len(data) == 1

    # Verify that the correct airport was returned.
    assert data[0]["iata_code"] == "JNB"


def test_duplicate_airport_code(client):
    # Create the first airport using the JNB IATA code.
    client.post(
        "/airports/",
        json={
            "name": "O.R. Tambo International Airport",
            "iata_code": "JNB",
            "city": "Johannesburg",
            "country": "South Africa"
        }
    )

    # Attempt to create another airport using
    # the same IATA code.
    response = client.post(
        "/airports/",
        json={
            "name": "Another Airport",
            "iata_code": "JNB",
            "city": "Johannesburg",
            "country": "South Africa"
        }
    )

    # The API should reject the duplicate code
    # with a 400 Bad Request response.
    assert response.status_code == 400

    # Verify that the expected error message is returned.
    assert response.json()["detail"] == "Airport IATA code already exists."


def test_get_airport_by_id(client):
    # Create an airport first.
    create_response = client.post(
        "/airports/",
        json={
            "name": "Cape Town International Airport",
            "iata_code": "CPT",
            "city": "Cape Town",
            "country": "South Africa"
        }
    )

    # Get the automatically generated ID from the response.
    airport_id = create_response.json()["id"]

    # Request that specific airport using its ID.
    response = client.get(
        f"/airports/{airport_id}"
    )

    # The request should be successful.
    assert response.status_code == 200

    # Verify that the correct airport was returned.
    assert response.json()["iata_code"] == "CPT"


def test_update_airport(client):
    # Create an airport that will be updated.
    create_response = client.post(
        "/airports/",
        json={
            "name": "O.R. Tambo International Airport",
            "iata_code": "JNB",
            "city": "Johannesburg",
            "country": "South Africa"
        }
    )

    # Store the ID of the airport that was created.
    airport_id = create_response.json()["id"]

    # Send a PUT request with the updated airport information.
    response = client.put(
        f"/airports/{airport_id}",
        json={
            "name": "Cape Town International Airport",
            "iata_code": "CPT",
            "city": "Cape Town",
            "country": "South Africa"
        }
    )

    # The update should be successful.
    assert response.status_code == 200

    # Verify that the airport name was updated correctly.
    assert response.json()["name"] == "Cape Town International Airport"

    # Verify that the IATA code was updated correctly.
    assert response.json()["iata_code"] == "CPT"


def test_delete_airport(client):
    # Create an airport that will be deleted.
    create_response = client.post(
        "/airports/",
        json={
            "name": "Cape Town International Airport",
            "iata_code": "CPT",
            "city": "Cape Town",
            "country": "South Africa"
        }
    )

    # Store the ID of the airport that was created.
    airport_id = create_response.json()["id"]

    # Send a DELETE request for that airport.
    response = client.delete(
        f"/airports/{airport_id}"
    )

    # The deletion should be successful.
    assert response.status_code == 200

    # Verify that the API returned the expected
    # deletion confirmation message.
    assert response.json()["message"] == "Airport deleted successfully."