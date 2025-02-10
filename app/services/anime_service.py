"""
This module the service layer or business logic for anime
"""

from typing import List, Optional
from fastapi import Depends
from app.models.tables.anime_models import Anime
from app.models.tables.author_models import Author
from app.models.tables.episode_models import Episode
from app.repositories.anime_repository import AnimeRepository
from app.factories.anime_factory import AnimeFactory
from app.schemas.anime_schema import AnimeSchema
from app.validations.anime_validator import AnimeValidator

class AnimeService:
    """
    Service class for managing Anime class

    This class provides methods to interact with the AnimeService,
    including listing authors with optional filters, retrieving
    a specific anime by ID, creating a new author by ID, creating
    a new author, updating an existing anime, and deleting an anime.

    Attributes:
        anime_repository (AnimeRepository): The repository used for
        accessing Anime data.
    """

    # Attributes
    anime_repository: AnimeRepository


    # Constructor
    def __init__(self,
                 anime_repository: AnimeRepository = Depends(),
                 anime_validator: AnimeValidator = Depends()) -> None:
        """
        Initialize the AnimeService with a repository for accessing
        Anime date.

        Args:
            anime_repository (AnimeRepository): The repository used
            for accessing Anime data.
        """
        self.anime_repository = anime_repository
        self.anime_validator = anime_validator


    # Methods
    def list(self,
             name: Optional[str] = None,
             category: Optional[str] = None,
             release_date: Optional[str] = None,
             page_size: Optional[int] = 100,
             start_index: Optional[int] = 0) -> Optional[List[Anime]]:
        """
        Retrieves a list of anime with optional filters for name,
        category, release_date, limit, start, and supports pagination.

        Args:
            name (Optional[str]): The name of the anime to filter by.
            category (Optional[str]): The alias of the anime to filter by.
            release_date (Optional[str]): The release date of the anime to
                filter by.
            page_size (Optional[int]): The maximum number of results to returns.
                Defaults to 100.
            start_index (Optional[int]): The index of the first result to return.
                Default to 0.

        Returns:
            List[Anime]: A list of anime that match the given
            filters and pagination settings.
        """
        return self.anime_repository.list(
            name = name,
            category = category,
            release_date = release_date,
            limit = page_size,
            start = start_index)


    def get(self, anime_id: int) -> Optional[Anime]:
        """
        Retrieves a specific anime by ID, including related anime
        and episodes.

        Args:
            anime_id (int): The ID of the anime.
        """
        self.anime_validator.validate_data_for_get(anime_id)
        return self.anime_repository.get(anime_id)


    def create(self, anime_body: AnimeSchema) -> Anime:
        """
        Creates a new anime in the database.

        Args:
            anime_body (AnimeSchema): The data of the
            anime to create.

        Returns:
            Author: The created anime with the assigned
            ID.
        """
        self.anime_validator.validate_data_for_create(anime_body)
        anime = AnimeFactory.create(anime_body)
        return self.anime_repository.create(anime)


    def update(self, anime_id: int, anime_body: AnimeSchema) -> Anime:
        """
        Updates an existing anime in the database with the
        provide data.

        Args:
            anime_id (int): The ID of the anime to update.
            anime_body (AnimeSchema): The anime schema.

        Returns:
            Anime: The updated anime with the data.
        """
        self.anime_validator.validate_data_for_update(anime_id = anime_id, anime_body = anime_body)
        anime = AnimeFactory.create(anime_body)
        return self.anime_repository.update(anime_id, anime)


    def delete(self, anime_id: int) -> None:
        """
        Delete an existing anime in the database
        with the given ID.

        Args:
            anime_id (int): The ID of the anime to delete.
        """
        self.anime_validator.validate_data_for_delete(anime_id)
        return self.anime_repository.delete(anime_id)


    def get_authors(self, anime_id: int) -> List[Author]:
        """
        Retrieves the list of authors associated with a specific anime.

        Args:
            anime_id (int): The ID of the anime.

        Returns:
            List[Author]: A list of authors associated with the anime.
        """
        self.anime_validator.validate_data_for_get(anime_id)
        return self.anime_repository.get(anime_id).authors


    def get_episodes(self, anime_id: int) -> List[Episode]:
        """
        Retrieves the list of episodes associated with a specific anime.

        Args:
            anime_id (int): The ID of the anime.

        Returns:
            List[Episode]: A list of episodes associated with the author.
        """
        self.anime_validator.validate_data_for_get(anime_id)
        return self.anime_repository.get(anime_id).episodes
