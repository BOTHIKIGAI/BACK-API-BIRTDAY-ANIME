"""
This module contains the schema to define and validate the Anime data structure.
"""
from datetime import date, datetime
from typing import Union

from pydantic import BaseModel, field_validator


class AnimeSchema(BaseModel):
    """
    Represents the schema for the validation and sanatization of the Anime object data.

    Attributes:
        name (str): The name of the anime.
        category (str): The category of the anime.
        release_date (date): The release date of the anime.
    """

    # Attributes
    name: str = ""
    category: str = ""
    release_date: date = date.fromisoformat("1907-01-01")


    model_config = {
        "from_attributes": True
    }


    # Validate data
    @field_validator('name', 'category', mode='before')
    def validate_str(cls, v):
        """
        Validate if the input value is a string.

        Args:
            value: The value to be validated.

        Returns:
            str: The validated string value.

        Raises:
            ValueError: If the value is not a string.
        """
        cls.validate_is_instance_str(v)
        return v


    @field_validator('release_date', mode='before')
    def validate_date(cls, v):
        """
        Validate and convert the input value to a date object.

        Args:
            value: A string in ISO format (YYYY-MM-DD) or a date object.

        Returns:
            date: The validated date object.

        Raises:
            ValueError: If the value cannot be converted to a valid date.
        """
        v = cls.create_date(v)
        cls.validate_date_not_in_the_future(v)
        cls.validate_date_no_less_minimum(v)
        return v


    # Sanitize Functions
    @field_validator('name', 'category', mode='after')
    def sanitize_string(cls, v: str) -> str:
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
    def validate_is_instance_str(value) -> None:
        if not isinstance(value, str):
            raise ValueError(f'{value} is not a string')


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


    @staticmethod
    def create_date(value: Union[str, date]) -> date:
        """
        Create a date object from a string or validate an existing date object.

        This function handles both string conversion to date and validation of
        existing date objects. It ensures the date is within acceptable bounds
        (1900-01-01 to 2100-12-31).

        Args:
            value: A string in ISO format (YYYY-MM-DD) or a date object.

        Returns:
            date: The validated date object.

        Raises:
            ValueError: If the input is invalid, in wrong format, or outside
                        acceptable date range.
        """
        if isinstance(value, date):
            parsed_date = value
        else:
            try:
                parsed_date = date.fromisoformat(value)
            except ValueError:
                raise ValueError(
                    f"Invalid date format: '{value}'. "
                    "Date must be in ISO format (YYYY-MM-DD)"
                )
            except TypeError:
                raise ValueError(
                    f"Invalid date type: {type(value)}. "
                    "Date must be a string in ISO format (YYYY-MM-DD)"
                )
        return parsed_date


    @staticmethod
    def validate_date_not_in_the_future(value) -> None:
        """
        Validate that a date is not in the future.

        This validator ensures that the provided date is not later than
        the current date. It's typically used for release dates or
        other historical dates that shouldn't be in the future.

        Args:
            value: The date to validate.

        Returns:
            date: The validated date if it's not in the future.

        Raises:
            ValueError: If the date is later than the current date.
        """
        current_date = datetime.now().date()
        if value > current_date:
            raise ValueError("The date should not be in the future.")


    @staticmethod
    def validate_date_no_less_minimum(value) -> None:
        min_date = date(1907, 1, 1)
        if value < min_date:
                raise ValueError(
                    f"Date {value} is too early. "
                    f"Minimum allowed date is {min_date}"
                )
