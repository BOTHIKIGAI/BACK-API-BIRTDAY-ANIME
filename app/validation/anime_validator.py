"""
This module contains the validation for the anime.
"""
from datetime import datetime
from fastapi import Depends, HTTPException
from app.schemas.anime_schema import AnimeSchema
from app.repositories.anime_repository import AnimeRepository

class AnimeValidator:
    """
    Validator class for validating Anime data.

    This class provides methods to validate the Anime data,
    including checking if an anime exists by ID, validating
    the anime name, and validating the release date.

    Attributes:
        anime_repository (AnimeRepository): The repository used for
        accessing Anime data.
    """

    # Constructor
    def __init__(self, anime_repository: AnimeRepository = Depends()) -> None:
        """
        Initializes the AnimeValidator with a repository for accessing anime data.

        Args:
            anime_repository (AnimeRepository): The repository used for accessing anime data.
        """
        self.anime_repository = anime_repository


    # High Level Functions
    def validate_anime(self, anime_body: AnimeSchema):
        """
        Validates the given anime data.

        Args:
            anime_body (AnimeSchema): The anime data to validate.

        Returns:
            bool: True if the anime data is valid, False otherwise.
        """
        self.validate_name(anime_body.name)
        self.validate_release_date(anime_body.release_date)


    # Low Level Functions
    def anime_exists(self, anime_id: int):
        """
        Checks if an anime with the given ID exists.

        Args:
            anime_id (int): The ID of the anime to check.

        Raises:
            HTTPException: If the anime does not exist (status code 404).

        Returns:
            bool: True if the anime exists, False otherwise.
        """
        if self.anime_repository.exists(anime_id):
            raise HTTPException(status_code = 404,
                                detail = 'The anime does not exist.')


    def validate_name(self, anime_name: str):
        """
        Validates if the given anime name already exists.

        Args:
            anime_name (str): The name of the anime to validate.

        Raises:
            HTTPException: If the anime name already exists (status code 409).

        Returns:
            bool: True if the name is valid, False otherwise.
        """
        if self.anime_repository.name_exists(anime_name):
            raise HTTPException(status_code = 409,
                                detail = "There is an anime with that name")


    def validate_release_date(self, release_date: str):
        """
        Validates if the given release date is not in the future.

        Args:
            release_date (str): The release date to validate in format '%Y-%m-%d'.

        Raises:
            HTTPException: If the release date is in the future (status code 409).

        Returns:
            bool: True if the release date is valid, False otherwise.
        """
        current_date = datetime.now().date()
        if release_date > current_date:
            raise HTTPException(status_code=409,
                                detail="The date of publication should not be in the future.")
