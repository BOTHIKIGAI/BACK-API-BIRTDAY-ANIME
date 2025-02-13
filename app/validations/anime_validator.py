"""
This module contains the validation for the anime.
"""
from datetime import date, datetime

from fastapi import Depends, HTTPException

from app.repositories.anime_repository import AnimeRepository
from app.schemas.anime_schema import AnimeSchema


class AnimeValidator:
    """
    Validator class for validating Anime data.

    This class provides methods to validate the Anime data, including checking if an anime exists
    by ID, validating the anime name, and validating the release date.

    Attributes:
        anime_repository (AnimeRepository): The repository used for accessing Anime data.
    """


    # Constructor
    def __init__(self, anime_repository: AnimeRepository=Depends()) -> None:
        """
        Initializes the AnimeValidator with a repository for accessing anime data.

        Args:
            anime_repository (AnimeRepository): The repository used for accessing anime data.
        """
        self.anime_repository = anime_repository


    # High Level Functions
    def validate_data_for_get(self, anime_id: int) -> None:
        """
        Validates the given anime ID for retrieval.

        Args:
            anime_id (int): The ID of the anime to validate.

        Raises:
            HTTPException: If the anime does not exist (status code 404).
        """
        self.validate_exists_by_id(anime_id)


    def validate_data_for_create(self, anime_body: AnimeSchema) -> None:
        """
        Validates the given anime data for creation.

        Args:
            anime_body (AnimeSchema): The anime data to validate.

        Raises:
            HTTPException: If the anime name already exists (status code 409).
            HTTPException: If the release date is in the future (status code 409).
        """
        self.validate_unique_name_for_create(anime_body.name)
        self.validate_release_date_not_in_future(anime_body.release_date)


    def validate_data_for_update(self, anime_id: int, anime_body: AnimeSchema) -> None:
        """
        Validates the given anime data for update.

        Args:
            anime_id (int): The ID of the anime to validate.
            anime_body (AnimeSchema): The anime data to validate.

        Raises:
            HTTPException: If the anime does not exist (status code 404).
            HTTPException: If the anime name already exists (status code 409).
            HTTPException: If the release date is in the future (status code 409).
        """
        self.validate_exists_by_id(anime_id)
        self.validate_unique_name_for_update(exclude_id=anime_id, anime_name=anime_body.name)
        self.validate_release_date_not_in_future(anime_body.release_date)


    def validate_data_for_delete(self, anime_id: int) -> None:
        """
        Validates the given anime ID for deletion.

        Args:
            anime_id (int): The ID of the anime to validate.

        Raises:
            HTTPException: If the anime does not exist (status code 404).
            HTTPException: If the anime is related to any episode (status code 409).
        """
        self.validate_exists_by_id(anime_id)
        self.validate_is_related_to_episode(anime_id)


    # Low Level Functions
    def validate_exists_by_id(self, anime_id: int) -> None:
        """
        Validates if an anime with the given ID exists.

        Args:
            anime_id (int): The ID of the anime to validate.

        Raises:
            HTTPException: If the anime does not exist (status code 404).
        """
        if not self.anime_repository.exists_by_id(anime_id):
            raise HTTPException(detail='The anime does not exist.',
                                status_code=404)


    def validate_is_related_to_episode(self, anime_id: int) -> None:
        """
        Validates if the anime is related to any episode.

        Args:
            anime_id (int): The ID of the anime to validate.

        Raises:
            HTTPException: If the anime is related to any episode (status code 409).
        """
        if self.anime_repository.is_related_to_episode(anime_id):
            raise HTTPException(detail="The anime is related to episode",
                                status_code=409)


    def validate_unique_name_for_create(self, anime_name: str) -> None:
        """
        Validates if the given anime name is unique for creation.

        Args:
            anime_name (str): The name of the anime to validate.

        Raises:
            HTTPException: If the anime name already exists (status code 409).
        """
        if self.anime_repository.is_name_taken_for_create(anime_name):
            self.exception_unique_name()


    def validate_unique_name_for_update(self, exclude_id: int, anime_name: str) -> None:
        """
        Validates if the given anime name is unique for update, excluding the current anime.

        Args:
            exclude_id (int): The ID of the current anime.
            anime_name (str): The name of the anime to validate.

        Raises:
            HTTPException: If the anime name already exists (status code 409).
        """
        if self.anime_repository.is_name_taken_for_update(exclude_id=exclude_id,
                                                          anime_name=anime_name):
                self.exception_unique_name()


    def validate_release_date_not_in_future(self, release_date: date) -> None:
        """
        Validates if the given release date is not in the future.

        Args:
            release_date (date): The release date to validate in format '%Y-%m-%d'.

        Raises:
            HTTPException: If the release date is in the future (status code 409).
        """
        current_date = datetime.now().date()
        if release_date > current_date:
            raise HTTPException(detail="The date of publication should not be in the future.",
                                status_code=409)


    # Exceptions
    def exception_unique_name(self) -> None:
        """
        Raises an HTTPException if the given anime name already exists.

        Raises:
            HTTPException: If the anime name already exists (status code 409).
        """
        raise HTTPException(detail="There is an anime with that name",
                            status_code=409)
