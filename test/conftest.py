"""
Pytest configuration module for the Golden Raspberry Awards test suite.

This module provides fixtures and configuration for running automated tests,
including setting up test environments, database connections, and application clients.
"""
from src.service.db import db  # SQLAlchemy database instance
from src.model.awards import Awards  # Awards model for loading dataset
from os import environ, path
import pytest

# Configure environment variables for testing
# Using in-memory SQLite database for testing to ensure isolation and speed
environ["DATABASE_URL"] = "sqlite:///:memory:"
# Set the path to the test dataset - using the directory of this file as base
environ["INITIAL_DATASET_PATH"] = path.dirname(path.abspath(__file__)) + "/Movielist.csv"
# Define the delimiter used in the test CSV file
environ["CSV_DELIMITER"] = ";"

# Import the Flask application AFTER setting environment variables to ensure it's initialized with the test configuration
from src.api import app


@pytest.fixture()
def application():
    """
    Fixture to provide the Flask application instance.
    
    Returns:
        Flask: The configured Flask application instance for testing.
    """

    # Making sure to use current app context
    with app.app_context():
        # Initialize database schema
        db.create_all()

        # Load initial data from the CSV file into the database
        Awards.load_dataset()

    yield app  # Yield allows for setup/teardown if needed in the future


@pytest.fixture()
def client(application):
    """
    Fixture to provide a Flask test client.
    
    This fixture configures the application in testing mode and returns
    a test client for making requests against the API.
    
    Args:
        application: The Flask application fixture.
        
    Returns:
        FlaskClient: A test client for the application.
    """
    # Configure application for testing
    application.config.update({
        "TESTING": True,  # Enable testing mode for Flask
    })
    return application.test_client()


@pytest.fixture()
def config(application):
    """
    Fixture to provide access to the application configuration.
    
    This fixture allows tests to check or modify the application
    configuration during testing.
    
    Args:
        application: The Flask application fixture.
        
    Returns:
        dict: The application configuration dictionary.
    """
    # Configure application for testing
    application.config.update({
        "TESTING": True,  # Enable testing mode for Flask
    })
    return application.config
