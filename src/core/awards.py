from sqlalchemy import text
from src.model.awards import AwardsModel

from src.service.db import DB


class AwardsCore:

    def __init__(self, *args, **kwargs):
        self.db = DB()
        self.model = AwardsModel()

    def get_longest_fastest_consecutive_awards(self):
        response = {}
        with self.db.connect() as conn:
            cursor_result = conn.execute(text(self.model.get_longest_consecutive_awards()))
            longest_consecutive_awards = cursor_result.fetchall()
            response["max"] = []
            for obj in longest_consecutive_awards:
                response["max"].append(dict(producer=obj[0], interval=obj[1], previousWin=obj[2], followingWin=obj[3]))

            cursor_result = conn.execute(text(self.model.get_fastest_consecutive_awards()))
            fastest_consecutive_awards = cursor_result.fetchall()
            response["min"] = []
            for obj in fastest_consecutive_awards:
                response["min"].append(dict(producer=obj[0], interval=obj[1], previousWin=obj[2], followingWin=obj[3]))

        return response, 200
