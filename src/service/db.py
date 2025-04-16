from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy import text

from os import environ
import json

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
        self.connection = self.engine.connect()

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()

    def fetch_to_dict(self, query: str, obj: dict = {}) -> dict:
        try:
            cursor_reader = self.connection.execute(text(query), obj)
            return self.db_to_dict(cursor_reader.keys(), cursor_reader.fetchone())
        except Exception as e:
            self.rollback()
            raise e

    def execute(self, query: str, obj: dict = {}) -> dict:
        try:
            self.connection.execute(text(query), obj)
            return True
        except Exception as e:
            self.rollback()
            raise e

    def db_to_dict(self, db_fields, db_object) -> dict:
        try:
            result = {}
            for i, field in enumerate(db_fields):
                value = db_object[i]
                if '{"' == value[:2] or '[{' == value[:2]:
                    try:
                        value = json.loads(value)
                    except:
                        pass
                result[field] = value
            return result
        except:
            return dict()
