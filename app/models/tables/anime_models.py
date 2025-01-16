"""
This module contains the model of the Anime table.
"""

from sqlalchemy import Column, BigInteger, String, Date
from sqlalchemy.orm import relationship
from app.config.database import Base
from app.models.relationships.anime_author_association import anime_author_association

class Anime(Base):
    """
    Represents the Anime table in the database.

    Attributes:
        id (int): The primary key of the anime.
        name (str): The name of the anime.
        category (str): The category of the anime.
        release_date (date): The release date of the anime.
    """
    __tablename__ = 'anime'

    # Columns
    id = Column(BigInteger, primary_key=True, index=True, nullable=False)
    name = Column(String, index=True, nullable=False)
    category = Column(String, index=True, nullable=False)
    release_date = Column(Date, index=True, nullable=False)

    # Relationships
    authors = relationship(
        "Author",
        secondary=anime_author_association,
        back_populates="animes")

    episodes = relationship(
        "Episode",
        back_populates="anime")
