"""
This module contains the schema to define and
validate the Episode data structure.
"""
from datetime import date
from pydantic import BaseModel, field_validator
from typing import Optional


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
    anime_id: int
    arc: Optional[str] = None
    temp: int
    name: str
    episode: int
    air_date: date


    # Sanitize Functions
    @field_validator('arc', 'name', mode = 'before')
    def sanitize_string(cls, v):
        """
        Sanitizes string fields by stripping whitespace
        and converting to lowercase.

        Args:
            v (str): The string value to sanitize.

        Returns:
            str: The sanitized string.
        """
        if v is None:
            return v

        v = cls.remove_extra_spaces(v)
        v = cls.convert_to_lowercase(v)

        return v

    # Functions to sanitize data
    @staticmethod
    def remove_extra_spaces(value: str) -> str:
        """
        Removes extra spaces between words.

        Args:
            value (str): The string value to process.

        Returns:
            str: The string with extra spaces removed.
        """
        return ' '.join(value.split())


    @staticmethod
    def convert_to_lowercase(value: str) -> str:
        """
        Converts the string to lowercase.

        Args:
            value (str): The string value to process.

        Returns:
            str: The string converted to lowercase.
        """
        return value.lower()


    class Config:
        """
        Configuration class for Pydantic model.
        
        Attributes:
            from_attributes (bool): Indicates if the model
            should be populated from attributes.
        """
        from_attributes = True


class EpisodeAuthorRelationSchema(BaseModel):
    """
    Represents the schema for the creation of a relationship
    between an episode and an author.

    Attributes:
        episode_id (int): The ID of the episode.
        author_id (int): The ID of the author.
    """

    # Attributes
    episode_id: int
    author_id: int