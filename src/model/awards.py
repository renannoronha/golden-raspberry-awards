class AwardsModel():

    def get_longest_consecutive_awards(self):
        query = f"""
            WITH difference AS (
                SELECT
                    *,
                    (SELECT year FROM awards WHERE winner='yes' AND producers=a.producers AND year>a.year ORDER BY year LIMIT 1) AS next_win,
                    (SELECT year FROM awards WHERE winner='yes' AND producers=a.producers AND year>a.year ORDER BY year LIMIT 1)-year AS next_win_year_difference
                FROM
                    awards a
                WHERE
                    winner='yes'
                ORDER BY year
            )
            SELECT
                producers AS producer,
                next_win_year_difference AS 'interval',
                year AS previousWin,
                next_win AS followingWin
            FROM
                difference
            WHERE
                "interval" IS NOT NULL AND "interval"=(SELECT MAX(next_win_year_difference) FROM difference)
        """
        return query

    def get_fastest_consecutive_awards(self):
        query = f"""
            WITH difference AS (
                SELECT
                    *,
                    (SELECT year FROM awards WHERE winner='yes' AND producers=a.producers AND year>a.year ORDER BY year LIMIT 1) AS next_win,
                    (SELECT year FROM awards WHERE winner='yes' AND producers=a.producers AND year>a.year ORDER BY year LIMIT 1)-year AS next_win_year_difference
                FROM
                    awards a
                WHERE
                    winner='yes'
                ORDER BY year
            )
            SELECT
                producers AS producer,
                next_win_year_difference AS 'interval',
                year AS previousWin,
                next_win AS followingWin
            FROM
                difference
            WHERE
                "interval" IS NOT NULL AND "interval"=(SELECT MIN(next_win_year_difference) FROM difference)
        """
        return query
