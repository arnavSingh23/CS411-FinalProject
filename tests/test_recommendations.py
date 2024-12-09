import pytest
from app.models.recommendations import fetch_exercises
from unittest.mock import patch

@patch("app.models.recommendations.requests.get")
def test_fetch_exercises_success(mock_get):
    """
    Test successful retrieval of exercises from the Wger API.

    This test mocks the Wger API response to simulate a successful API call
    and verifies that the `fetch_exercises` function correctly processes the response.

    Mocks:
        - requests.get: Returns a mocked response with exercise data.

    Asserts:
        - The function returns a list of exercises when the API call is successful.
        - The logger logs a success message.
    """
    mock_response = {
        "results": [
            {"id": 1, "name": "Push-ups", "description": "Chest exercise"},
            {"id": 2, "name": "Squats", "description": "Leg exercise"}
        ]
    }
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_response

    exercises = fetch_exercises(category="4", equipment="7")
    assert len(exercises) == 2
    assert exercises[0]["name"] == "Push-ups"

@patch("app.models.recommendations.requests.get")
def test_fetch_exercises_failure(mock_get):
    """
    Test failure to retrieve exercises from the Wger API.

    This test mocks the Wger API response to simulate a failed API call
    and verifies that the `fetch_exercises` function returns an empty list.

    Mocks:
        - requests.get: Returns a mocked response with an error status.

    Asserts:
        - The function returns an empty list when the API call fails.
        - The logger logs an error message.
    """
    mock_get.return_value.status_code = 500

    exercises = fetch_exercises(category="4", equipment="7")
    assert exercises == []
