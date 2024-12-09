import logging
from datetime import datetime, timedelta
from collections import defaultdict

logger = logging.getLogger(__name__)

# In-memory storage for workout logs
workout_logs = {}  # {user_id: [{"exercise_id": int, "repetitions": int, "weight": float, "date": str, "comment": str}]}


def log_workout(user_id, exercise_id, repetitions, weight, date, comment):
    """
    Logs a workout for a user in the in-memory dictionary.

    Args:
        user_id (int): ID of the user.
        exercise_id (int): ID of the exercise.
        repetitions (int): Number of repetitions.
        weight (float): Weight used in kilograms.
        date (str): Date of the workout in YYYY-MM-DD format.
        comment (str): Additional comments.

    Returns:
        dict: The logged workout entry.
    """
    if user_id not in workout_logs:
        workout_logs[user_id] = []

    workout = {
        "exercise_id": exercise_id,
        "repetitions": repetitions,
        "weight": weight,
        "date": date,
        "comment": comment,
    }
    workout_logs[user_id].append(workout)
    logger.info(f"Logged workout for user {user_id}: {workout}")
    return workout


def get_workouts(user_id, start_date=None, end_date=None):
    """
    Retrieves workout logs for a user, optionally filtered by date.

    Args:
        user_id (int): ID of the user.
        start_date (str, optional): Start date for filtering (YYYY-MM-DD).
        end_date (str, optional): End date for filtering (YYYY-MM-DD).

    Returns:
        list: A list of workout entries.
    """
    if user_id not in workout_logs:
        return []

    workouts = workout_logs[user_id]
    if start_date or end_date:
        start = datetime.strptime(start_date, "%Y-%m-%d") if start_date else None
        end = datetime.strptime(end_date, "%Y-%m-%d") if end_date else None

        filtered_workouts = [
            workout for workout in workouts
            if (not start or datetime.strptime(workout["date"], "%Y-%m-%d") >= start) and
               (not end or datetime.strptime(workout["date"], "%Y-%m-%d") <= end)
        ]
        return filtered_workouts

    return workouts

def aggregate_workouts(user_id, metric="weight"):
    if user_id not in workout_logs or not workout_logs[user_id]:
        return {"labels": [], "data": []}

    # Get user workouts
    workouts = workout_logs[user_id]

    # Sort workouts by date
    workouts.sort(key=lambda x: datetime.strptime(x["date"], "%Y-%m-%d"))

    weekly_totals = defaultdict(float)
    weekly_labels = []

    current_week_start = None
    for workout in workouts:
        workout_date = datetime.strptime(workout["date"], "%Y-%m-%d")

        # Align week start to Sunday
        week_start = workout_date - timedelta(days=(workout_date.isoweekday() % 7))

        # If this is the first workout or we have moved to a new week, update current_week_start
        if current_week_start is None or week_start != current_week_start:
            current_week_start = week_start
            weekly_labels.append(current_week_start.strftime("%Y-%m-%d"))

        weekly_totals[current_week_start] += workout[metric]

    labels = weekly_labels
    data = [weekly_totals[datetime.strptime(label, "%Y-%m-%d")] for label in labels]

    return {"labels": labels, "data": data}

