from os import environ, path
import pytest

environ["DATABASE_URL"] = "sqlite:///:memory:"
environ["INITIAL_DATASET_PATH"] = path.dirname(path.abspath(__file__)) + "/Movielist.csv"
environ["CSV_DELIMITER"] = ";"

from src.api import app


@pytest.fixture()
def application():
    yield app


@pytest.fixture()
def client(application):
    application.config.update({
        "TESTING": True,
    })
    return application.test_client()


@pytest.fixture()
def config(application):
    application.config.update({
        "TESTING": True,
    })
    return application.config
