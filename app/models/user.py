import os
from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    """
     Represents a user in the system.

     This class defines the structure of the 'user' table in the database,
     with columns for 'id', 'username', and 'password_hash'. The 'id' is
     the primary key, 'username' is unique, and 'password_hash' stores the
     hashed password.

     Methods:
         set_password(password):
             Sets the user's password by hashing it and storing it in the database.

         check_password(password):
             Checks if the provided password matches the stored hashed password.

     Attributes:
         id (int): The unique identifier for each user.
         username (str): The username of the user (must be unique).
         password_hash (str): The hashed password of the user.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    salt = db.Column(db.String(128))

    def set_password(self, password):
        """
             Hashes the provided password and stores it in the 'password_hash' column.

             Args:
                 password (str): The plain-text password to be hashed.
            Notes:
                A unique salt is generated using os.urandom() to ensure that even if two users have the same password,
                their hashes will be different.
        """
        self.salt = os.urandom(16).hex()
        self.password_hash = generate_password_hash(password + self.salt)

    def check_password(self, password):
        """
        Compares the provided password with the stored hashed password.

            Args:
                password (str): The plain-text password to check.
            Returns:
                bool: True if the password matches the stored hash, otherwise False.
        """
        return check_password_hash(self.password_hash, password + self.salt)
