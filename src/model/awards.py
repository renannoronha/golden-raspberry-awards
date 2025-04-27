"""
Awards model module for the Golden Raspberry Awards application.

This module defines the database model for movie awards, including data structure,
initialization logic, data loading functionality, and analytical queries.
"""
from sqlalchemy import Column, Integer, String, Boolean, and_, select, exists, func
from sqlalchemy.orm import aliased

from src.service.db import db
from os import environ
import csv


class Awards(db.Model):
    __tablename__ = "awards"

    id = Column(Integer, primary_key=True)
    year = Column(Integer, nullable=False)  # Year when the award was given
    title = Column(String, nullable=False)  # Movie title
    studios = Column(String, nullable=True)  # Studios that produced the movie
    producers = Column(String, nullable=True)  # Producers of the movie
    winner = Column(Boolean, nullable=True)  # Whether the movie won the award

    def __init__(self, year, title, studios, producers, winner):
        """
        Initialize an Awards instance with movie data.
        
        Args:
            year (int): The year when the award was given
            title (str): The title of the movie
            studios (str): The studios that produced the movie
            producers (str): The producers of the movie
            winner (str/bool): Whether the movie won ('yes'/'no'/True/False)
        """
        self.year = year
        self.title = title
        self.studios = studios
        self.producers = producers
        self.winner = winner if type(winner) == bool else (str(winner) == 'yes')  # If winner is boolean do nothing, else make sure it's string and convert 'yes'/'no' to True/False

    @classmethod
    def load_dataset(self):
        """
        Load the initial dataset from a CSV file into the database.
        
        This method reads the CSV file specified in the INITIAL_DATASET_PATH
        environment variable, parses each row into an Awards object, and
        commits the data to the database.
        
        Raises:
            ValueError: If the INITIAL_DATASET_PATH environment variable is not set
        """
        print("Setting up the database...")
        db.create_all()

        # Get the dataset path from environment variable
        dataset_path = environ.get("INITIAL_DATASET_PATH")
        if dataset_path is None:
            raise ValueError("INITIAL_DATASET_PATH environment variable is not set")

        with open(dataset_path, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file, delimiter=";")
            for row in reader:
                movie = self(
                    year=int(row["year"]),
                    title=row["title"],
                    studios=row["studios"],
                    producers=row["producers"],
                    winner=row["winner"],
                )
                db.session.add(movie)
            db.session.commit()

        print("Database setup complete.")

    def to_dict(self):
        """
        Convert the Awards object to a dictionary.
        
        Returns:
            dict: Dictionary representation of the Awards object
        """
        return {"id": self.id, "year": self.year, "title": self.title, "studios": self.studios, "producers": self.producers, "winner": self.winner}

    @classmethod
    def get_longest_fastest_consecutive_awards(self):
        """
        Find producers with the shortest and longest intervals between consecutive award wins.
        
        This method uses SQL Common Table Expressions (CTEs) to calculate the intervals
        between consecutive wins for each producer and identifies the minimum and maximum
        intervals.
        
        Returns:
            dict: Dictionary containing lists of producers with the shortest and longest intervals
        """
        # Create alias for self-join operations
        AwardAlias = aliased(self)

        # Subquery to find the next win for each producer
        subquery_next_win = select(AwardAlias.year).where(
            AwardAlias.winner == True,  # Only consider winners
            AwardAlias.producers == self.producers,  # Same producer
            AwardAlias.year > self.year,  # Next win must be after the current year
        ).order_by(AwardAlias.year).limit(1).scalar_subquery()

        # Calculate the interval between consecutive wins
        subquery_interval = subquery_next_win - self.year

        # CTE 'difference' to calculate intervals and next wins
        difference_cte = select(self.id, self.year, self.producers, subquery_next_win.label('next_win'), subquery_interval.label('interval')).where(self.winner == True).cte('difference')

        # Find minimum interval from the 'difference' CTE
        min_interval_subquery = select(func.min(difference_cte.c.interval)).scalar_subquery()

        # CTE 'min' to find producers with the minimum interval
        min_cte = select(difference_cte.c.producers, difference_cte.c.interval, difference_cte.c.year, difference_cte.c.next_win).where(difference_cte.c.interval == min_interval_subquery).cte('min')

        # Find maximum interval from the 'difference' CTE
        max_interval_subquery = select(func.max(difference_cte.c.interval)).scalar_subquery()

        # CTE 'max' to find producers with the maximum interval
        max_cte = select(
            difference_cte.c.producers,
            difference_cte.c.interval,
            difference_cte.c.year,
            difference_cte.c.next_win,
        ).where(and_(
            difference_cte.c.interval == max_interval_subquery,
            difference_cte.c.interval != min_interval_subquery,  # Ensure it's not the same as min
        )).cte('max')

        # Execute the queries to get the results
        min_result = db.session.execute(select(min_cte)).all()
        max_result = db.session.execute(select(max_cte)).all()

        # Format the results into the expected output structure
        return {
            "min": [{
                "producer": award[0],
                "interval": award[1],
                "previousWin": award[2],
                "followingWin": award[3]
            } for award in min_result],
            "max": [{
                "producer": award[0],
                "interval": award[1],
                "previousWin": award[2],
                "followingWin": award[3]
            } for award in max_result],
        }
