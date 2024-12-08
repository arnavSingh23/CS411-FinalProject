from app import db

class ExerciseLog(db.Model):
    """
    Represents a workout log entry for a user.
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)  # connect with user's list
    exercise_id = db.Column(db.Integer, nullable=False)  # Wger workout ID
    repetitions = db.Column(db.Integer, nullable=False)  
    weight = db.Column(db.Float, nullable=True)        
    date = db.Column(db.Date, nullable=False)           
    comment = db.Column(db.String(256), nullable=True)  

    def __repr__(self):
        return f"<ExerciseLog {self.id} {self.exercise_id}>"