import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
db = SQLAlchemy()
migrate = Migrate()

logger = logging.getLogger(__name__)


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

    try:
        logger.info("Starting app initialization...")
        app.config.from_object(Config)
        logger.info("Configuration loaded successfully.")

        db.init_app(app)
        logger.info("Database initialized successfully.")

        migrate.init_app(app, db)
        logger.info("Migrations setup completed.")

        from app.routes import auth_bp
        app.register_blueprint(auth_bp)
        logger.info("Blueprints registered successfully.")

        logger.info("App initialization completed.")
    except Exception as e:
        logger.error(f"Error during app initialization: {e}")
        raise

    return app