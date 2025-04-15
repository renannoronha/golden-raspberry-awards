from src.model.awards import AwardsModel

from src.service.db import DB


class ActionCore:

    def __init__(self, *args, **kwargs):
        self.db = DB()
        self.model = AwardsModel()

    def get_longest_fastest_consecutive_awards(self):
        awards = self.db.fetch_to_dict(self.model.get_longest_fastest_consecutive_awards())
        return 200, awards
