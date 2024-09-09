import sqlite3
from tgbot.files.config import db_path

# database = sqlite3.connect(db_path)
# cursor = database.cursor()


class SQLite:
    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def register_user(self, user_id, user_number):
        with self.connection:
            self.connection.execute("""INSERT INTO users (user_id, user_number) VALUES
            (?, ?)""",
                                    [user_id, user_number])

    def select_user_info(self, user_id):
        with self.connection:
            self.cursor.execute(
                """SELECT user_id, number FROM users WHERE user_id == ? """,
                [user_id])
            row = self.cursor.fetchall()

            return row[0]

    def is_registered(self, user_id):
        with self.connection:
            self.cursor.execute("""SELECT user_id FROM users WHERE user_id == ? """, [user_id])
            rows = self.cursor.fetchall()

            return rows


    def select_phone(self, user_id):
        with self.connection:
            self.cursor.execute("""SELECT number FROM users WHERE user_id = ? """, [user_id])
            rows = self.cursor.fetchall()

            return rows[0][0]




# cursor.execute("""CREATE TABLE users (
#            id            int      primary key,
#            user_id       int      not null,
#            full_name     text     not null,
#            user_name     text     not null,
#            lang          int      not null)
#            """)

""" 
    lang == int: 0 => uz; 1 => ru; 2 => en
"""
