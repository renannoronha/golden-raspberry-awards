class AwardsModel():

    def get_longest_fastest_consecutive_awards(self):
        query = f"""
            SELECT
                *
            FROM
                awards
        """
        return query