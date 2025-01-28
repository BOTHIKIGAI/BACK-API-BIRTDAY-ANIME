"""
This module contains the validation for the author.
"""
from datetime import datetime
from fastapi import Depends, HTTPException
from app.schemas.author_schema import AuthorSchema
from app.repositories.author_repository import AuthorRepository

class AuthorValidator:
    """
    Validator class for validating Author data.

    This class provides methods to validate the Author data,
    including checking if an author exists by ID, validating
    the author name, and validating the birthday date.

    Attributes:
        author_repository (AuthorRepository): The repository used for
        accessing Author data.
    """


    # Constructor
    def __init__(self, author_repository: AuthorRepository = Depends()) -> None:
        """
        Initializes the AuthorValidator with a repository
        for accessing author data.

        Args:
            author_repository (AuthorRepository): The repository
            used for accessing author data.
        """
        self.author_repository = author_repository


    # High Level Functions
    def validate_author(self, author_body: AuthorSchema):
        """
        Validates the given author data.

        Args:
            author_body (AuthorSchema): The author data to validate.

        Returns:
            bool: True if the author data is valid, False otherwise.
        """
        self.validate_name(author_body.name)
        self.validate_birthday_date(author_body.birthday)


    # Low Level Functions
    def author_exists(self, author_id: int) -> bool:
        """
        Checks if an author with the given ID exists in the repository.
        
        Args:
            author_id (int): The ID of the author to check.
        
        Returns:
            bool: True if the author exists, False otherwise.
        """
        if self.author_repository.exists(author_id):
            raise HTTPException(status_code = 404,
                                detail = 'The author does not exist.')


    def validate_name(self, author_name: str):
        """
        Validates if the given author name already exists.

        Args:
            author_name (str): The name of the author to validate.

        Raises:
            HTTPException: If the author name already exists (status code 409).

        Returns:
            bool: True if the name is valid, False otherwise.
        """
        if self.author_repository.name_exists(author_name):
            raise HTTPException(status_code = 409,
                                detail = "There is an auhor with that name")


    def validate_birthday_date(self, birthday_date: str):
        """
        Validates if the given birthday date is not in the future.

        Args:
            release_date (str): The birthday date to validate in format '%Y-%m-%d'.

        Raises:
            HTTPException: If the birthday date is in the future (status code 409).

        Returns:
            bool: True if the  birthday date is valid, False otherwise.
        """
        current_date = datetime.now().date()
        if birthday_date > current_date:
            raise HTTPException(status_code=409,
                                detail="The birthday date should not be in the future.")
