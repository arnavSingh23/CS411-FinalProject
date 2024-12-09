import logging
import requests
import os

logger = logging.getLogger(__name__)

# External API Configuration
WGER_API_URL = "https://wger.de/api/v2/exercise/"
WGER_API_HEADERS = {
    "Authorization": f"Token {os.getenv('WGER_API_KEY')}"  # API key stored in .env file
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
