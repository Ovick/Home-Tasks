from sqlalchemy import create_engine, Column, Integer, String, DATE, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

DB_NAME = 'sqlite:///university.db'

Base = declarative_base()


class Faculty(Base):
    __tablename__ = 'faculty'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)


class Student(Base):
    __tablename__ = 'student'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    faculty_id = Column(Integer, ForeignKey(
        'faculty.id', onupdate='CASCADE', ondelete='SET NULL'))
    faculty = relationship(Faculty)


class Teacher(Base):
    __tablename__ = 'teacher'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)


class Discipline(Base):
    __tablename__ = 'discipline'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    teacher_id = Column(Integer, ForeignKey(
        'teacher.id', onupdate='CASCADE', ondelete='SET NULL'))
    teacher = relationship(Teacher)


class Mark(Base):
    __tablename__ = 'mark'
    mark_value = Column(Integer, nullable=False)
    mark_date = Column(DATE, nullable=False)
    student_id = Column(
        Integer, ForeignKey('student.id', ondelete='CASCADE'))
    student = relationship(Student)
    discipline_id = Column(
        Integer, ForeignKey('discipline.id', ondelete='NO ACTION'))
    discipline = relationship(Discipline)
    __table_args__ = (PrimaryKeyConstraint(
        'student_id', 'discipline_id', 'mark_date', name='mark_pk'), {})
