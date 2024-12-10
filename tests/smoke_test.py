import requests

BASE_URL = "http://localhost:5000"

def test_health_check():
    """Check if the health endpoint is working."""
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    assert response.json() == {"status": "OK"}


def test_create_account():
    """Test creating a new user account."""
    response = requests.post(f"{BASE_URL}/create-account", json={
        "username": "smoketestuser",
        "password": "testpassword123"
    })
    assert response.status_code == 201
    assert response.json()["message"] == "Account created successfully"


def test_login():
    """Test logging in with a valid account."""
    response = requests.post(f"{BASE_URL}/login", json={
        "username": "smoketestuser",
        "password": "testpassword123"
    })
    assert response.status_code == 200
    assert response.json()["message"] == "Login successful"


def test_update_password():
    """Test updating the password for the test user."""
    response = requests.post(f"{BASE_URL}/update-password", json={
        "username": "smoketestuser",
        "current_password": "testpassword123",
        "new_password": "newtestpassword123"
    })
    assert response.status_code == 200
    assert response.json()["message"] == "Password updated successfully"


def test_log_workout():
    """Test logging a workout."""
    response = requests.post(f"{BASE_URL}/log-workout", json={
        "user_id": 1,
        "exercise_id": 101,
        "repetitions": 12,
        "weight": 25.0,
        "date": "2024-12-10",
        "comment": "Smoketest session"
    })
    assert response.status_code == 201
    assert response.json()["status"] == "success"


def test_view_workouts():
    """Test viewing workouts for a user."""
    response = requests.get(f"{BASE_URL}/view-workouts", params={"user_id": 1})
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert len(response.json()["workouts"]) > 0  # Ensure at least one workout is logged


def test_recommendations():
    """Test fetching exercise recommendations."""
    response = requests.get(f"{BASE_URL}/recommendations?category=4&equipment=7")
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert len(response.json()["exercises"]) > 0  # Ensure exercises are returned


if __name__ == "__main__":
    print("Starting Smoke Test...")
    test_health_check()
    print("Health Check Passed!")
    test_create_account()
    print("Create Account Passed!")
    test_login()
    print("Login Passed!")
    test_update_password()
    print("Update Password Passed!")
    test_log_workout()
    print("Log Workout Passed!")
    test_view_workouts()
    print("View Workouts Passed!")
    test_recommendations()
    print("Recommendations Passed!")
    print("All Smoke Tests Passed!")
