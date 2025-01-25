"""
This module contains the schema to define and
validate the Author data structure.
"""
from datetime import date
from pydantic import BaseModel
from typing import Optional


class AuthorSchema(BaseModel):
    """
    Represents the schema for the validation of
    the Author object data.

    Attributes:
        name (str): The name of the author.
        alias (str): The alias of the author.
        birthday (date): The birthday of the author.
    """

    # Attributes
    name: Optional[str] = None
    alias: Optional[str] = None
    birthday: Optional[date] = None

    class Config:
        """
        Configuration class for Pydantic model.
        
        Attributes:
            from_attributes (bool): Indicates if the model
            should be populated from attributes.
        """
        from_attributes = True


class AuthorAnimeRelationSchema(BaseModel):
    """
    Represents the schema for the creation of a relationship
    between an author and an anime.

    Attributes:
        author_id (int): The ID of the author.
        anime_id (int): The ID of the anime.
    """

    # Attributes
    author_id: int
    anime_id: int
