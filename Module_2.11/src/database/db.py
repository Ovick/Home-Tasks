from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists

SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:567234@localhost:5432/rest_app"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def validate_database():
    if not database_exists(engine.url):
        create_database(engine.url)

# Dependency


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
