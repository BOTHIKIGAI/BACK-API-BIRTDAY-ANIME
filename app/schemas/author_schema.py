"""
This module contains the schema to define and
validate the Author data structure.
"""

from datetime import datetime
from pydantic import BaseModel

class Author(BaseModel):
    """
    Represents the schema for the validation of
    the Author object data.

    Attributes:
        name (str): The name of the author.
        alias (str): The alias of the author.
        birthday (date): The birthday of the author.
    """

    # Attributes
    name: str
    alias: str
    birthday: datetime
