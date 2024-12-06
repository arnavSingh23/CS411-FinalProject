import pytest
from app import create_app, db
from app.models.user import User


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
