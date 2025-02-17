"""
This module contains the schema to define and validate the Author data structure.
"""
from datetime import date

from pydantic import BaseModel, field_validator

from app.utils.sanatizers.common_sanatizers_str import (
    convert_to_lowercase,
    remove_extra_spaces,
)
from app.utils.validations.common_validations_date import (
    create_date,
    validate_date_format,
    validate_date_no_less_minimum,
    validate_date_not_in_the_future,
)
from app.utils.validations.common_validations_str import validate_is_instance_str


class AuthorSchemaResponse(BaseModel):
    name: str
    alias: str
    birthday: date


class AuthorSchemaCreate(BaseModel):
    name: str
    alias: str = ""
    birthday: date


    # Validate data
    @field_validator('name', 'alias', mode="before")
    def validate_str(cls, attribute: str) -> str:
        """
        Validate if the attribute is a string.

        Args:
            attribute (str): The string to validate.

        Returns:
            str: The validated string.

        Raises:
            ValueError: If the attribute is not a string.
        """
        validate_is_instance_str(attribute)
        return attribute


    @field_validator('birthday', mode="before")
    def validate_date(cls, attribute: str) -> date:
        """
        Validate the release date format and constraints.

        Args:
            attribute (str): The date string to validate.

        Returns:
            date: The validated date object.

        Raises:
            ValueError: If the date format is invalid or constraints are not met.
        """
        validate_is_instance_str(attribute)
        validate_date_format(attribute)
        attribute_date = create_date(attribute)
        validate_date_not_in_the_future(attribute_date)
        min_date = date(1877, 11, 4)
        validate_date_no_less_minimum(
            value=attribute_date,
            min_date=min_date
        )
        return attribute_date


    # Data sanitization
    @field_validator('name', 'alias', mode="after")
    def sanatizar_str(cls, attribute: str) -> str:
        """
        Sanitize string attributes by removing extra spaces and converting to lowercase.

        Args:
            attribute (str): The string to sanitize.

        Returns:
            str: The sanitized string.
        """
        attribute = remove_extra_spaces(attribute)
        attribute = convert_to_lowercase(attribute)
        return attribute


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
