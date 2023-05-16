from sqlalchemy import create_engine, select, func, desc
from sqlalchemy.orm import sessionmaker, aliased
from db_model import DB_NAME, Faculty, Student, Teacher, Discipline, Mark


def select_1():
    engine = create_engine(DB_NAME)
    DBSession = sessionmaker(bind=engine)
    with DBSession() as session:
        return session.execute(
            select(Student.name, func.round(
                func.avg(Mark.mark_value), 1).label("Average_mark"))
            .join(Student)
            .group_by(Student.name)
            .order_by(desc("Average_mark"))
            .limit(5)
        ).mappings().all()


def select_2():
    engine = create_engine(DB_NAME)
    DBSession = sessionmaker(bind=engine)
    with DBSession() as session:
        subquery = session.query(select(Discipline.name).limit(1).subquery())
        return session.execute(
            select(Discipline.name.label("Discipline"), Student.name.label(
                "Student"), func.round(func.avg(Mark.mark_value), 1).label("Average_mark"))
            .join(Student)
            .join(Discipline)
            .filter(Discipline.name.in_(subquery))
            .group_by(Student.name)
            .order_by(desc("Average_mark"))
            .limit(1)
        ).mappings().all()


def select_3():
    engine = create_engine(DB_NAME)
    DBSession = sessionmaker(bind=engine)
    with DBSession() as session:
        subquery = session.query(select(Discipline.name).limit(1).subquery())
        return session.execute(
            select(Discipline.name.label("Discipline"), Faculty.name.label(
                "Faculty"), func.round(func.avg(Mark.mark_value), 1).label("Average_mark"))
            .select_from(Mark)
            .join(Student)
            .join(Faculty)
            .join(Discipline)
            .filter(Discipline.name.in_(subquery))
            .group_by(Faculty.name)
            .order_by(desc("Average_mark"))
        ).mappings().all()


def select_4():
    engine = create_engine(DB_NAME)
    DBSession = sessionmaker(bind=engine)
    with DBSession() as session:
        return session.execute(
            select(func.round(func.avg(Mark.mark_value), 1).label("Average_mark"))
        ).mappings().all()


def select_5():
    engine = create_engine(DB_NAME)
    DBSession = sessionmaker(bind=engine)
    with DBSession() as session:
        return session.execute(
            select(Teacher.name.label("Teacher"),
                   Discipline.name.label("Discipline"))
            .join(Discipline)
            .order_by(Teacher.name, Discipline.name)
        ).mappings().all()


def select_6():
    engine = create_engine(DB_NAME)
    DBSession = sessionmaker(bind=engine)
    with DBSession() as session:
        return session.execute(
            select(Faculty.name.label("Faculty"),
                   Student.name.label("Student"))
            .join(Student)
            .order_by(Faculty.name, Student.name)
        ).mappings().all()


def select_7():
    engine = create_engine(DB_NAME)
    DBSession = sessionmaker(bind=engine)
    with DBSession() as session:
        subquery_faculty = session.query(
            select(Faculty.name).limit(1).subquery())
        subquery_discipline = session.query(
            select(Discipline.name).limit(1).subquery())
        return session.execute(
            select(Discipline.name.label("Discipline"), Faculty.name.label(
                "Faculty"), Student.name.label("Student"), Mark.mark_date, Mark.mark_value)
            .select_from(Mark)
            .join(Student)
            .join(Faculty)
            .join(Discipline)
            .filter(Discipline.name.in_(subquery_discipline))
            .filter(Faculty.name.in_(subquery_faculty))
            .order_by(Student.name, desc(Mark.mark_date))
        ).mappings().all()


def select_8():
    engine = create_engine(DB_NAME)
    DBSession = sessionmaker(bind=engine)
    with DBSession() as session:
        subquery = session.query(select(Teacher.name).limit(1).subquery())
        return session.execute(
            select(Discipline.name.label("Discipline"), Teacher.name.label(
                "Teacher"), func.round(func.avg(Mark.mark_value), 1).label("Average_mark"))
            .select_from(Mark)
            .join(Discipline)
            .join(Teacher)
            .filter(Teacher.name.in_(subquery))
            .group_by(Teacher.name, Discipline.name)
        ).mappings().all()


def select_9():
    engine = create_engine(DB_NAME)
    DBSession = sessionmaker(bind=engine)
    with DBSession() as session:
        subquery = session.query(select(Student.name).limit(1).subquery())
        return session.execute(
            select(Discipline.name.label("Discipline"),
                   Student.name.label("Student"))
            .select_from(Mark)
            .join(Student)
            .join(Discipline)
            .filter(Student.name.in_(subquery))
            .distinct()
        ).mappings().all()


def select_10():
    engine = create_engine(DB_NAME)
    DBSession = sessionmaker(bind=engine)
    with DBSession() as session:
        subquery_student = session.query(
            select(Student.name).limit(1).subquery())
        subquery_teacher = session.query(
            select(Teacher.name).limit(1).subquery())
        return session.execute(
            select(Discipline.name.label("Discipline"),
                   Student.name.label("Student"),
                   Teacher.name.label("Teacher"))
            .select_from(Mark)
            .join(Student)
            .join(Discipline)
            .join(Teacher)
            .filter(Student.name.in_(subquery_student))
            .filter(Teacher.name.in_(subquery_teacher))
            .distinct()
        ).mappings().all()


def select_11():
    engine = create_engine(DB_NAME)
    DBSession = sessionmaker(bind=engine)
    with DBSession() as session:
        subquery_student = session.query(
            select(Student.name).limit(1).subquery())
        subquery_teacher = session.query(
            select(Teacher.name).limit(1).subquery())
        return session.execute(
            select(Student.name.label("Student"),
                   Teacher.name.label("Teacher"),
                   func.round(func.avg(Mark.mark_value), 1).label("Average_mark"))
            .select_from(Mark)
            .join(Student)
            .join(Discipline)
            .join(Teacher)
            .filter(Student.name.in_(subquery_student))
            .filter(Teacher.name.in_(subquery_teacher))
            .group_by(Teacher.name, Student.name)
        ).mappings().all()
