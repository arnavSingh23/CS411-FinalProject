# Fitness and Activity Tracker 

## Overview

**Fitness and Activity Tracker** is a web application that helps users set and track their fitness goals. The app integrates with the **wger Workout Manager API** to provide exercise recommendations, log daily workouts, and visualize progress through charts.

This application is developed using **Flask** for the backend, **SQLite** for the database, and **SQLAlchemy** as the ORM. It includes account management features for secure user authentication and leverages Docker for containerization.

## Features

* **Account Management**
  * Securely store passwords using hashing with salts
  * Allow users to register, log in, and update their passwords

* **Workout Tracking**
  * Log daily workouts and activities
  * Set and track fitness goals
  * View progress using charts (❌)

* **Exercise Recommendations (❌)** 
  * Fetch exercise recommendations from the wger Workout Manager API
  * Save favorite exercises or routines

* **Health Check**
  * Verify the app's status through a health check route

## Technologies Used

* **Backend Framework**: Flask
* **Database**: SQLite
* **ORM**: SQLAlchemy
* **External API**: wger Workout Manager API
* **Containerization**: Docker

## How to Run

### Prerequisites

* Python 3.10+
* Docker (if containerizing the app)

### Setup Instructions

1. Clone the repository:
```bash
git clone <git@github.com:arnavSingh23/CS411-FinalProject.git>
cd fitness-tracker
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Set up your environment variables:
   * Create a `.env` file in the project root and add the following variables:
```env
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=<your-secret-key>
API_KEY=<wger-api-key>
```

4. Initialize the database:
```bash
flask db init
flask db migrate
flask db upgrade
```

5. Start the Flask application:
```bash
flask run
```

6. Open the app in your browser at `http://127.0.0.1:5000`

### Using Docker

1. Build the Docker image:
```bash
docker build -t fitness-tracker .
```

2. Run the Docker container:
```bash
docker run -p 5000:5000 --env-file .env fitness-tracker
```

## API Endpoints

### Authentication Routes

1. **Login**
   * **Route**: `/login`
   * **Method**: POST
   * **Purpose**: Authenticate users by verifying their password against stored hashes
   * **Request Format**:
```json
{
    "username": "string",
    "password": "string"
}
```
   * **Response Format**:
```json
{
    "message": "Login successful",
    "token": "jwt-token-string"
}
```

2. **Create Account**
   * **Route**: `/create-account`
   * **Method**: POST
   * **Purpose**: Allow users to register
   * **Request Format**:
```json
{
    "username": "string",
    "password": "string"
}
```
   * **Response Format**:
```json
{
    "message": "Account created successfully"
}
```

3. **Update Password**
   * **Route**: `/update-password`
   * **Method**: POST
   * **Purpose**: Allow users to update their password
   * **Request Format**:
```json
{
    "username": "string",
    "current_password": "string",
    "new_password": "string"
}
```
   * **Response Format**:
```json
{
    "message": "Password updated successfully"
}
```

### API Interaction Routes

1. **Log Workouts**
   * **Route**: `/log-workout`
   * **Method**: POST
   * **Purpose**: Log user workouts
   * **Request Format**:
   ```json
   {
       "user_id": "integer",
       "exercise_id": "integer",
       "repetitions": "integer",
       "weight": "float",
       "date": "YYYY-MM-DD",
       "comment": "string"
   }
   ```
   * **Response Format**:
   ```json
   {
   "message": "Workout logged successfully"
   }

2. **View Workouts**
   * **Route**: `/view-workouts`
   * **Method**: GET
   * **Purpose**: Retrieve all logged workouts for a user
   * **Request Format**:
   ```json
   {
       "user_id": "integer"
   }
   ```
   * **Response Format**:
   ```json
   
    {
        "exercise_id": "integer",
        "repetitions": "integer",
        "weight": "float",
        "date": "YYYY-MM-DD",
        "comment": "string"
    }
   


3. **View Progress ❌**
   * **Route**: `/progress`
   * **Method**: GET
   * **Purpose**: View fitness progress using charts
   * **Response Format**:
```json
{
    "labels": ["Week 1", "Week 2"],
    "data": [20, 30]
}
```

4. **Health Check**
   * **Route**: `/health`
   * **Method**: GET
   * **Purpose**: Verify the app is running
   * **Response Format**:
```json
{
    "status": "OK"
}
```
