"""
This module represents the service layer or business logic for episode.
"""

from typing import List, Optional

from fastapi import Depends

from app.factories.episode_factory import EpisodeFactory
from app.models.tables.anime_models import Anime
from app.models.tables.author_models import Author
from app.models.tables.episode_models import Episode
from app.repositories.episode_repository import EpisodeRepository
from app.repositories.anime_repository import AnimeRepository
from app.repositories.author_repository import AuthorRepository
from app.schemas.episode_schema import EpisodeAuthorRelationSchema, EpisodeSchema
from app.validations.episode_validator import EpisodeValidator


class EpisodeService:
    """
    Service class for managing Episode data.

    This class provides methods to interact with the EpisodeRepository, including listing episodes
    with optional filters, retrieving a specific episode by ID, creating a new episode, updating an
    existing episode, deleting an episode, and creating relationships between episodes and authors.

    Attributes:
        episode_repository (EpisodeRepository): The repository used for accessing Episode data.
        episode_factory (EpisodeFactory): The factory used for creating Episode instances.
        author_validator (AuthorValidator): The service used for accessing Author data.
        anime_repository (AnimeRepository): The service used for accessing Anime data.
        author_repository (AuthorRepository): The service used for accessing Author data.
    """

    # Attributes
    episode_repository: EpisodeRepository
    episode_factory: EpisodeFactory
    episode_validator: EpisodeValidator
    anime_repository: AnimeRepository
    author_repository: AuthorRepository

    # Constructor
    def __init__(self,
                 episode_repository: EpisodeRepository = Depends(),
                 episode_factory: EpisodeFactory = Depends(),
                 episode_validator: EpisodeValidator = Depends(),
                 anime_repository: AnimeRepository = Depends(),
                 author_repository: AuthorRepository = Depends()) -> None:
        """
        Initializes the EpisodeService with repositories and services for accessing Episode data
        and author logic.

        Args:
            episode_repository (EpisodeRepository): The repository used for accessing Episode data.
            episode_factory (EpisodeFactory): The factory used for creating Episode instances.
            anime_repository (AnimeRepository): The service used for accessing Anime data.
            author_repository (AuthorRepository): The service used for accessing Author data.
        """
        self.episode_repository = episode_repository
        self.episode_factory = episode_factory
        self.episode_validator = episode_validator
        self.anime_repository = anime_repository
        self.author_repository = author_repository


    # Methods
    def list(self,
             anime_id: Optional[int] = None,
             arc: Optional[str] = None,
             season: Optional[int] = None,
             name: Optional[str] = None,
             episode: Optional[int] = None,
             air_date: Optional[str] = None,
             page_size: Optional[int] = 100,
             start_index: Optional[int] = None) -> Optional[List[Episode]]:
        return self.episode_repository.list(
            anime_id = anime_id,
            arc = arc,
            season = season,
            name = name,
            episode = episode,
            air_date = air_date,
            limit = page_size,
            start = start_index)


    def get(self, episode_id: int) -> Episode:
        """
        Retrieves a specific episode by ID.

        Args:
            episode_id (int): The ID of the episode to retrieve.

        Returns:
            Episode: The episode object if found.

        Raises:
            HTTPException: If the episode does not exist (status code 404).
        """
        self.episode_validator.validate_data_for_get(episode_id)
        return self.episode_repository.get(episode_id)


    def create(self, episode_body: EpisodeSchema) -> Episode:
        """
        Creates a new episode in the database.

        Args:
            episode_body (EpisodeSchema): The data of the episode to create.

        Returns:
            Episode: The created episode with the assigned ID.

        Raises:
            HTTPException: If the episode data is invalid.
        """
        self.episode_validator.validate_data_for_create(episode_body)
        episode = self.episode_factory.create(episode_body)
        return self.episode_repository.create(episode)


    def update(self, episode_id: int, episode_body: EpisodeSchema) -> Episode:
        """
        Updates an existing episode in the database with the provided data.

        Args:
            episode_id (int): The ID of the episode to update.
            episode_body (EpisodeSchema): The data of the episode to update.

        Returns:
            Episode: The updated episode with the new data.

        Raises:
            HTTPException: If the episode does not exist or the episode data is invalid.
        """
        self.episode_validator.validate_data_for_update(episode_id, episode_body)
        episode = self.episode_factory.create_for_update(episode_id=episode_id,
                                                         episode_body=episode_body)
        return self.episode_repository.update(episode)


    def delete(self, episode_id: int) -> None:
        """
        Deletes an existing episode in the database with the given ID.

        Args:
            episode_id (int): The ID of the episode to delete.

        Raises:
            HTTPException: If the episode does not exist (status code 404).
        """
        self.episode_validator.validate_data_for_delete(episode_id)
        self.episode_repository.delete(episode_id)


    def get_anime(self, episode_id: int) -> Anime:
        """
        Retrieves the anime associated with a specific episode by episode ID.

        Args:
            episode_id (int): The ID of the episode.

        Returns:
            Anime: The anime associated with the episode.

        Raises:
            HTTPException: If the episode does not exist (status code 404).
        """
        self.episode_validator.validate_exists_by_id(episode_id)
        return self.anime_repository.get_by_episode(episode_id)


    def get_author(self, episode_id: int) -> List[Author]:
        """
        Retrieves the list of authors associated with a specific episode.

        Args:
            episode_id (int): The ID of the episode.

        Returns:
            List[Author]: A list of authors associated with the episode.

        Raises:
            HTTPException: If the episode does not exist (status code 404).
        """
        self.episode_validator.validate_exists_by_id(episode_id)
        return self.author_repository.get_by_episode(episode_id)


    def create_author_relation(
            self,
            data_relation: EpisodeAuthorRelationSchema
        ) -> EpisodeAuthorRelationSchema:
            """
            Creates a relationship between an episode and an author.

            Args:
                episode_id (int): The ID of the episode.
                author_id (int): The ID of the author.

            Returns:
                EpisodeAuthorRelationSchema: The created relationship data.

            Raises:
                HTTPException: If the episode or author does not exist (status code 404).
            """
            self.episode_validator.validate_data_for_create_relation_author(data_relation)
            return self.episode_repository.create_author_relation(data_relation)
