import logging

from app import create_app, db
from flask_migrate import Migrate # Ensure import Migrate


logger = logging.getLogger(__name__)


app = create_app()

# initialize Flask-Migrate
migrate = Migrate(app, db)  # connect Flask-Migrate with app and db 

if __name__ == '__main__':
    try:
        logger.info("Starting the Flask application...")
        app.run(debug=True)
    except Exception as e:
        logger.error(f"An error occurred while running the application: {e}")
    finally:
        logger.info("Shutting down the Flask application.")