import contextlib
import sqlite3


class DataManager:
    def __init__(self):
        with contextlib.ExitStack() as stack:
            self.db_connection = stack.enter_context(sqlite3.connect("snake_scores.db"))
            self.db_cursor = self.db_connection.cursor()
            self.db_cursor.execute(
                """
                    CREATE TABLE IF NOT EXISTS scores (
                        username TEXT,
                        score INTEGER,
                        difficult TEXT,
                        area INTEGER,
                        date TEXT
                    )
                """
            )
            self.db_cursor.execute(
                """
                    CREATE TABLE IF NOT EXISTS setting (
                        username TEXT,
                        difficult TEXT,
                        sound BOOLEN,
                        area INTEGER,
                        control TEXT
                    )
                """
            )

    def add_setting(self, username, difficult, sound, area, control):
        with self.db_connection:
            self.db_cursor.execute(
                "INSERT INTO setting VALUES (?, ?, ?, ?, ?)",
                (username, difficult, sound, area, control),
            )

    def save_score(self, username, score, difficult, area, date):
        self.db_cursor.execute(
            "INSERT INTO scores VALUES (?, ?, ?, ?, ?)",
            (username, score, difficult, area, date),
        )
        self.db_connection.commit()
