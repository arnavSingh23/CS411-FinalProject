import logging
import requests
import os

logger = logging.getLogger(__name__)
favorite_exercises = {}

# External API Configuration
WGER_API_URL = "https://wger.de/api/v2/exercise/"
WGER_API_HEADERS = {
    "Authorization": f"Token {os.getenv('WGER_API_KEY')}"
}


def fetch_exercises(category=None, equipment=None):
    """
    Fetches exercises from the Wger Workout Manager API.

    Args:
        category (str, optional): ID for filtering exercises by category.
        equipment (str, optional): ID for filtering exercises by equipment.

    Returns:
        list: A list of exercise dictionaries.
    """
    try:
        params = {"language": 2, "category": category, "equipment": equipment}
        response = requests.get(WGER_API_URL, headers=WGER_API_HEADERS, params=params)

        if response.status_code == 200:
            exercises = response.json().get("results", [])
            logger.info(f"Successfully fetched {len(exercises)} exercises.")
            return exercises
        else:
            logger.error(f"Wger API error: {response.status_code} - {response.text}")
            return []
    except Exception as e:
        logger.error(f"Error fetching exercises: {str(e)}")
        return []


def save_favorite_exercise(user_id, exercise_id, name, description=""):
    """
    Saves a favorite exercise for a user in the in-memory dictionary.

    Args:
        user_id (int): The ID of the user.
        exercise_id (int): The ID of the exercise from the API.
        name (str): The name of the exercise.
        description (str, optional): Description of the exercise.

    Returns:
        dict: A dictionary representing the saved exercise.
    """
    if user_id not in favorite_exercises:
        favorite_exercises[user_id] = []

    # Avoid duplicate entries for the same exercise
    for exercise in favorite_exercises[user_id]:
        if exercise["exercise_id"] == exercise_id:
            logger.warning(f"Exercise ID {exercise_id} is already in favorites for user {user_id}.")
            return {"message": "Exercise already exists in favorites"}

    exercise = {"exercise_id": exercise_id, "name": name, "description": description}
    favorite_exercises[user_id].append(exercise)
    logger.info(f"Saved favorite exercise for user {user_id}: {exercise}")
    return exercise


def get_favorite_exercises(user_id):
    """
    Retrieves all favorite exercises for a user.

    Args:
        user_id (int): The ID of the user.

    Returns:
        list: A list of favorite exercises.
    """
    return favorite_exercises.get(user_id, [])
