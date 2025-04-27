"""
Core business logic module for the Golden Raspberry Awards application.

This module provides the business logic layer between the API resources
and the data models, handling award-related operations and data processing.
"""
from src.model.awards import Awards  # Import the Awards data model


class AwardsCore:

    def __init__(self, *args, **kwargs):
        """
        Initialize the AwardsCore instance.
        
        Args:
            *args: Variable length argument list (not used currently).
            **kwargs: Arbitrary keyword arguments (not used currently).
        
        The constructor sets up the reference to the Awards model.
        """
        self.model = Awards  # Reference to the Awards data model for database operations

    def get_longest_fastest_consecutive_awards(self):
        """
        Get information about the longest and fastest intervals between consecutive awards.
        
        This method delegates to the model layer to fetch data about producers who have
        won multiple awards and the intervals between their consecutive wins.
        
        Returns:
            tuple: A tuple containing:
                - dict: A dictionary with two keys:
                    - "min": List of producers with the shortest intervals between wins
                    - "max": List of producers with the longest intervals between wins
                - int: HTTP status code (200 for success)
        """
        # Call the model method to retrieve the data
        response = self.model.get_longest_fastest_consecutive_awards()

        # Return the response data with a 200 OK status code
        return response, 200
