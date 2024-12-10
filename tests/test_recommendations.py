import pytest
from app.models.recommendations import fetch_exercises, save_favorite_exercise, get_favorite_exercises
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


def test_save_favorite_exercise():
    """
    Test saving a favorite exercise for a user.

    This test verifies that the `save_favorite_exercise` function correctly saves an exercise
    in the in-memory dictionary and prevents duplicates.
    """
    user_id = 1
    exercise_id = 101
    name = "Push-ups"
    description = "Chest exercise"

    # Save the exercise
    favorite = save_favorite_exercise(user_id, exercise_id, name, description)
    assert favorite["exercise_id"] == exercise_id
    assert favorite["name"] == name

    # Attempt to save the same exercise again
    duplicate = save_favorite_exercise(user_id, exercise_id, name, description)
    assert duplicate == {"message": "Exercise already exists in favorites"}


def test_get_favorite_exercises():
    """
    Test retrieving favorite exercises for a user.

    This test verifies that the `get_favorite_exercises` function returns the correct list
    of favorite exercises for a given user ID.
    """
    user_id = 1

    # Add favorite exercises
    save_favorite_exercise(user_id, 101, "Push-ups", "Chest exercise")
    save_favorite_exercise(user_id, 102, "Squats", "Leg exercise")

    # Retrieve favorite exercises
    favorites = get_favorite_exercises(user_id)
    assert len(favorites) == 2
    assert favorites[0]["name"] == "Push-ups"
    assert favorites[1]["name"] == "Squats"

    # Check for a user with no favorites
    empty_favorites = get_favorite_exercises(2)  # User ID 2 has no favorites
    assert empty_favorites == []
