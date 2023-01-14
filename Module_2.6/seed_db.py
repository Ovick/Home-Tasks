from datetime import datetime
import faker
from random import randint, choice
import sqlite3

NUMBER_FACULTIES = 3
NUMBER_STUDENTS = 50
NUMBER_DISCIPLINES = 8
NUMBER_TEACHERS = 5
NUMBER_MARKS = 20


def generate_fake_data(number_faculties, number_students, number_disciplines, number_teachers) -> tuple():

    fake_faculties = []
    fake_students = []
    fake_disciplines = []
    fake_teachers = []

    fake_data = faker.Faker()

    for _ in range(number_faculties):
        fake_faculties.append(fake_data.word())

    for _ in range(number_students):
        fake_students.append(fake_data.name())

    for _ in range(number_teachers):
        fake_teachers.append(fake_data.name())

    for _ in range(number_disciplines):
        fake_disciplines.append(fake_data.word())

    return fake_faculties, fake_students, fake_teachers, fake_disciplines


def prepare_data(faculties, students, teachers, disciplines) -> tuple():
    for_faculties = []
    for faculty in faculties:
        for_faculties.append((faculty, ))

    for_teachers = []
    for teacher in teachers:
        for_teachers.append((teacher, ))

    for_disciplines = []
    for discipline in disciplines:
        for_disciplines.append((discipline, randint(1, NUMBER_TEACHERS)))

    for_students = []
    for student in students:
        for_students.append((student, randint(1, NUMBER_FACULTIES)))

    for_marks = []
    for student in range(1, NUMBER_STUDENTS + 1):
        for discipline in range(1, NUMBER_DISCIPLINES + 1):
            for month in range(1, 12 + 1):
                mark_date = datetime(datetime.now().year,
                                     month, randint(5, 25)).date()
                for_marks.append(
                    (randint(1, 12), mark_date, student, discipline))

    return for_faculties, for_students, for_teachers, for_disciplines, for_marks


def insert_data_to_db(faculties, students, teachers, disciplines, marks) -> None:

    with sqlite3.connect('university.db') as con:

        cur = con.cursor()

        cur.execute('DELETE FROM faculty;')
        cur.execute('DELETE FROM student;')
        cur.execute('DELETE FROM teacher;')
        cur.execute('DELETE FROM discipline;')
        cur.execute('DELETE FROM mark;')

        sql_to_faculty = """INSERT INTO faculty(name)
                               VALUES (?)"""
        cur.executemany(sql_to_faculty, faculties)

        sql_to_teacher = """INSERT INTO teacher(name)
                               VALUES (?)"""
        cur.executemany(sql_to_teacher, teachers)

        sql_to_discipline = """INSERT INTO discipline(name, teacher_id)
                               VALUES (?, ?)"""
        cur.executemany(sql_to_discipline, disciplines)

        sql_to_student = """INSERT INTO student(name, faculty_id)
                               VALUES (?, ?)"""
        cur.executemany(sql_to_student, students)

        sql_to_mark = """INSERT INTO mark(mark_value, mark_date, student_id, discipline_id)
                              VALUES (?, ?, ?, ?)"""
        cur.executemany(sql_to_mark, marks)

        con.commit()


if __name__ == "__main__":
    faculties, students, teachers, disciplines, marks = prepare_data(
        *generate_fake_data(NUMBER_FACULTIES, NUMBER_STUDENTS, NUMBER_DISCIPLINES, NUMBER_TEACHERS))
    insert_data_to_db(faculties, students, teachers, disciplines, marks)
