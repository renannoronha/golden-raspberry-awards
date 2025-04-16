from sqlalchemy import text

from os import environ


class SetDatabase:

    def set_database(self):
        """Set the database for the application"""
        print("Setting up the database...")

        from src.service.db import DB

        # Get the database URL from environment variables
        db_url = environ.get("DATABASE_URL")
        if db_url is None:
            raise ValueError("DATABASE_URL environment variable is not set")

        # Initialize the database with the URL
        db = DB()

        with db.engine.begin() as conn:
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS awards (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    year INTEGER NOT NULL,
                    title TEXT NOT NULL,
                    studios TEXT NOT NULL,
                    producers TEXT NOT NULL,
                    winner TEXT NOT NULL
                );
            """))
            conn.commit()

        # Get the dataset path from environment variable
        dataset_path = environ.get("INITIAL_DATASET_PATH")
        if dataset_path is None:
            raise ValueError("INITIAL_DATASET_PATH environment variable is not set")

        with db.engine.begin() as conn:
            # Delete the previous data
            conn.execute(text("DELETE FROM awards"))

            with open(dataset_path, "r") as file:
                for i, line in enumerate(file):
                    # Skip the header line
                    if i == 0:
                        continue

                    # Skip empty lines
                    if not line.strip():
                        continue

                    # Split the line by the delimiter
                    year, title, studios, producers, winner = line.strip().split(environ.get("CSV_DELIMITER", ","))
                    payload = {"year": year, "title": title, "studios": studios, "producers": producers, "winner": winner}
                    # print(payload)

                    # Insert the data into the database
                    conn.execute(text("""
                        INSERT INTO awards (year, title, studios, producers, winner)
                        VALUES (:year, :title, :studios, :producers, :winner);
                    """), payload)
            conn.commit()

        print("Database setup complete.")
