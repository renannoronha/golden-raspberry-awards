"""
API configuration module for the Golden Raspberry Awards application.

This module sets up the Flask application, configures the database connection,
initializes Flask-RESTX for API documentation, and enables CORS for cross-origin requests.
"""
from flask import Flask
from flask_restx import Api  # Extension for building RESTful APIs with Swagger documentation

from src.service.db import db  # SQLAlchemy database instance

from src.resource.awards import awards_ns  # API namespace for award-related endpoints

from os import environ

# Create and configure the Flask application
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = environ["DATABASE_URL"]  # Configure SQLAlchemy with database URL from environment variables
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # Disable modification tracking to improve performance
db.init_app(app)  # Initialize the SQLAlchemy instance

# Create a Flask-RESTX API instance with documentation metadata
api = Api(app, version="1.0", title="Golden Raspberry Awards", description="Documentação para consulta da API do Golden Raspberry Awards")

# Register API namespaces
api.add_namespace(awards_ns)  # Add the awards namespace to the API
