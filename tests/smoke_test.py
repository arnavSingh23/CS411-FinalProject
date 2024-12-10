import pytest
from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_health_check(client):
    """Test if the health check route works"""
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'OK'


def test_login(client):
    """Test login route with valid credentials"""
    data = {
        'username': 'valid_username',
        'password': 'valid_password'
    }
    response = client.post('/login', json=data)
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Login successful'


def test_create_account(client):
    """Test account creation with valid data"""
    data = {
        'username': 'new_username',
        'password': 'new_password'
    }
    response = client.post('/create-account', json=data)
    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == 'Account created successfully'


def test_update_password(client):
    """Test password update with valid credentials"""
    data = {
        'username': 'valid_username',
        'current_password': 'valid_password',
        'new_password': 'new_valid_password'
    }
    response = client.post('/update-password', json=data)
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Password updated successfully'


def test_get_exercises(client):
    """Test if the external exercise API route works"""
    response = client.get('/get-exercises')
    assert response.status_code == 200
    data = response.get_json()
    assert 'results' in data


def test_favorite_exercise(client):
    """Test saving a favorite exercise"""
    data = {
        'user_id': 1,
        'exercise_id': 1,
        'name': 'Push-up'
    }
    response = client.post('/favorites', json=data)
    assert response.status_code == 201
    data = response.get_json()
    assert data['status'] == 'success'


def test_view_workouts(client):
    """Test viewing workouts route"""
    response = client.get('/view-workouts?user_id=1')
    assert response.status_code == 200
    data = response.get_json()
    assert 'workouts' in data


def test_list_favorite_exercises(client):
    """Test listing favorite exercises for a user"""
    response = client.get('/favorites?user_id=1')
    assert response.status_code == 200
    data = response.get_json()
    assert 'favorites' in data
