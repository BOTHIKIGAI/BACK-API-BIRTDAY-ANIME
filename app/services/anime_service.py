"""
This module the service layer or
bussines logic for anime
"""

from typing import List, Optional
from fastapi import Depends, HTTPException
from app.models.tables.anime_models import Anime
from app.models.tables.author_models import Author
from app.models.tables.episode_models import Episode
from app.repositories.anime_repository import AnimeRepository
from app.schemas.anime_schema import AnimeSchema

class AnimeService:
    """
    Service class for managing Anime class

    This class provides methods to interact
    with the AnimeService, including listing
    authors with optional filters, retrieving
    a specific anime by ID, creating a new
    author by ID, creating a new author,
    updating an existing anime, and deleting
    an anime.

    Attributes:
        anime_repository (AnimeRepository):
        The repository used for accesing
        Anime data.
    """

    # Attributes
    animeRepository: AnimeRepository

    # Constructor
    def __init__(self, anime_repository: AnimeRepository = Depends()) -> None:
        """
        Initialize the AnimeService with a
        repository for accesing Anime date.

        Args:
            anime_repository (AnimeRepository):
            The repository used for accesing
            Anime data.
        """
        self.anime_repository = anime_repository

    def list(self,
             name: Optional[str] = None,
             category: Optional[str] = None,
             release_date: Optional[str] = None,
             page_size: Optional[int] = 100,
             start_index: Optional[int] = 0) -> Optional[List[Anime]]:
        """
        Retrieves a list of anime with
        optional filters for name,
        category, release_date, limit,
        start, and supports pagination.

        Args:
            name (Optional[str]): The name
            of the anime to filter by.
            category (Optional[str]): The alias
            of the anime to filter by.
            release_date (Optional[str]): The
            release date of the anime to filter
            by.
            page_size (Optional[int]): The
            maximum number of results to returns.
            Defaults to 100.
            start_index (Optional[int]): The
            index of the first result to return.
            Default to 0.

        Returns:
            List[Anime]: A list of anime that match
            the given filters and pagination
            settings.
        """
        return self.anime_repository.list(
            name=name,
            category=category,
            release_date=release_date,
            limit=page_size,
            start=start_index)

    def get(self, anime_id: int) -> Optional[Anime]:
        """
        Retrieves a specific anime by ID, incluiding
        related anime and episodes.

        Args:
            Anime: The anime with the given ID,
            incluiding related author and episodes.
        """
        anime = self.anime_repository.get(anime_id)
        if not anime:
            raise HTTPException(status_code=404,
                                detail="Anime not found")
        return anime

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
        return self.anime_repository.create(
            Anime(name=anime_body.name,
                  category=anime_body.category,
                  release_date=anime_body.release_date))

    def update(self,
               anime_id: int,
               anime_body: AnimeSchema) -> Anime:
        """
        Updates an existing anime in the database
        with the provide data.

        Args:
            anime_id (int): The ID of the anime
            to update
            anime (AnimeSchema): 

        Returns:
            Anime: The updated anime with the
            data.
        """
        if not self.get(anime_id):
            raise HTTPException(status_code=404,
                                detail="Anime not found")
        return self.anime_repository.update(
            anime_id,
            Anime(name=anime_body.name,
                  category=anime_body.category,
                  release_date=anime_body.release_date))

    def delete(self, anime_id: int) -> None:
        """
        Delete an existing anime in the database
        with the given ID.

        Args:
            anime_id (int): The ID of the anime to
            delete
        """
        if not self.get(anime_id):
            raise HTTPException(status_code=404,
                                detail="Anime not found")
        return self.anime_repository.delete(anime_id)

    def get_authors(self, anime_id: int) -> List[Author]:
        """
        Retrieves the list of authors associated
        with a specific anime.

        Args:
            anime_id (int): The ID of the anime.

        Returns:
            List[Author]: A list of authors
            associated with the anime.
        """
        if not self.get(anime_id):
            raise HTTPException(status_code=404,
                                detail="Author not found")
        return self.anime_repository.get(anime_id).authors

    def get_episodes(self, anime_id: int) -> List[Episode]:
        """
        Retrieves the list of episodes associated
        with a specific anime.
        
        Args:
            anime_id (int): The ID of the anime.

        Returns:
            List[Episode]: A list of episoddes associated
            with the author.
        """
        if not self.get(anime_id):
            raise HTTPException(status_code=404,
                                detail="Anime not found")
        return self.anime_repository.get(anime_id).episodes