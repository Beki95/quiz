from contextlib import contextmanager

from databases import Database
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from core.config import DATABASE_URL

database = Database(DATABASE_URL)

engine = create_engine(
    DATABASE_URL,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@contextmanager
def get_context_db():
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

