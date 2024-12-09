import pytest
from app import create_app, db
from app.models.user import User
from app.models.workout import workout_logs
from unittest.mock import patch



@pytest.fixture
def test_client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()


def test_health_check(test_client):
    """Test the health check endpoint."""
    response = test_client.get('/health')
    assert response.status_code == 200
    assert response.get_json() == {"status": "OK"}


def test_create_account_success(test_client):
    """Test successful account creation."""
    response = test_client.post('/create-account', json={
        'username': 'testuser',
        'password': 'password123'
    })
    assert response.status_code == 201
    assert response.get_json() == {"message": "Account created successfully"}


def test_login_success(test_client):
    """Test successful login."""
    user = User(username='testuser')
    user.set_password('password123')
    db.session.add(user)
    db.session.commit()

    response = test_client.post('/login', json={
        'username': 'testuser',
        'password': 'password123'
    })
    assert response.status_code == 200
    assert "Login successful" in response.get_json()["message"]


def test_update_password_success(test_client):
    """Test successful password update."""
    user = User(username='testuser')
    user.set_password('password123')
    db.session.add(user)
    db.session.commit()

    response = test_client.post('/update-password', json={
        'username': 'testuser',
        'current_password': 'password123',
        'new_password': 'newpassword123'
    })
    assert response.status_code == 200
    assert response.get_json() == {"message": "Password updated successfully"}


def test_create_account_missing_fields(test_client):
    """Test attempt to create an account without providing a password"""
    response = test_client.post('/create-account', json={
        'username': 'validusername',
        'email': 'test@example.com'
    })
    assert response.status_code == 400
    assert response.json['message'] == 'Missing required fields'


def test_login_incorrect_password(test_client):
    """Test attempt to log in with an incorrect password"""
    test_client.post('/create-account', json={
        'username': 'testuser',
        'password': 'CorrectPass123',
        'email': 'testuser@example.com'
    })

    response = test_client.post('/login', json={
        'username': 'testuser',
        'password': 'WrongPass456'
    })
    assert response.status_code == 401
    assert response.json['message'] == 'Invalid username or password'

def test_log_workout(test_client):
    """
    Test the log workout route with in-memory dictionary.

    Ensures that a workout is correctly logged into the in-memory dictionary.
    """
    response = test_client.post('/log-workout', json={
        "user_id": 1,
        "exercise_id": 101,
        "repetitions": 10,
        "weight": 20.5,
        "date": "2024-12-07",
        "comment": "Good session"
    })
    assert response.status_code == 201
    assert response.json['status'] == "success"
    assert len(workout_logs[1]) == 1
    assert workout_logs[1][0]["exercise_id"] == 101


def test_view_workouts(test_client):
    """
    Test the view workouts route with in-memory dictionary.

    Ensures that workouts are correctly retrieved from the in-memory dictionary.
    """
    # Pre-log a workout
    workout_logs[1] = [
        {"exercise_id": 101, "repetitions": 10, "weight": 20.5, "date": "2024-12-07", "comment": "Good session"}
    ]

    response = test_client.get('/view-workouts', query_string={"user_id": 1})
    assert response.status_code == 200
    assert response.json['status'] == "success"
    assert len(response.json['workouts']) == 1
    assert response.json['workouts'][0]["exercise_id"] == 101

@patch("app.routes.fetch_exercises")
def test_get_recommendations_success(mock_fetch_exercises, test_client):
    """
    Test successful retrieval of exercise recommendations.

    This test mocks the `fetch_exercises` function to simulate a successful API response
    and verifies that the `/recommendations` route correctly handles the request.

    Mocks:
        - fetch_exercises: Returns a mocked list of exercises.

    Asserts:
        - The route returns a status code of 200.
        - The returned exercises match the mocked response.
    """
    # Mock data
    mock_fetch_exercises.return_value = [
        {"id": 1, "name": "Push-ups"},
        {"id": 2, "name": "Squats"}
    ]

    response = test_client.get('/recommendations?category=4&equipment=7')
    assert response.status_code == 200
    assert response.json['status'] == "success"
    assert len(response.json['exercises']) == 2
    assert response.json['exercises'][0]['name'] == "Push-ups"
    assert response.json['exercises'][1]['name'] == "Squats"


@patch("app.routes.fetch_exercises")
def test_get_recommendations_failure(mock_fetch_exercises, test_client):
    """
    Test failure in retrieving exercise recommendations.

    This test mocks the `fetch_exercises` function to simulate an exception
    and verifies that the `/recommendations` route correctly handles the error.

    Mocks:
        - fetch_exercises: Raises an exception.

    Asserts:
        - The route returns a status code of 500.
        - The returned message indicates an error occurred.
    """
    # Simulate an error
    mock_fetch_exercises.side_effect = Exception("API error")

    response = test_client.get('/recommendations?category=4&equipment=7')
    assert response.status_code == 500
    assert response.json['status'] == "error"
    assert "API error" in response.json['message']