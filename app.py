import logging

from app import create_app, db


logger = logging.getLogger(__name__)


app = create_app()

if __name__ == '__main__':
    try:
        logger.info("Starting the Flask application...")
        app.run(debug=True)
    except Exception as e:
        logger.error(f"An error occurred while running the application: {e}")
    finally:
        logger.info("Shutting down the Flask application.")