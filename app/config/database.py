"""
This module contains the connection and configuration to the database.
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

# load env variable
load_dotenv()

DATABASE_MOTOR = os.getenv('database_motor')
USERNAME_DB = os.getenv('username_db')
PASSWORD_DB = os.getenv('password_db')
HOST_PORT = os.getenv('host_port')
NAME_DB = os.getenv('name_database')

DATABASE_URL = f"{DATABASE_MOTOR}://{USERNAME_DB}:{PASSWORD_DB}@{HOST_PORT}/{NAME_DB}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db_connection():
    """
    Provides a scoped session for database connection.

    Yields:
        db (Session): A SQLAlchemy scoped session.
    """
    db = scoped_session(SessionLocal)
    try:
        yield db
    finally:
        db.close()
