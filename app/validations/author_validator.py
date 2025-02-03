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
    def validate_data_for_get(self, author_id: int) -> None:
        """
        Validates the given author ID for retrieval.

        Args:
            author_id (int): The ID of the author to validate.

        Raises:
            HTTPException: If the author does not exist (status code 404).
        """
        self.validate_exists_by_id(author_id)


    def validate_data_for_create(self, author_body: AuthorSchema) -> None:
        """
        Validates the given author data for creation.

        Args:
            author_body (AuthorSchema): The author data to validate.

        Raises:
            HTTPException: If the author name already exists (status code 409).
            HTTPException: If the birthday date is in the future (status code 409).
        """
        self.validate_unique_name_for_create(author_body.name)
        self.validate_birthday_date_not_in_future(author_body.birthday)


    def validate_data_for_update(self, exclude_id: int, author_body: AuthorSchema) -> None:
        """
        Validates the given author data for update.

        Args:
            author_id (int): The ID of the author to validate.
            author_body (AuthorSchema): The author data to validate.

        Raises:
            HTTPException: If the author does not exist (status code 404).
            HTTPException: If the author name already exists (status code 409).
            HTTPException: If the birthday date is in the future (status code 409).
        """
        self.validate_aunique_name_for_update(exclude_id = exclude_id, author_name = author_body.name)
        self.validate_birthday_date_not_in_future(author_body.birthday)


    def validate_data_for_delete(self, author_id: int) -> None:
        """
        Validates the given author ID for deletion.

        Args:
            author_id (int): The ID of the author to validate.

        Raises:
            HTTPException: If the author does not exist (status code 404).
            HTTPException: If the author is related to any anime (status code 409).
            HTTPException: If the author is related to any episode (status code 409).
        """
        self.validate_exists_by_id(author_id)
        self.validate_is_related_to_anime(author_id)
        self.validate_is_related_to_episode(author_id)


    # Low Level Functions
    def validate_exists_by_id(self, author_id: int) -> None:
        """
        Checks if an author with the given ID exists in the repository.
        
        Args:
            author_id (int): The ID of the author to check.

        Raises:
            HTTPException: If the anime does not exist (status code 404).
        """
        if not self.author_repository.exists_by_id(author_id):
            raise HTTPException(status_code = 404,
                                detail = 'The author does not exist.')


    def validate_unique_name_for_create(self, author_name: str) -> None:
        """
        Validates if the given author name is unique for creation.

        Args:
            author_name (str): The name of the author to validate.

        Raises:
            HTTPException: If the author name already exists (status code 409).
        """
        if self.author_repository.is_name_taken_for_create(author_name):
            self.raise_exception_if_unique_name()


    def validate_aunique_name_for_update(self, exclude_id: int, author_name: str) -> None:
        """
        Validates if the given author name is unique for update,
        excluding the current author.

        Args:
            exclude_id (int): The ID of the current author.
            author_name (str): The name of the author to validate.

        Raises:
            HTTPException: If the author name already exists (status code 409).
        """
        if self.author_repository.is_name_taken_for_update(exclude_id = exclude_id, author_name = author_name):
            self.raise_exception_if_unique_name()


    def validate_birthday_date_not_in_future(self, birthday_date: str) -> None:
        """
        Validates if the given birthday date is not in the future.

        Args:
            release_date (str): The birthday date to validate in format '%Y-%m-%d'.

        Raises:
            HTTPException: If the birthday date is in the future (status code 409).
        """
        current_date = datetime.now().date()
        if birthday_date > current_date:
            raise HTTPException(status_code = 409,
                                detail = "The birthday date should not be in the future.")


    def validate_is_related_to_anime(self, author_id: int) -> None:
        """
        Validates if the author is related to any anime.

        Args:
            author_id (int): The ID of the author to validate.

        Raises:
            HTTPException: If the author is related to any anime (status code 409).
        """
        if self.author_repository.is_related_to_animes(author_id):
            raise HTTPException(status_code = 409,
                                detail = "The author is releated to anime")


    def validate_is_related_to_episode(self, author_id: int) -> None:
        """
        Validates if the author is related to any episode.

        Args:
            author_id (int): The ID of the author to validate.

        Raises:
            HTTPException: If the author is related to any episode (status code 409).
        """
        if self.author_repository.is_related_to_episodes(author_id):
            raise HTTPException(status_code = 409,
                                detail = "The author is releated to episode")


    def validate_has_relationship_with_anime(self, author_id: int, anime_id: int) -> None:
        """
        Validates if the relationship between the author and anime already exists.

        Args:
            author_id (int): The ID of the author.
            anime_id (int): The ID of the anime.

        Raises:
            HTTPException: If the relationship already exists (status code 409).
        """
        if self.author_repository.has_relationship_with_anime(author_id = author_id,
                                                              anime_id = anime_id):
            raise HTTPException(status_code = 409,
                                detail = "The relationship between the author and anime already exists.")


    # Exceptions
    def raise_exception_if_unique_name(self) -> None:
        """
        Raises an HTTPException if the given author name already exists.

        Args:
            author_name (str): The name of the author to check.

        Raises:
            HTTPException: If the author name already exists (status code 409).
        """
        raise HTTPException(status_code = 409,
                            detail = "There is an auhor with that name")
