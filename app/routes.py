from flask import Blueprint, request, jsonify
from app.models.user import User
from app import db

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login():
    """
        Logs in a user by verifying their credentials.

        This route receives a POST request with a username and password,
        checks if the user exists in the database, and verifies the provided
        password. If the credentials are correct, a success message is returned.
        If the credentials are invalid, an error message is returned.

        Args:
            None (expects JSON body containing 'username' and 'password' keys).

        Returns:
            Response: A JSON response with a message indicating success or failure.

        Raises:
            KeyError: If the input JSON does not contain 'username' or 'password'.
    """
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        # REMEMBER ARNAV Add JWT token generation here later
        return jsonify({"message": "Login successful"}), 200
    return jsonify({"message": "Invalid username or password"}), 401


@auth_bp.route('/create-account', methods=['POST'])
def create_account():
    """
        Creates a new user account.

        This route receives a POST request with a username and password,
        checks if the username is already taken, and if not, creates a new
        user in the database with the provided credentials.

        Args:
            None (expects JSON body containing 'username' and 'password' keys).

        Returns:
            Response: A JSON response indicating success or failure in account creation.

        Raises:
            KeyError: If the input JSON does not contain 'username' or 'password'.
            sqlalchemy.exc.IntegrityError: If the username already exists in the database.
    """
    data = request.get_json()
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"message": "Username already exists"}), 400

    user = User()
    user.username = data['username']
    user.set_password(data['password'])

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "Account created successfully"}), 201


@auth_bp.route('/update-password', methods=['POST'])
def update_password():
    """
        Updates the user's password.

        This route allows a user to update their password by providing their
        current password and the new password. The current password is
        validated first. If it matches, the new password is set.

        Args:
            None (expects JSON body containing 'username', 'current_password', and 'new_password' keys).

        Returns:
            Response: A JSON response indicating success or failure in updating the password.

        Raises:
            KeyError: If the input JSON does not contain 'username', 'current_password', or 'new_password'.
            sqlalchemy.exc.NoResultFound: If the user with the provided username does not exist.
            ValueError: If the current password does not match the stored password.
    """
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()

    if not user or not user.check_password(data['current_password']):
        return jsonify({"message": "Invalid username or current password"}), 401

    user.set_password(data['new_password'])
    db.session.commit()

    return jsonify({"message": "Password updated successfully"}), 200


@auth_bp.route('/health', methods=['GET'])
def health_check():
    """
    Health check route to verify the app is running.

    Returns:
        Response: A simple 'OK' message to indicate the application is running.
    """
    return jsonify({"status": "OK"}), 200
