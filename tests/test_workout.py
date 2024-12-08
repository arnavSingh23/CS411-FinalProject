import unittest
from app import create_app, db
from app.models.workout import ExerciseLog
from app.models.user import User
from datetime import datetime

class WorkoutModelTest(unittest.TestCase):
    """
    Unit tests for the ExerciseLog model.
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up the Flask test app and database.
        """
        cls.app = create_app()
        cls.app.config['TESTING'] = True
        cls.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # 使用内存数据库
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        db.create_all()

    @classmethod
    def tearDownClass(cls):
        """
        Tear down the test environment.
        """
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    def setUp(self):
        """
        Set up resources before each test.
        """
        self.user = User(username="testuser")
        self.user.set_password("password123")
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        """
        Clean up resources after each test.
        """
        db.session.query(ExerciseLog).delete()
        db.session.query(User).delete()
        db.session.commit()

    def test_create_exercise_log(self):
        """
        Test creating a new ExerciseLog entry.
        """
        log = ExerciseLog(
            user_id=self.user.id,
            exercise_id=10,
            repetitions=15,
            weight=50.0,
            date=datetime.strptime("2024-12-07", '%Y-%m-%d'),
            comment="Test workout"
        )
        db.session.add(log)
        db.session.commit()

        fetched_log = ExerciseLog.query.filter_by(user_id=self.user.id).first()
        self.assertIsNotNone(fetched_log)
        self.assertEqual(fetched_log.repetitions, 15)
        self.assertEqual(fetched_log.weight, 50.0)
        self.assertEqual(fetched_log.comment, "Test workout")

    def test_missing_required_fields(self):
        """
        Test creating an ExerciseLog entry with missing required fields.
        """
        log = ExerciseLog(
            user_id=self.user.id,
            exercise_id=10,
            repetitions=None,  
            weight=50.0,
            date=datetime.strptime("2024-12-07", '%Y-%m-%d'),
            comment="Invalid workout"
        )
        with self.assertRaises(Exception):
            db.session.add(log)
            db.session.commit()

    def test_delete_exercise_log(self):
        """
        Test deleting an ExerciseLog entry.
        """
        log = ExerciseLog(
            user_id=self.user.id,
            exercise_id=10,
            repetitions=15,
            weight=50.0,
            date=datetime.strptime("2024-12-07", '%Y-%m-%d'),
            comment="Workout to delete"
        )
        db.session.add(log)
        db.session.commit()

        db.session.delete(log)
        db.session.commit()

        fetched_log = ExerciseLog.query.filter_by(user_id=self.user.id).first()
        self.assertIsNone(fetched_log)

if __name__ == '__main__':
    unittest.main()
