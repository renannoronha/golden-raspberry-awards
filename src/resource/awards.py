"""
Award resources module for the Golden Raspberry Awards API.

This module defines the API endpoints related to award information,
including the endpoint for retrieving data about consecutive awards.
"""
from flask_restx import Namespace, Resource
from src.core.awards import AwardsCore  # Core business logic for awards

import traceback  # For detailed error tracking

# Define API namespace for award-related endpoints
awards_ns = Namespace("awards", description="Prêmios")


@awards_ns.route("/longest-fastest-consecutive-awards")
class ListRegionResource(Resource):
    """
    Resource for retrieving information about consecutive award intervals.
    
    This endpoint provides data about producers with the longest and shortest
    intervals between consecutive awards.
    """

    @awards_ns.doc(description="Intervalo de prêmios")
    def get(self):
        """
        Get the producers with the longest and shortest intervals between consecutive awards.
        
        Returns:
            tuple: A tuple containing:
                - dict: JSON response with min and max intervals data
                - int: HTTP status code (200 for success, 400 for error)
        """
        try:
            # Call the business logic layer to get the award intervals
            return AwardsCore().get_longest_fastest_consecutive_awards()
        except Exception as e:
            # Log any errors that occur during processing
            print(f"Error: {e}")
            print(traceback.format_exc())  # Print detailed stack trace for debugging
            return {}, 400  # Return empty response with 400 Bad Request status code
