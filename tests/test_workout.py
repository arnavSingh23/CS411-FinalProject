import pytest
from app.models.workout import log_workout, get_workouts, workout_logs

def test_log_workout():
    """
    Test successful logging of a workout.

    This test verifies that a workout entry is correctly added to the in-memory dictionary
    when the `log_workout` function is called with valid input data.

    Asserts:
        - The workout is added to the dictionary.
        - The returned workout matches the input data.
    """
    user_id = 1
    workout = log_workout(
        user_id=user_id,
        exercise_id=101,
        repetitions=10,
        weight=50.0,
        date="2024-12-07",
        comment="Felt strong!"
    )

    assert workout["exercise_id"] == 101
    assert workout["repetitions"] == 10
    assert workout["weight"] == 50.0
    assert workout["date"] == "2024-12-07"
    assert workout["comment"] == "Felt strong!"

def test_get_workouts():
    """
    Test retrieval of workouts for a user.

    This test ensures that workouts are correctly retrieved from the in-memory dictionary,
    with optional filtering by date range.

    Asserts:
        - All workouts are returned when no filters are applied.
        - Filtering by start_date and end_date works correctly.
    """
    # Clear workout_logs to prevent interference
    workout_logs.clear()

    user_id = 1
    log_workout(user_id, 101, 10, 50.0, "2024-12-07", "Felt strong!")
    log_workout(user_id, 102, 8, 40.0, "2024-12-08", "Good session")

    # Retrieve all workouts
    workouts = get_workouts(user_id)
    assert len(workouts) == 2

    # Filter by date range
    filtered_workouts = get_workouts(user_id, start_date="2024-12-08")
    assert len(filtered_workouts) == 1
    assert filtered_workouts[0]["exercise_id"] == 102
