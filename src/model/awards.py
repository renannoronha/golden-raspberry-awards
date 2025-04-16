class AwardsModel():

    def get_longest_fastest_consecutive_awards(self):
        query = f"""
            WITH difference AS (
                SELECT
                    *,
                    (SELECT year FROM awards WHERE winner='yes' AND producers=a.producers AND year>a.year ORDER BY year LIMIT 1) AS next_win,
                    (SELECT year FROM awards WHERE winner='yes' AND producers=a.producers AND year>a.year ORDER BY year LIMIT 1)-year AS interval
                FROM
                    awards a
                WHERE
                    winner='yes'
                ORDER BY year
            ), max AS (
                SELECT
                    JSON_GROUP_ARRAY(
                        JSON_OBJECT(
                            'producer', producers,
                            'interval', interval,
                            'previousWin', year,
                            'followingWin', next_win
                        )
                    ) AS max
                FROM
                    difference
                WHERE
                    interval=(SELECT MAX(interval) FROM difference)
            ), min AS (
                SELECT
                    JSON_GROUP_ARRAY(
                        JSON_OBJECT(
                            'producer', producers,
                            'interval', interval,
                            'previousWin', year,
                            'followingWin', next_win
                        )
                    ) AS min
                FROM
                    difference
                WHERE
                    interval=(SELECT MIN(interval) FROM difference)
            )
            SELECT
                min.min,
                max.max
            FROM
                min,
                max
        """
        return query
