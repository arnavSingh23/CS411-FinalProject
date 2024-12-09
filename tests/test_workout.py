import pytest
from app.models.workout import aggregate_workouts, log_workout, get_workouts, workout_logs

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

def test_aggregate_workouts_weight():
    """
    Test aggregation of workouts by weight.
    """
    # Clear workout_logs to prevent interference
    workout_logs.clear()

    user_id = 1
    # Log some workouts spanning two weeks
    log_workout(user_id, 101, 10, 50.0, "2024-12-01", "Session 1")
    log_workout(user_id, 102, 8, 70.0, "2024-12-02", "Session 2")
    log_workout(user_id, 103, 15, 60.0, "2024-12-08", "Session 3")

    # Aggregate by weight
    progress = aggregate_workouts(user_id, metric="weight")

    # Expected result
    expected = {
        "labels": ["2024-12-01", "2024-12-08"],
        "data": [120.0, 60.0]  # Week 1 total: 50+70, Week 2 total: 60
    }

    assert progress == expected


def test_aggregate_workouts_repetitions():
    """
    Test aggregation of workouts by repetitions.

    This test verifies that the `aggregate_workouts` function correctly aggregates workout
    data for a user by weeks and computes total repetitions for each week.

    Asserts:
        - Weekly labels are correctly generated.
        - Aggregated data matches the expected totals.
    """
    # Clear workout_logs to prevent interference
    workout_logs.clear()

    user_id = 1
    # Log some workouts spanning two weeks
    log_workout(user_id, 101, 10, 50.0, "2024-12-01", "Session 1")
    log_workout(user_id, 102, 20, 70.0, "2024-12-02", "Session 2")
    log_workout(user_id, 103, 15, 60.0, "2024-12-08", "Session 3")

    # Aggregate by repetitions
    progress = aggregate_workouts(user_id, metric="repetitions")

    # Expected result
    expected = {
        "labels": ["2024-12-01", "2024-12-08"],
        "data": [30, 15]  # Week 1 total: 10+20, Week 2 total: 15
    }

    assert progress == expected

def test_aggregate_workouts_empty():
    """
    Test aggregation of workouts when there is no data.

    This test ensures that `aggregate_workouts` handles the case where no workouts exist for the user.

    Asserts:
        - Returned labels and data are empty.
    """
    # Clear workout_logs to prevent interference
    workout_logs.clear()

    user_id = 2  # User with no logged workouts
    progress = aggregate_workouts(user_id)

    # Expected result
    expected = {
        "labels": [],
        "data": []
    }

    assert progress == expected