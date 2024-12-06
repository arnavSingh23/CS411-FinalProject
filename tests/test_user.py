import pytest
from app.models.user import User
from werkzeug.security import check_password_hash


@pytest.fixture
def new_user():
    """Fixture to provide a new User instance."""
    return User(username="testuser")


def test_set_password(new_user):
    """Test that passwords are hashed and stored correctly."""
    new_user.set_password("securepassword")
    assert new_user.password_hash is not None, "Password hash should not be None"
    assert new_user.salt is not None, "Salt should not be None"
    assert check_password_hash(new_user.password_hash, "securepassword" + new_user.salt), \
        "Hashed password should match the plain-text password with salt"


def test_check_password_success(new_user):
    """Test successful password validation."""
    new_user.set_password("securepassword")
    assert new_user.check_password(
        "securepassword") is True, "Password validation should return True for correct password"


def test_check_password_failure(new_user):
    """Test failed password validation."""
    new_user.set_password("securepassword")
    assert new_user.check_password(
        "wrongpassword") is False, "Password validation should return False for incorrect password"


# Testing User Attributes

def test_user_creation():
    """Test creating a new User instance."""
    user = User(username="newuser")
    assert user.username == "newuser", "Username should be correctly set during creation"
    assert user.password_hash is None, "Password hash should be None initially"
    assert user.salt is None, "Salt should be None initially"


def test_user_logging_on_set_password(new_user, mocker):
    """Test that logging occurs when setting a password."""
    mock_logger = mocker.patch("app.models.user.logger.info")
    new_user.set_password("securepassword")
    mock_logger.assert_called_with(f"Password set successfully for user: {new_user.username}")


def test_user_logging_on_failed_set_password(new_user, mocker):
    """Test that logging occurs when setting a password fails."""
    mock_logger = mocker.patch("app.models.user.logger.error")
    mocker.patch("os.urandom", side_effect=Exception("Random generation error"))
    with pytest.raises(Exception, match="Random generation error"):
        new_user.set_password("securepassword")
    mock_logger.assert_called()
