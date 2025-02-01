"""
This module contains the schema to define and
validate the Anime data structure.
"""
from datetime import date
from pydantic import BaseModel, field_validator


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


    # Sanitize Functions
    @field_validator('name', 'category', mode = 'before')
    def sanitize_string(cls, v):
        """
        Sanitizes string fields by stripping whitespace and converting to lowercase.

        Args:
            v (str): The string value to sanitize.

        Returns:
            str: The sanitized string.
        """
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
            from_attributes (bool): Indicates if the model should
            be populated from attributes.
        """
        from_attributes = True
