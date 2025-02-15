"""
This module contains the schema to define and validate the consult
the coincidence of a date with anime, episodes and authors.
"""

from typing import List

from pydantic import BaseModel

from app.schemas.anime_schema import AnimeSchemaResponse
from app.schemas.author_schema import AuthorSchema


class BirthdaySchemaResponse(BaseModel):
    """
    Schema for the response of a birthday match query.

    Attributes:
        anime (List[AnimeSchemaResponse]): List of anime that match the given date.
        author (List[AuthorSchema]): List of authors that match the given date.
        episode (int): Number of episodes that match the given date.
    """

    # Attributes
    anime: List[AnimeSchemaResponse]
    author: List[AuthorSchema]
    episode: int = 0
