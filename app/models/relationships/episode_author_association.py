"""
This module contains the model with the intermediate table
for the many-to-many relationship between episode and author
"""

from sqlalchemy import (
    Table, Column, BigInteger,
    ForeignKey, DateTime)
from sqlalchemy.sql import func
from app.config.database import Base

episode_author_association = Table(
    'episode_author_association', Base.metadata,
    Column('episode_id', BigInteger, ForeignKey('episode.id'), primary_key=True),
    Column('author_id', BigInteger, ForeignKey('author.id'), primary_key=True),
    Column('created_at', DateTime(timezone=True), server_default=func.now(), nullable=False),
    Column('updated_at', DateTime(timezone=True), onupdate=func.now()))
