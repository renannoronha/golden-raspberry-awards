from os import environ, path
import pytest

environ["DATABASE_URL"] = "sqlite:///:memory:"
environ["INITIAL_DATASET_PATH"] = path.dirname(path.abspath(__file__)) + "/Movielist.csv"
environ["CSV_DELIMITER"] = ";"

from src.api import app


class Middleware:

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        environ.update({"custom:provider_id": 1})
        environ.update({"custom:_id": 1})
        environ.update({"email": "marcos.agnes@eemovel.com"})
        return self.app(environ, start_response)


@pytest.fixture()
def application():
    app.wsgi_app = Middleware(app.wsgi_app)
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
