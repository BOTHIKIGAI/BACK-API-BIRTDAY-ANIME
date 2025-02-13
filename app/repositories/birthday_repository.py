"""
Repository module for managing birthday and date-related queries in the anime database system.
"""
from datetime import date
from typing import List

from fastapi import Depends
from sqlalchemy.orm import Session

from app.config.database import get_db_connection
from app.models.tables.anime_models import Anime
from app.models.tables.author_models import Author
from app.repositories.anime_repository import AnimeRepository
from app.repositories.author_repository import AuthorRepository
from app.repositories.episode_repository import EpisodeRepository


class BirthdayRepository:
    """
    Repository class for managing birthday-related queries across different entities.

    This class provides methods to retrieve authors, anime, and episodes based on
    specific dates (birthdays or release dates). It acts as a centralized repository
    for date-based queries across different entities in the system.

    Attributes:
        db (Session): Database session for executing queries.
        anime_repository (AnimeRepository): Repository for anime-related operations.
        author_repository (AuthorRepository): Repository for author-related operations.
        episode_repository (EpisodeRepository): Repository for episode-related operations.

    The repository coordinates with other specific repositories to provide
    comprehensive date-based search functionality across the application's
    different entities.
    """

    # Attributes
    db: Session
    anime_repository: AnimeRepository
    author_repository: AuthorRepository
    episode_repository: EpisodeRepository

    def __init__(
        self,
        db: Session = Depends(get_db_connection),
        anime_repository: AnimeRepository = Depends(),
        author_repository: AuthorRepository = Depends(),
        episode_repository: EpisodeRepository = Depends()
    ) -> None:
        """
        Initializes a new instance of the BirthdayRepository.

        This constructor sets up the repository with necessary dependencies for
        accessing and managing birthday-related data across different entities.

        Args:
            db (Session): Database session for executing queries.
                Defaults to dependency injection from get_db_connection.
            anime_repository (AnimeRepository): Repository for anime-related operations.
                Defaults to dependency injection.
            author_repository (AuthorRepository): Repository for author-related operations.
                Defaults to dependency injection.
            episode_repository (EpisodeRepository): Repository for episode-related operations.
                Defaults to dependency injection.
        """
        self.author_repository = author_repository
        self.anime_repository = anime_repository
        self.episode_repository = episode_repository


    def get_authors_matching_date(self, target_date: date) -> List[Author]:
        """
        Retrieves all authors whose birthday matches the specified date.

        This method queries the database through the author repository to find
        authors with a birthday that matches the provided date. This is useful
        for finding authors who were born on a specific date.

        Args:
            target_date (date): The date to match against authors' birthdays.

        Returns:
            List[Author]: A list of Author instances whose birthday matches
                            the specified date.
        """
        return self.author_repository.get_by_birthday(target_date)


    def get_animes_matching_date(self, target_date: date) -> List[Anime]:
        """
        Retrieves all anime whose release date matches the specified date.

        This method queries the database through the anime repository to find
        anime with a release date that matches the provided date.

        Args:
            target_date (date): The date to match against anime release dates.

        Returns:
            List[Anime]: A list of Anime instances whose release date matches
                        the specified date.
        """
        return self.anime_repository.get_by_release_date(target_date)


    def get_episodes_matching_date(self, target_date: date) -> int:
        """
        Retrieves all episodes whose release date matches the specified date.

        This method queries the database through the episode repository to find
        episodes with a release date that matches the provided date.

        Args:
            target_date (date): The date to match against episode release dates.

        Returns:
            int: The number of episodes whose release date matches the specified date.
        """
        return self.episode_repository.get_by_release_date(target_date)
