from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool

from os import environ


class SingletonMeta(type):

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class DB(metaclass=SingletonMeta):

    def __init__(self):
        self.engine = create_engine(environ.get("DATABASE_URL"), connect_args={"check_same_thread": False}, poolclass=StaticPool, echo=False)

    def connect(self):
        """
        Connect to the database
        """
        return self.engine.connect()
