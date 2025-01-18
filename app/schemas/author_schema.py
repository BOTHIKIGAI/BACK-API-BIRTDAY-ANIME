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
        from_attributes = True
