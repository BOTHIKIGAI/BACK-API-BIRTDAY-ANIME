"""
This module contains the modul of the Episode table.
"""

from sqlalchemy import Column, BigInteger, String, Integer, Date
from sqlalchemy.orm import relationship
from app.config.database import Base
from app.models.relationships.episode_author_association import episode_author_association

class Episode(Base):
    """
    Represents the Episode table in the database.

    Attributes:
        id (int): The primary key of the episode.
        arc (str): The name of the arc.
        temp (int): The number of the temp.
        episode (int): The number of the episode.
        air_date (date): The air date of the episode.
    """
    __tablename__ = 'episode'

    # Columns
    id = Column(BigInteger, primary_key=True, index=True, nullable=False)
    arc = Column(String, index=True, nullable=True)
    temp = Column(Integer, index=True, nullable=False)
    episode = Column(Integer, index=True, nullable=False)
    air_date = Column(Date, index=True, nullable=False)

    # Relationships
    authors = relationship(
        "Author",
        secondary=episode_author_association,
        back_populates="episodes"
    )
