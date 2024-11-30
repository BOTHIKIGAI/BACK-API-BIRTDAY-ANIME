"""
This module contains the connection and configuration to the database.
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

DATABASE_URL = f"postgresql://{os.getenv('username_db')}:{os.getenv('password_db')}@localhost:5432/happy_birthday_anime_db"

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
