"""
This module contains the intermediate table for the 
many-to-many relationship between anime and author.
"""

from sqlalchemy import Table, Column, BigInteger, ForeignKey
from app.config.database import Base

anime_author_association = Table(
    'anime_author_association', Base.metadata,
    Column('anime_id', BigInteger, ForeignKey('anime.id'), primary_key=True),
    Column('author_id', BigInteger, ForeignKey('author.id'), primary_key=True)
)
