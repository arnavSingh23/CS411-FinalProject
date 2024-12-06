from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
db = SQLAlchemy()
migrate = Migrate()


def create_app():
    """
     Creates and configures the Flask application instance.

     This function initializes a new Flask application, loads configurations
     from the provided Config class, and sets up SQLAlchemy and database
     migration tools.

     Returns:
         Flask: The configured Flask application instance.

     Raises:
         Exception: If any configuration or setup step fails (e.g., database connection issues).
     """
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes import auth_bp
    app.register_blueprint(auth_bp)

    return app
