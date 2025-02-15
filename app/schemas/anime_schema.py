"""
This module contains the schema to define and validate the Anime data structure.
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


class AnimeSchemaResponse(BaseModel):
    # Attributes
    name: str
    category: str
    release_date: date

    # Configuration
    model_config = {
        "from_attributes": True
    }


class AnimeSchemaCreate(BaseModel):


    # Attributes
    name: str = ""
    category: str = ""
    release_date: date


    # Validate data
    @field_validator('name', 'category', mode="before")
    def validate_str(cls, attribute: str) -> str:
        validate_is_instance_str(attribute)
        return attribute


    @field_validator('release_date', mode="before")
    def validate_date(cls, attribute: str) -> date:
        validate_date_format(attribute)
        attribute_date = create_date(attribute)
        validate_date_not_in_the_future(attribute_date)
        min_date = date(1907, 1, 1)
        validate_date_no_less_minimum(
            value=attribute_date,
            min_date=min_date
        )
        return attribute_date


    # Data sanitization
    @field_validator('name', 'category', mode="after")
    def sanatizar_str(cls, attribute: str) -> str:
        attribute = remove_extra_spaces(attribute)
        attribute = convert_to_lowercase(attribute)
        return attribute
