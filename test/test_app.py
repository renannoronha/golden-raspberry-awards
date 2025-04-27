"""
Application configuration tests for the Golden Raspberry Awards application.

This module contains tests that verify the Flask application is correctly configured
for testing, including validation of application name and environment settings.
"""


def test_app_is_created(application):
    """
    Test that the Flask application is created with the correct name.
    
    This test verifies that the application has the expected module name,
    ensuring it was properly initialized from the src.api module.
    
    Args:
        application: The Flask application fixture from conftest.py
    """
    assert application.name == "src.api"


def test_debug_is_false(config):
    """
    Test that debug mode is disabled in the test environment.
    
    This ensures that the application is not running in debug mode during tests,
    which could affect test behavior and results.
    
    Args:
        config: The application configuration fixture from conftest.py
    """
    assert config["DEBUG"] is False


def test_testing_is_true(config):
    """
    Test that testing mode is enabled in the test environment.
    
    This ensures that the application is configured for testing,
    which enables Flask's test-specific behaviors like error handling.
    
    Args:
        config: The application configuration fixture from conftest.py
    """
    assert config["TESTING"] is True
