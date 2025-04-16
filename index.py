from os import environ

environ["DATABASE_URL"] = "sqlite:///:memory:"
environ["INITIAL_DATASET_PATH"] = "Movielist.csv"
environ["CSV_DELIMITER"] = ";"

from src.api import app

if __name__ == "__main__":
    app.run()
