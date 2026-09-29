def test_create_airline(client):
    # Send a POST request to create a new airline.
    response = client.post(
        "/airlines/",
        json={
            "name": "British Airways",
            "code": "BA"
        }
    )

    # The API should successfully create the airline.
    assert response.status_code == 200

    # Convert the JSON response into a Python dictionary.
    data = response.json()

    # Verify that the returned airline contains
    # the same information that was submitted.
    assert data["name"] == "British Airways"
    assert data["code"] == "BA"

    # The database should automatically generate an ID.
    assert "id" in data


def test_get_airlines(client):
    # First create an airline so there is data
    # available for the GET request.
    client.post(
        "/airlines/",
        json={
            "name": "British Airways",
            "code": "BA"
        }
    )

    # Request all airlines from the API.
    response = client.get("/airlines/")

    # The request should be successful.
    assert response.status_code == 200

    # Convert the JSON response into a Python list.
    data = response.json()

    # Verify that exactly one airline was returned.
    assert len(data) == 1

    # Verify that the correct airline was returned.
    assert data[0]["name"] == "British Airways"


def test_duplicate_airline_code(client):
    # Create the first airline using the BA code.
    client.post(
        "/airlines/",
        json={
            "name": "British Airways",
            "code": "BA"
        }
    )

    # Attempt to create another airline using
    # the same code.
    response = client.post(
        "/airlines/",
        json={
            "name": "Another Airline",
            "code": "BA"
        }
    )

    # The API should reject the duplicate code
    # with a 400 Bad Request response.
    assert response.status_code == 400

    # Verify that the expected error message is returned.
    assert response.json()["detail"] == "Airline code already exists."


def test_get_airline_by_id(client):
    # Create an airline first.
    create_response = client.post(
        "/airlines/",
        json={
            "name": "British Airways",
            "code": "BA"
        }
    )

    # Get the automatically generated ID from the response.
    airline_id = create_response.json()["id"]

    # Request that specific airline using its ID.
    response = client.get(
        f"/airlines/{airline_id}"
    )

    # The request should be successful.
    assert response.status_code == 200

    # Verify that the correct airline was returned.
    assert response.json()["name"] == "British Airways"


def test_update_airline(client):
    # Create an airline that will be updated.
    create_response = client.post(
        "/airlines/",
        json={
            "name": "British Airways",
            "code": "BA"
        }
    )

    # Store the ID of the airline that was created.
    airline_id = create_response.json()["id"]

    # Send a PUT request with the updated airline information.
    response = client.put(
        f"/airlines/{airline_id}",
        json={
            "name": "British Airways International",
            "code": "BAI"
        }
    )

    # The update should be successful.
    assert response.status_code == 200

    # Verify that the airline name was updated correctly.
    assert response.json()["name"] == "British Airways International"

    # Verify that the airline code was updated correctly.
    assert response.json()["code"] == "BAI"


def test_delete_airline(client):
    # Create an airline that will be deleted.
    create_response = client.post(
        "/airlines/",
        json={
            "name": "British Airways",
            "code": "BA"
        }
    )

    # Store the ID of the airline that was created.
    airline_id = create_response.json()["id"]

    # Send a DELETE request for that airline.
    response = client.delete(
        f"/airlines/{airline_id}"
    )

    # The deletion should be successful.
    assert response.status_code == 200

    # Verify that the API returned the expected
    # deletion confirmation message.
    assert response.json()["message"] == "Airline deleted successfully."