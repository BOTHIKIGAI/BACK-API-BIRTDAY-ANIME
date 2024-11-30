"""
This module contains the model with the intermediate table
for the many-to-many relationship between episode and author
"""

from sqlalchemy import Table, Column, BigInteger, ForeignKey
from app.config.database import Base

episode_author_association = Table(
    'episode_author_association', Base.metadata,
    Column('episode_id', BigInteger, ForeignKey('episode.id'), primary_key=True),
    Column('author_id', BigInteger, ForeignKey('author.id'), primary_key=True)
)
