import unittest
from app import create_app, db
from app.models.user import User

class SmokeTest(unittest.TestCase):
    """
    Smoke tests to ensure the basic functionality of the app is working.
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up the Flask test client and test database.
        """
        cls.app = create_app()
        cls.app.config['TESTING'] = True
        cls.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        db.create_all()  # create all the list
        cls.client = cls.app.test_client()

    @classmethod
    def tearDownClass(cls):
        """
        Tear down the test environment.
        """
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    def test_app_health_check(self):
        """
        Test if the health check route is accessible.
        """
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"status": "OK"})

    def test_database_connection(self):
        """
        Test if the database connection is working.
        """
        try:
            db.session.execute('SELECT 1')
        except Exception as e:
            self.fail(f"Database connection failed: {e}")

    def test_user_creation(self):
        """
        Test if a new user can be created.
        """
        user = User(username="testuser")
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()

        fetched_user = User.query.filter_by(username="testuser").first()
        self.assertIsNotNone(fetched_user)
        self.assertTrue(fetched_user.check_password("password123"))

    def test_user_login_route(self):
        """
        Test if the login route is working.
        """
        # create an user
        user = User(username="testlogin")
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()

        # test logging API
        response = self.client.post('/login', json={
            "username": "testlogin",
            "password": "password123"
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.json)
        self.assertEqual(response.json["message"], "Login successful")

    def test_workout_logging(self):
        """
        Test if a workout entry can be logged.
        """
        # create test user
        user = User(username="workoutuser")
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()

        # test record workout API
        response = self.client.post('/log-workout', json={
            "user_id": user.id,
            "exercise_id": 10,
            "repetitions": 15,
            "weight": 50.0,
            "date": "2024-12-07",
            "comment": "Great workout!"
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["status"], "success")

    def test_view_workouts(self):
        """
        Test if workout logs can be viewed.
        """
        # test create user and record 
        user = User(username="viewuser")
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()

        log = ExerciseLog(
            user_id=user.id,
            exercise_id=10,
            repetitions=15,
            weight=50.0,
            date="2024-12-07",
            comment="Test log"
        )
        db.session.add(log)
        db.session.commit()

        # view record API
        response = self.client.get('/view-workouts', query_string={"user_id": user.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status"], "success")
        self.assertGreater(len(response.json["workouts"]), 0)

if __name__ == '__main__':
    unittest.main()
