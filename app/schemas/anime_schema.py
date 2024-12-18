"""
This module contains the schema to define and
validate the Anime data structure.
"""

from datetime import date
from pydantic import BaseModel

class AnimeSchema(BaseModel):
    """
    Represents the schema for the validation of
    the Anime object data.

    Attributes:
        name (str): The name of the anime.
        category (str): The category of the anime.
        release_date (date): The release date of the anime.
    """

    # Attributes
    name: str
    category: str
    release_date: date
