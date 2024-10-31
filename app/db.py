'''database connection and session management'''

from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings

SQLALCHEMY_DATABASE_URL = f"mysql+mysqlconnector://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# db session life cycle management
@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
        db.commit() # auto commit
    except Exception as e:
        db.rollback() # auto rollback if error
        print(f"Database session error: {e}")
    finally:
        db.close() # auto cleanup