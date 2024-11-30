"""
This module contains the model of the Author table.
"""

from sqlalchemy import Column, BigInteger, String, Date
from sqlalchemy.orm import relationship
from app.config.database import Base
from app.models.relationships.anime_author_association import anime_author_association
from app.models.relationships.episode_author_association import episode_author_association

class Author(Base):
    """
    Represents the Author table in the database.

    Attributes:
        id (int): The primary key of the author.
        name (str): The name of the author.
        alias (str): The alias of the author.
        birthday (date): The birthday of the author.
    """
    __tablename__ = 'author'

    # Columns
    id = Column(BigInteger, primary_key=True, index=True, nullable=False)
    name = Column(String, index=True, nullable=False)
    alias = Column(String, index=True, nullable=True)
    birthday = Column(Date, index=True, nullable=True)

    # Relationships
    animes = relationship(
        "Anime",
        secondary=anime_author_association,
        back_populates="authors"
    )

    episodes = relationship(
        "Episode",
        secondary=episode_author_association,
        back_populates="authors"
    )
