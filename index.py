"""
Main entry point for the Golden Raspberry Awards application.

This script initializes environment variables, sets up the database, loads the initial dataset,
and starts the Flask web server.
"""
from os import environ

# Configure environment variables for the application
environ["DATABASE_URL"] = "sqlite:///:memory:"  # Using in-memory SQLite database
environ["INITIAL_DATASET_PATH"] = "Movielist.csv"  # Path to the CSV dataset file
environ["CSV_DELIMITER"] = ";"  # Delimiter used in the CSV file

# Import application components after setting environment variables
# to ensure they use the correct configuration
from src.api import app, db  # Flask application and database instances
from src.model.awards import Awards  # Awards model

if __name__ == "__main__":
    # Execute only when run directly (not when imported)

    # Making sure to use current app context
    with app.app_context():
        # Initialize database schema
        db.create_all()

        # Load initial data from the CSV file into the database
        Awards.load_dataset()

    # Start the Flask development server with default settings (host='127.0.0.1', port=5000)
    app.run()
