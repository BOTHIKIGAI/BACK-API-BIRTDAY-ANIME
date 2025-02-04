"""
This module contains the modul of the Episode table.
"""
from sqlalchemy import Column, BigInteger, String, Integer, Date, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.config.database import Base
from app.models.relationships.episode_author_association import episode_author_association

class Episode(Base):
    """
    Represents the Episode table in the database.

    Attributes:
        id (int): The primary key of the episode.
        anime_id (int): The anime ID of the episode.
        arc (str): The name of the arc.
        temp (int): The number of the temp.
        episode (int): The number of the episode.
        air_date (date): The air date of the episode.
        created_at (datetime): The date of creation of the registry.
        updated_at (datetime): The date of update of the registry.
    """
    __tablename__ = 'episode'

    # Columns
    id = Column(BigInteger, primary_key = True, index = True, nullable = False)
    anime_id = Column(BigInteger, ForeignKey('anime.id'), nullable = False)
    arc = Column(String, index = True, nullable = True)
    season = Column(Integer, index = True, nullable = False)
    name = Column(String, index = True, nullable = False)
    episode = Column(Integer, index = True, nullable = False)
    air_date = Column(Date, index = True, nullable = False)
    created_at = Column(DateTime(timezone = True), server_default = func.now(), nullable = False)
    updated_at = Column(DateTime(timezone = True), onupdate = func.now())

    # Relationships
    authors = relationship("Author",
                           secondary = episode_author_association,
                           back_populates = "episodes")

    anime = relationship("Anime",
                         back_populates = "episodes")
