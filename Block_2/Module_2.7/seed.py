from datetime import datetime
import faker
from random import randint
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_model import DB_NAME, Faculty, Student, Teacher, Discipline, Mark

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

    engine = create_engine(DB_NAME)
    DBSession = sessionmaker(bind=engine)

    with DBSession() as session:

        for faculty in faculties:
            new_faculty = Faculty(name=faculty[0])
            session.add(new_faculty)

        for teacher in teachers:
            new_teacher = Teacher(name=teacher[0])
            session.add(new_teacher)

        for discipline in disciplines:
            new_discipline = Discipline(
                name=discipline[0], teacher_id=discipline[1])
            session.add(new_discipline)

        for student in students:
            new_student = Student(name=student[0], faculty_id=student[1])
            session.add(new_student)

        for mark in marks:
            new_mark = Mark(
                mark_value=mark[0],
                mark_date=mark[1],
                student_id=mark[2],
                discipline_id=mark[3]
            )
            session.add(new_mark)

        session.commit()


if __name__ == "__main__":
    faculties, students, teachers, disciplines, marks = prepare_data(
        *generate_fake_data(NUMBER_FACULTIES, NUMBER_STUDENTS, NUMBER_DISCIPLINES, NUMBER_TEACHERS))
    insert_data_to_db(faculties, students, teachers, disciplines, marks)
