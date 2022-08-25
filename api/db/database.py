import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session


postgres_user = os.getenv("POSTGRES_USER", 'postgres')
postgres_db = os.getenv("POSTGRES_DB", 'real_estate')
postgres_password = os.getenv("POSTGRES_PASSWORD", 'password')
postgres_host = os.getenv("POSTGRES_HOST", 'db')

SQLALCHEMY_DATABASE_URL = f"postgresql://{postgres_user}:{postgres_password}@{postgres_host}/{postgres_db}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
