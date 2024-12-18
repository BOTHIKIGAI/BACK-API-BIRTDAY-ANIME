"""
This module contains the schema to define and
validate the Episode data structure.
"""

from datetime import date
from pydantic import BaseModel

class EpisodeSchema(BaseModel):
    """
    Represents the schema for the validation of
    the Episode object data.

    Attributes:
        arc (str): The name of the arc.
        temp (int): The number of the temp.
        episode (int): The number of the episode.
        air_date (date): The air date of the episode.
    """

    # Attributes
    arc: str
    temp: int
    episode: int
    air_date: date
