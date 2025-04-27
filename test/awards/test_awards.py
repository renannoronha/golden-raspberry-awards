"""
Integration tests for the /awards/longest-fastest-consecutive-awards endpoint.

This module contains tests that verify the behavior of the endpoint that
returns information about producers with the longest and shortest intervals
between consecutive award wins.
"""
from src.model.awards import Awards
from src.service.db import db


def test_awards_longest_fastest_consecutive_awards(client):
    """
    Test the basic functionality of the consecutive awards endpoint.
    
    This test verifies that the endpoint returns the expected data format
    with the correct producer and interval information using the test dataset
    provided.
    
    Args:
        client: Flask test client fixture from conftest.py
    """
    response = client.get("/awards/longest-fastest-consecutive-awards")
    assert response.status_code == 200
    assert response.json == {
        "max": [],
        "min": [{
            "followingWin": 1990,
            "interval": 6,
            "previousWin": 1984,
            "producer": "Bo Derek",
        }]
    }


def test_awards_endpoint_structure(client):
    """
    Test the structure of the response from the consecutive awards endpoint.
    
    This test verifies that the response contains the expected keys and
    that the values have the correct structure, regardless of actual data.
    
    Args:
        client: Flask test client fixture from conftest.py
    """
    response = client.get("/awards/longest-fastest-consecutive-awards")
    assert response.status_code == 200

    # Check response structure
    assert "min" in response.json
    assert "max" in response.json
    assert isinstance(response.json["min"], list)
    assert isinstance(response.json["max"], list)

    # Check structure of items if they exist
    for item in response.json["min"] + response.json["max"]:
        assert "producer" in item
        assert "interval" in item
        assert "previousWin" in item
        assert "followingWin" in item
        assert item["followingWin"] > item["previousWin"]
        assert item["interval"] == item["followingWin"] - item["previousWin"]


def test_awards_custom_dataset(client, application):
    """
    Test the endpoint with a custom dataset inserted directly into the database.
    
    This test creates a controlled dataset that ensures predictable interval calculations
    and verifies that the endpoint correctly identifies the min and max intervals.
    
    Args:
        client: Flask test client fixture from conftest.py
        application: Flask application fixture from conftest.py
    """
    with application.app_context():
        # Clear existing data
        db.session.query(Awards).delete()
        db.session.commit()

        # Insert custom test data with known intervals
        test_data = [
            Awards(1980, "Film A", "Studio A", "Producer X", True),
            Awards(1984, "Film B", "Studio B", "Producer X", True),  # 4 year interval
            Awards(1990, "Film C", "Studio C", "Producer X", True),  # 6 year interval
            Awards(1985, "Film D", "Studio D", "Producer Y", True),
            Awards(1995, "Film E", "Studio E", "Producer Y", True),  # 10 year interval
            Awards(2000, "Film F", "Studio F", "Producer Z", True),
            Awards(2001, "Film G", "Studio G", "Producer Z", True),  # 1 year interval
        ]

        for award in test_data:
            db.session.add(award)
        db.session.commit()

        response = client.get("/awards/longest-fastest-consecutive-awards")
        assert response.status_code == 200

        # Check that the correct min and max intervals are identified
        min_intervals = [item["interval"] for item in response.json["min"]]
        max_intervals = [item["interval"] for item in response.json["max"]]

        assert 1 in min_intervals  # Producer Z has 1 year interval
        assert 10 in max_intervals  # Producer Y has 10 year interval


def test_awards_no_consecutive_winners(client, application):
    """
    Test the endpoint when there are no consecutive winners.
    
    This test creates a dataset where no producer has won multiple awards,
    and verifies that the endpoint handles this case appropriately.
    
    Args:
        client: Flask test client fixture from conftest.py
        application: Flask application fixture from conftest.py
    """
    with application.app_context():
        # Clear existing data
        db.session.query(Awards).delete()
        db.session.commit()

        # Insert data with no consecutive wins by any producer
        test_data = [
            Awards(1980, "Film A", "Studio A", "Producer W", True),
            Awards(1981, "Film B", "Studio B", "Producer X", True),
            Awards(1982, "Film C", "Studio C", "Producer Y", True),
            Awards(1983, "Film D", "Studio D", "Producer Z", True),
        ]

        for award in test_data:
            db.session.add(award)
        db.session.commit()

        response = client.get("/awards/longest-fastest-consecutive-awards")
        assert response.status_code == 200

        # With no consecutive wins, both lists should be empty
        assert response.json["min"] == []
        assert response.json["max"] == []


def test_awards_same_min_max_interval(client, application):
    """
    Test the endpoint when min and max intervals are the same.
    
    This test creates a dataset where all producers have the same interval
    between consecutive wins, verifying that the endpoint correctly handles
    this case by including all producers in the min list and none in the max.
    
    Args:
        client: Flask test client fixture from conftest.py
        application: Flask application fixture from conftest.py
    """
    with application.app_context():
        # Clear existing data
        db.session.query(Awards).delete()
        db.session.commit()

        # Insert data where all producers have the same interval (5 years)
        test_data = [
            Awards(1980, "Film A", "Studio A", "Producer X", True),
            Awards(1985, "Film B", "Studio B", "Producer X", True),  # 5 year interval
            Awards(1990, "Film C", "Studio C", "Producer Y", True),
            Awards(1995, "Film D", "Studio D", "Producer Y", True),  # 5 year interval
        ]

        for award in test_data:
            db.session.add(award)
        db.session.commit()

        response = client.get("/awards/longest-fastest-consecutive-awards")
        assert response.status_code == 200

        # All producers should be in the min list, max list should be empty
        assert len(response.json["min"]) == 2
        assert response.json["max"] == []

        # Verify all intervals are 5
        for item in response.json["min"]:
            assert item["interval"] == 5


def test_multiple_producers_same_intervals(client, application):
    """
    Test the endpoint when multiple producers have the same min/max intervals.
    
    This test verifies that all producers with the same interval are included
    in their respective min/max lists.
    
    Args:
        client: Flask test client fixture from conftest.py
        application: Flask application fixture from conftest.py
    """
    with application.app_context():
        # Clear existing data
        db.session.query(Awards).delete()
        db.session.commit()

        # Create dataset with multiple producers having same min and max intervals
        test_data = [
            # Producer X: 2-year interval (minimum)
            Awards(2000, "Film A", "Studio A", "Producer X", True),
            Awards(2002, "Film B", "Studio A", "Producer X", True),

            # Producer Y: 2-year interval (minimum too)
            Awards(2010, "Film C", "Studio B", "Producer Y", True),
            Awards(2012, "Film D", "Studio B", "Producer Y", True),

            # Producer Z: 8-year interval (maximum)
            Awards(2000, "Film E", "Studio C", "Producer Z", True),
            Awards(2008, "Film F", "Studio C", "Producer Z", True),

            # Producer W: 8-year interval (maximum too)
            Awards(2005, "Film G", "Studio D", "Producer W", True),
            Awards(2013, "Film H", "Studio D", "Producer W", True),
        ]

        for award in test_data:
            db.session.add(award)
        db.session.commit()

        response = client.get("/awards/longest-fastest-consecutive-awards")
        assert response.status_code == 200

        # Check that all producers with minimum intervals are in min list
        min_producers = {item["producer"] for item in response.json["min"]}
        assert "Producer X" in min_producers
        assert "Producer Y" in min_producers
        assert len(response.json["min"]) == 2

        # Check that all producers with maximum intervals are in max list
        max_producers = {item["producer"] for item in response.json["max"]}
        assert "Producer Z" in max_producers
        assert "Producer W" in max_producers
        assert len(response.json["max"]) == 2


def test_producers_with_multiple_consecutive_wins(client, application):
    """
    Test producers with multiple sequences of consecutive wins.
    
    This test verifies that the endpoint correctly identifies all pairs of 
    consecutive wins and their intervals for the same producer.
    
    Args:
        client: Flask test client fixture from conftest.py
        application: Flask application fixture from conftest.py
    """
    with application.app_context():
        # Clear existing data
        db.session.query(Awards).delete()
        db.session.commit()

        # Producer X with multiple winning periods with different intervals
        test_data = [
            # First sequence: 2-year interval
            Awards(1990, "Film A", "Studio A", "Producer X", True),
            Awards(1992, "Film B", "Studio A", "Producer X", True),

            # Second sequence: 5-year interval
            Awards(1992, "Film B", "Studio A", "Producer X", True),  # Already added above
            Awards(1997, "Film C", "Studio A", "Producer X", True),

            # Third sequence: 3-year interval
            Awards(1997, "Film C", "Studio A", "Producer X", True),  # Already added above
            Awards(2000, "Film D", "Studio A", "Producer X", True),
        ]

        for award in test_data:
            db.session.add(award)
        db.session.commit()

        response = client.get("/awards/longest-fastest-consecutive-awards")
        assert response.status_code == 200

        # Verify 2 year min interval
        for item in response.json["min"]:
            assert item["interval"] == 2

        # Verify 5 year max interval
        for item in response.json["max"]:
            assert item["interval"] == 5

        # Verify that the producer is correctly identified
        for item in response.json["min"] + response.json["max"]:
            assert item["producer"] == "Producer X"


def test_empty_database(client, application):
    """
    Test the endpoint behavior with an empty database.
    
    This test verifies that the endpoint handles the case when there
    are no records in the database at all.
    
    Args:
        client: Flask test client fixture from conftest.py
        application: Flask application fixture from conftest.py
    """
    with application.app_context():
        # Clear all data from database
        db.session.query(Awards).delete()
        db.session.commit()

        response = client.get("/awards/longest-fastest-consecutive-awards")
        assert response.status_code == 200

        # Response should have empty min and max lists
        assert response.json == {"min": [], "max": []}


def test_similar_producer_names(client, application):
    """
    Test the endpoint with producers that have similar names.
    
    This test verifies that the endpoint correctly differentiates between 
    producers with similar names when calculating intervals.
    
    Args:
        client: Flask test client fixture from conftest.py
        application: Flask application fixture from conftest.py
    """
    with application.app_context():
        # Clear existing data
        db.session.query(Awards).delete()
        db.session.commit()

        # Create producers with similar names
        test_data = [
            # Producer John
            Awards(2000, "Film A", "Studio A", "John", True),
            Awards(2003, "Film B", "Studio A", "John", True),  # 3-year interval

            # Producer John Smith
            Awards(2005, "Film C", "Studio B", "John Smith", True),
            Awards(2012, "Film D", "Studio B", "John Smith", True),  # 7-year interval
        ]

        for award in test_data:
            db.session.add(award)
        db.session.commit()

        response = client.get("/awards/longest-fastest-consecutive-awards")
        assert response.status_code == 200

        # Find the intervals for each producer
        john_interval = None
        john_smith_interval = None

        for category in ["min", "max"]:
            for item in response.json[category]:
                if item["producer"] == "John":
                    john_interval = item["interval"]
                if item["producer"] == "John Smith":
                    john_smith_interval = item["interval"]

        # Verify that the intervals are calculated correctly
        assert john_interval == 3
        assert john_smith_interval == 7


def test_large_dataset(client, application):
    """
    Test the endpoint with a large dataset.
    
    This test uses large number of records to verify the endpoint.
    
    Args:
        client: Flask test client fixture from conftest.py
        application: Flask application fixture from conftest.py
    """
    with application.app_context():
        # Clear existing data
        db.session.query(Awards).delete()
        db.session.commit()

        test_data = []

        # Add a known minimum interval (1 year)
        test_data.append(Awards(2000, "Benchmark Min 1", "Studio Test", "Benchmark Producer", True))
        test_data.append(Awards(2001, "Benchmark Min 2", "Studio Test", "Benchmark Producer", True))

        # Add a known maximum interval (20 years)
        test_data.append(Awards(2001, "Benchmark Max 1", "Studio Test", "Benchmark Producer Max", True))
        test_data.append(Awards(2021, "Benchmark Max 2", "Studio Test", "Benchmark Producer Max", True))

        # Generate 100 producers with random intervals
        for i in range(1000):
            producer = f"Producer {i}"
            start_year = 1980 + i % 20

            # Add 3-5 awards for each producer
            for j in range(3, 6):
                test_data.append(Awards(start_year + j * 2, f"Film {i}-{j}", f"Studio {i}", producer, True))

        # Bulk insert all records
        for award in test_data:
            db.session.add(award)
        db.session.commit()

        response = client.get("/awards/longest-fastest-consecutive-awards")

        assert response.status_code == 200

        # Check for our benchmark producers
        min_producers = [item["producer"] for item in response.json["min"]]
        max_producers = [item["producer"] for item in response.json["max"]]

        assert "Benchmark Producer" in min_producers
        assert "Benchmark Producer Max" in max_producers


def test_multiple_awards_same_year(client, application):
    """
    Test with a producer who has multiple awards in the same year.
    
    This tests verifies that the endpoint correctly handles the case when
    a producer wins multiple awards in the same year, which shouldn't count
    as a consecutive win with an interval of 0.
    
    Args:
        client: Flask test client fixture from conftest.py
        application: Flask application fixture from conftest.py
    """
    with application.app_context():
        # Clear existing data
        db.session.query(Awards).delete()
        db.session.commit()

        # Producer with multiple awards in the same year
        test_data = [
            Awards(2000, "Film A", "Studio A", "Producer X", True),
            Awards(2000, "Film B", "Studio B", "Producer X", True),  # Same year
            Awards(2005, "Film C", "Studio C", "Producer X", True),  # 5 year interval from either
        ]

        for award in test_data:
            db.session.add(award)
        db.session.commit()

        response = client.get("/awards/longest-fastest-consecutive-awards")
        assert response.status_code == 200

        # Verify the interval is calculated from the first win in 2000 to 2005
        intervals = []
        for category in ["min", "max"]:
            for item in response.json[category]:
                if item["producer"] == "Producer X":
                    intervals.append(item["interval"])

        # Should be a 5-year interval (from 2000 to 2005)
        assert 5 in intervals
        # Should not have a 0-year interval
        assert 0 not in intervals


def test_with_long_gaps(client, application):
    """
    Test with producers that have wins with long gaps.
    
    This test verifies that the endpoint correctly identifies pairs that
    form valid intervals, even when there are large gaps between wins.
    
    Args:
        client: Flask test client fixture from conftest.py
        application: Flask application fixture from conftest.py
    """
    with application.app_context():
        # Clear existing data
        db.session.query(Awards).delete()
        db.session.commit()

        # Producer with very spread out wins
        test_data = [
            Awards(1980, "Film A", "Studio A", "Producer X", True),
            Awards(2023, "Film B", "Studio B", "Producer X", True),  # 43 year gap
            Awards(1990, "Film C", "Studio C", "Producer Y", True),
            Awards(1991, "Film D", "Studio D", "Producer Y", True),  # 1 year gap
        ]

        for award in test_data:
            db.session.add(award)
        db.session.commit()

        response = client.get("/awards/longest-fastest-consecutive-awards")
        assert response.status_code == 200

        # Verify Producer X has the max interval (43 years)
        max_producers = [item["producer"] for item in response.json["max"]]
        assert "Producer X" in max_producers

        # Verify Producer Y has the min interval (1 year)
        min_producers = [item["producer"] for item in response.json["min"]]
        assert "Producer Y" in min_producers

        # Check the actual intervals
        for item in response.json["max"]:
            if item["producer"] == "Producer X":
                assert item["interval"] == 43

        for item in response.json["min"]:
            if item["producer"] == "Producer Y":
                assert item["interval"] == 1


def test_with_special_characters_in_producer_names(client, application):
    """
    Test with producer names containing special characters.
    
    This test verifies that the endpoint correctly handles producer names
    with special characters, ensuring they're treated as distinct entities.
    
    Args:
        client: Flask test client fixture from conftest.py
        application: Flask application fixture from conftest.py
    """
    with application.app_context():
        # Clear existing data
        db.session.query(Awards).delete()
        db.session.commit()

        # Add producers with special characters in names
        test_data = [
            Awards(2000, "Film A", "Studio A", "Producer-X", True),  # Hyphen
            Awards(2004, "Film B", "Studio B", "Producer-X", True),
            Awards(2001, "Film C", "Studio C", "Producer & Co.", True),  # Ampersand
            Awards(2005, "Film D", "Studio D", "Producer & Co.", True),
            Awards(2002, "Film E", "Studio E", "Producer's Group", True),  # Apostrophe
            Awards(2006, "Film F", "Studio F", "Producer's Group", True),
        ]

        for award in test_data:
            db.session.add(award)
        db.session.commit()

        response = client.get("/awards/longest-fastest-consecutive-awards")
        assert response.status_code == 200

        # Get all producers from the response
        all_producers = []
        for category in ["min", "max"]:
            all_producers.extend([item["producer"] for item in response.json[category]])

        # Check that special character producers are included
        assert "Producer-X" in all_producers
        assert "Producer & Co." in all_producers
        assert "Producer's Group" in all_producers


def test_winner_false_excluded(client, application):
    """
    Test that non-winning movies are excluded from interval calculations.
    
    This test verifies that the endpoint correctly ignores movies where
    winner=False when calculating intervals between consecutive wins.
    
    Args:
        client: Flask test client fixture from conftest.py
        application: Flask application fixture from conftest.py
    """
    with application.app_context():
        # Clear existing data
        db.session.query(Awards).delete()
        db.session.commit()

        # Add a producer with wins and non-wins
        test_data = [
            Awards(2000, "Film A", "Studio A", "Producer X", True),  # Win
            Awards(2001, "Film B", "Studio B", "Producer X", False),  # Non-win
            Awards(2005, "Film C", "Studio C", "Producer X", True),  # Win
        ]

        for award in test_data:
            db.session.add(award)
        db.session.commit()

        response = client.get("/awards/longest-fastest-consecutive-awards")
        assert response.status_code == 200

        # Find Producer X's interval
        producer_x_interval = None
        for category in ["min", "max"]:
            for item in response.json[category]:
                if item["producer"] == "Producer X":
                    producer_x_interval = item["interval"]

        # Interval should be 5 years (from 2000 to 2005), not 1 year (which would include the non-win)
        assert producer_x_interval == 5


def test_malformed_data_resilience(client, application):
    """
    Test the endpoint's resilience to malformed data.
    
    This test verifies that the endpoint continues to function correctly
    when the database contains malformed records.
    
    Args:
        client: Flask test client fixture from conftest.py
        application: Flask application fixture from conftest.py
    """
    with application.app_context():
        # Clear existing data
        db.session.query(Awards).delete()
        db.session.commit()

        # Add a mix of valid and malformed data
        test_data = [
            # Valid records
            Awards(2000, "Film A", "Studio A", "Producer X", True),
            Awards(2005, "Film B", "Studio B", "Producer X", True),

            # Records with None in non-nullable fields (these should fail to insert)
            Awards(None, "Film C", "Studio C", "Producer Y", True),  # None year 
            Awards(2010, None, "Studio D", "Producer Z", True),  # None title

            # Records with unusual values
            Awards(-1000, "Film E", "Studio E", "Producer W", True),  # Negative year
            Awards(9999, "Film F", "Studio F", "Producer V", True),  # Far future year
        ]

        # Insert valid records only, skip ones that would violate constraints
        for award in test_data:
            if award.year is not None and award.title is not None:
                db.session.add(award)

        db.session.commit()

        response = client.get("/awards/longest-fastest-consecutive-awards")
        assert response.status_code == 200

        # Verify that valid records are still processed correctly
        has_valid_producer = False
        for category in ["min", "max"]:
            for item in response.json[category]:
                if item["producer"] == "Producer X":
                    has_valid_producer = True
                    assert item["interval"] == 5

        assert has_valid_producer, "Valid producer data should still be processed correctly"


def test_invalid_negative_interval(client, application):
    """
    Test that the endpoint doesn't report negative intervals.
    
    This test verifies that if there's any data that could produce a negative interval
    (due to incorrect time ordering), it's correctly filtered out.
    
    Args:
        client: Flask test client fixture from conftest.py
        application: Flask application fixture from conftest.py
    """
    with application.app_context():
        # Clear existing data
        db.session.query(Awards).delete()
        db.session.commit()

        # Add awards with years that could produce negative intervals if not filtered correctly
        test_data = [
            # Even though we insert 2010 first, the next_win query should find 2005 when sorting by year
            Awards(2010, "Film A", "Studio A", "Producer X", True),
            Awards(2005, "Film B", "Studio B", "Producer X", True),

            # Control group with proper ordering
            Awards(2000, "Film C", "Studio C", "Producer Y", True),
            Awards(2003, "Film D", "Studio D", "Producer Y", True),
        ]

        for award in test_data:
            db.session.add(award)
        db.session.commit()

        response = client.get("/awards/longest-fastest-consecutive-awards")
        assert response.status_code == 200

        # There should be no negative intervals and Producer Y should be included
        producer_y_found = False
        for category in ["min", "max"]:
            for item in response.json[category]:
                assert item["interval"] > 0, "Intervals should always be positive"
                if item["producer"] == "Producer Y":
                    producer_y_found = True
                    assert item["interval"] == 3

        assert producer_y_found, "Producer Y with valid interval should be included"
