"""
Database service module for the Golden Raspberry Awards application.

This module initializes the SQLAlchemy database instance that will be used
throughout the application. The database connection itself is configured
in the main application entry point.
"""
from flask_sqlalchemy import SQLAlchemy  # Flask extension for SQLAlchemy ORM

# Create a SQLAlchemy instance without binding it to an app
# This instance will be initialized with the Flask app in api.py using init_app()
db = SQLAlchemy()
