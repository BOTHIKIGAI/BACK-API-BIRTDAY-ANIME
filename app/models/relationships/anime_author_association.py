"""
This module contains the intermediate table for the 
many-to-many relationship between anime and author.
"""

from sqlalchemy import (
    Table, Column, BigInteger,
    ForeignKey, DateTime)
from sqlalchemy.sql import func
from app.config.database import Base

anime_author_association = Table(
    'anime_author_association', Base.metadata,
    Column('anime_id', BigInteger, ForeignKey('anime.id'),
           primary_key=True),
    Column('author_id', BigInteger, ForeignKey('author.id'),
           primary_key=True),
    Column('created_at', DateTime(timezone=True),
           server_default=func.now(),nullable=False),
    Column('updated_at', DateTime(timezone=True),
           onupdate=func.now()))
