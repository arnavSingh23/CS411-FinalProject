from flask import Blueprint, request, jsonify
from app.models.user import User
from app.models.workout import ExerciseLog
from app import db
from datetime import datetime, timedelta
import jwt
import os
import logging
import requests

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

@auth_bp.route('/get-exercises', methods=['GET'])
def get_exercises():
    """
    Fetches a list of exercises from the wger Workout Manager API.

    This function sends a GET request to the external wger API to retrieve a list of exercises.
    The response is returned to the client in JSON format. If the request fails, an error 
    message is returned with a 500 status code.

    Returns:
        Response: A Flask JSON response containing either:
            - A list of exercises if the request is successful (status code 200).
            - An error message if the request fails (status code 500).

    Raises:
        None: This function handles exceptions internally and logs errors if necessary.
    """
    url = 'https://wger.de/api/v2/exercise/'
    response = requests.get(url, params={'language': 'en'})
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": "Failed to fetch exercises"}), 500
    
@auth_bp.route('/log-workout', methods=['POST'])
def log_workout():
    """
    Logs a workout entry for a user.
    Expects JSON payload with:
    - user_id (int): ID of the user.
    - exercise_id (int): ID of the exercise (from Wger API).
    - repetitions (int): Number of repetitions performed.
    - weight (float, optional): Weight used in kilograms.
    - date (str): Date of the workout in YYYY-MM-DD format.
    - comment (str, optional): Additional comments.

    Returns:
        JSON response indicating success or failure.
    """
    data = request.get_json()
    try:
        new_entry = ExerciseLog(
            user_id=data['user_id'],
            exercise_id=data['exercise_id'],
            repetitions=data['repetitions'],
            weight=data.get('weight'),
            date=datetime.strptime(data['date'], '%Y-%m-%d'),
            comment=data.get('comment', '')
        )
        db.session.add(new_entry)
        db.session.commit()
        return jsonify({"status": "success", "message": "Workout logged successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 400
    
@auth_bp.route('/view-workouts', methods=['GET'])
def view_workouts():
    """
    Retrieves workout entries for a user.
    Query parameters:
    - user_id (int): ID of the user.
    - start_date (str, optional): Filter workouts starting from this date.
    - end_date (str, optional): Filter workouts up to this date.

    Returns:
        JSON response with the list of workout logs or an error message.
    """
    user_id = request.args.get('user_id')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    try:
        query = ExerciseLog.query.filter_by(user_id=user_id)
        if start_date:
            query = query.filter(ExerciseLog.date >= datetime.strptime(start_date, '%Y-%m-%d'))
        if end_date:
            query = query.filter(ExerciseLog.date <= datetime.strptime(end_date, '%Y-%m-%d'))

        workouts = query.all()
        return jsonify({
            "status": "success",
            "workouts": [
                {
                    "id": workout.id,
                    "exercise_id": workout.exercise_id,
                    "repetitions": workout.repetitions,
                    "weight": workout.weight,
                    "date": workout.date.strftime('%Y-%m-%d'),
                    "comment": workout.comment
                }
                for workout in workouts
            ]
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400
