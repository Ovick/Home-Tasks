import sqlite3
from create_db import create_db, DB_NAME
from seed_db import prepare_data, generate_fake_data, insert_data_to_db, \
    NUMBER_FACULTIES, NUMBER_STUDENTS, NUMBER_DISCIPLINES, NUMBER_TEACHERS

if __name__ == "__main__":
    # recreate tables
    create_db()
    # seed random values
    faculties, students, teachers, disciplines, marks = prepare_data(
        *generate_fake_data(NUMBER_FACULTIES, NUMBER_STUDENTS, NUMBER_DISCIPLINES, NUMBER_TEACHERS))
    insert_data_to_db(faculties, students, teachers, disciplines, marks)
    # read a query
    with open('queries/query_10.sql', 'r') as f:
        sql = f.read()
    # execute the query
    with sqlite3.connect(DB_NAME) as con:
        cursor = con.cursor()
        cursor.execute(sql)
        for row in cursor.fetchall():
            print(row)
