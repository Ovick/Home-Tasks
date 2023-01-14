import sqlite3

DB_NAME = 'university.db'


def create_db():
    with open('db_definition.sql', 'r') as f:
        sql = f.read()

    with sqlite3.connect(DB_NAME) as con:
        cursor = con.cursor()
        cursor.executescript(sql)


if __name__ == "__main__":
    create_db()
