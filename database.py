import sqlite3


def add_score(name, score):
    with sqlite3.connect(('score.sqlite')) as db:

        cur = db.cursor()

        cur.execute("""
            create table if not exists RECORDS (
            name text, score integer)
        """)


        cur.execute("""INSERT INTO RECORDS (name, score) VALUES (?, ?)""",
                    (name, score))

        cur.execute("""
                SELECT name, max(score) score from RECORDS
                GROUP BY name
                ORDER BY score DESC
                limit 5
            """)
        result = cur.fetchall()

        return result