from flask import Blueprint, request, jsonify
from app.models.user import User
from app import db
from datetime import datetime, timedelta
import jwt
import os
import logging

logger = logging.getLogger(__name__)

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
    try:
        data = request.get_json()
        logger.info(f"Login attempt for username: {data.get('username')}")

        user = User.query.filter_by(username=data['username']).first()
        if user and user.check_password(data['password']):
            token = jwt.encode({
                'user_id': user.id,
                'username': user.username,
                'exp': datetime.utcnow() + timedelta(hours=24)
            }, os.getenv('SECRET_KEY'), algorithm='HS256')
            logger.info(f"Successful login for user: {user.username}")
            return jsonify({"message": "Login successful"}), 200

        logger.warning(f"Failed login attempt for username: {data.get('username')}")
        return jsonify({"message": "Invalid username or password"}), 401
    except KeyError as e:
        logger.error(f"Login attempt failed due to missing field: {str(e)}")
        return jsonify({"message": "Missing required fields"}), 400
    except Exception as e:
        logger.error(f"Unexpected error during login: {str(e)}")
        return jsonify({"message": "An unexpected error occurred"}), 500


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
    try:
        data = request.get_json()
        logger.info(f"Account creation attempt for username: {data.get('username')}")

        if User.query.filter_by(username=data['username']).first():
            logger.warning(f"Account creation failed - username already exists: {data['username']}")
            return jsonify({"message": "Username already exists"}), 400

        user = User()
        user.username = data['username']
        user.set_password(data['password'])

        db.session.add(user)
        db.session.commit()

        logger.info(f"Account created successfully for username: {user.username}")
        return jsonify({"message": "Account created successfully"}), 201
    except KeyError as e:
        logger.error(f"Account creation failed due to missing field: {str(e)}")
        return jsonify({"message": "Missing required fields"}), 400
    except Exception as e:
        logger.error(f"Unexpected error during account creation: {str(e)}")
        db.session.rollback()
        return jsonify({"message": "An unexpected error occurred"}), 500


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
    try:
        data = request.get_json()
        logger.info(f"Password update attempt for username: {data.get('username')}")

        user = User.query.filter_by(username=data['username']).first()
        if not user or not user.check_password(data['current_password']):
            logger.warning(f"Password update failed - invalid credentials for username: {data.get('username')}")
            return jsonify({"message": "Invalid username or current password"}), 401

        user.set_password(data['new_password'])
        db.session.commit()

        logger.info(f"Password updated successfully for user: {user.username}")
        return jsonify({"message": "Password updated successfully"}), 200
    except KeyError as e:
        logger.error(f"Password update failed due to missing field: {str(e)}")
        return jsonify({"message": "Missing required fields"}), 400
    except Exception as e:
        logger.error(f"Unexpected error during password update: {str(e)}")
        db.session.rollback()
        return jsonify({"message": "An unexpected error occurred"}), 500


@auth_bp.route('/health', methods=['GET'])
def health_check():
    """
    Health check route to verify the app is running.

    Returns:
        Response: A simple 'OK' message to indicate the application is running.
    """
    logger.debug("Health check endpoint called")
    return jsonify({"status": "OK"}), 200
