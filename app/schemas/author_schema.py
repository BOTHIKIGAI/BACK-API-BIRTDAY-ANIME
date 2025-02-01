"""
This module contains the schema to define and
validate the Author data structure.
"""
from datetime import date
from pydantic import BaseModel, field_validator
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


    # Sanitize Functions
    @field_validator('name', 'alias', mode = 'before')
    def sanitize_string(cls, v):
        """
        Sanitizes string fields by stripping whitespace and converting to lowercase.

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
