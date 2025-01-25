"""
This module represents the service layer or business
logic for episode.
"""

from typing import List, Optional
from fastapi import Depends, HTTPException
from app.models.tables.episode_models import Episode
from app.models.tables.anime_models import Anime
from app.models.tables.author_models import Author
from app.repositories.episode_repository import EpisodeRepository
from app.services.author_service import AuthorService
from app.schemas.episode_schema import EpisodeSchema, EpisodeAuthorRelationSchema

class EpisodeService:
    """
    Service class for managing Episode data.

    This class provides methods to interact with the EpisodeRepository,
    including listing episode with optional filters, retrieving a
    specific episode by ID, creating a new episode, updating an
    existing episode, and deleting an episode.

    Attributes:
        episode_repository (EpisodeRepository): The repository
        used for accessing Episode data.
    """

    # Attributes
    episode_repository: EpisodeRepository
    author_service: AuthorService
    
    # Constructor
    def __init__(self,
                 episode_repository: EpisodeRepository = Depends(),
                 author_service: AuthorService = Depends()) -> None:
        """
        Initializes the EpisodeService with a repository for
        accessing Episode data and a service for author logic.

        Args:
            episode_repository (EpisodeRepository): The repository
            used for accessing Episode data.
            author_service (AuthorService): The service used for
            accessing author logic.
        """
        self.episode_repository = episode_repository
        self.author_service = author_service


    # Methods
    def list(self,
             arc: Optional[str] = None,
             temp: Optional[int] = None,
             name: Optional[str] = None,
             episode: Optional[int] = None,
             air_date: Optional[str] = None,
             page_size: Optional[int] = 100,
             start_index: Optional[int] = None) -> Optional[List[Episode]]:
        """
        Retrieves a list of episodes with optional filters
        for arc, temp, episode, air_date and supports pagination.

        Args:
            arc (Optional[str]): The arc of the episode to
            filter by.
            temp (Optional[int]): The alias of the episode 
            to filter by.
            name (Optional[str]): The name of the episode.
            episode (Optional[int]): The episode to filter by.
            air_date (Optional[str]): The air_date of the
            episode to filter by.
            page_size (Optional[int]): The maximum number
            of results to return. Defaults to 100.
            start_index (Optional[int]): The index of the
            first result to return. Defaults to 0.

        Returns:
            List[Episode]: A list of episode that match the
            given filters and pagination settings.
        """
        return self.episode_repository.list(
            arc = arc,
            temp = temp,
            name = name,
            episode = episode,
            air_date = air_date,
            limit = page_size,
            start = start_index)


    def get(self, episode_id: int) -> Optional[Episode]:
        """
        Retrieves a specific episode by ID, including related
        author and anime.

        Args:
            episode_id (int): The ID of the episode to retrieve.

        Returns:
            Episode: The Episode with the given ID, including
            related author and anime.
        """
        if not self.episode_exists(episode_id):
            raise HTTPException(status_code = 404,
                                detail = 'The episode does not exist.')

        return self.episode_repository.get(episode_id)


    def create(self, episode_body: EpisodeSchema) -> Episode:
        """
        Creates a new episode in the database.

        Args:
            episode_body (EpisodeSchema): The data of the author
            to create.

        Returns:
            Episode: The created episode with the assigned ID.
        """
        return self.episode_repository.create(
            Episode(anime_id = episode_body.anime_id,
                    arc = episode_body.arc,
                    temp = episode_body.temp,
                    name = episode_body.name,
                    episode = episode_body.episode,
                    air_date = episode_body.air_date))


    def update(self, episode_id: int, episode_body: EpisodeSchema) -> Episode:
        """
        Updates an existing episode in the database with the
        provided data.

        Args:
            episode_id (int): The ID of the episode to update.
            episode_body (EpisodeSchema): The updated data of
            the episode.

        Returns:
            Author: The updated episode with the new data.
        """
        if not self.episode_exists(episode_id):
            raise HTTPException(status_code = 404,
                                detail = 'The episode does not exist.')

        return self.episode_repository.update(
            episode_id=episode_id,
            episode=Episode(
                anime_id = episode_body.anime_id,
                arc = episode_body.arc,
                temp = episode_body.temp,
                name = episode_body.name,
                episode = episode_body.episode,
                air_date = episode_body.air_date))


    def delete(self, episode_id: int) -> None:
        """
        Deletes an existing episode in the database with the
        given ID.

        Args:
            episode_id (int): The ID of the episode to delete.
        """
        if not self.episode_exists(episode_id):
            raise HTTPException(status_code = 404,
                                detail = 'The episode does not exist.')

        self.episode_repository.delete(episode_id)


    def get_anime(self, episode_id: int) -> Anime:
        """
        Retrieves the Anime associated with a specific episode.

        Args:
            episode_id (int): The ID of the episode.

        Returns:
            Anime: A anime associated with the episode.
        """
        if not self.episode_exists(episode_id):
            raise HTTPException(status_code = 404,
                                detail = 'The episode does not exist.')

        return self.episode_repository.get(episode_id).anime


    def get_author(self, episode_id: int) -> List[Author]:
        """
        Retrieves the list of author/s
        associated with a specific
        episode.

        Args:
            episode_id (int): The ID of the episode.

        Returns:
            List[Episode]: A list of author/s associated with the
            episode.
        """
        if not self.episode_exists(episode_id):
            raise HTTPException(status_code = 404,
                                detail = 'The episode does not exist.')

        return self.episode_repository.get(episode_id).authors


    def create_author_relation(self,
                               episode_id: int,
                               author_id: int) -> EpisodeAuthorRelationSchema:
        """
        Creates a relationship between an episode and an author.

        Args:
            episode_id (int): The ID of the episode.
            author_id (int): The ID of the author.

        Returns:
            EpisodeAuthorRelationSchema: The created relationship data.

        Raises:
            HTTPException: If the episode or author does not exist.
        """
        if not self.episode_exists(episode_id):
            raise HTTPException(status_code = 404,
                                detail = 'The episode does not exist.')

        if not self.author_service.author_exists(author_id):
            raise HTTPException(status_code = 404,
                                detail = 'The author does not exist.')

        return self.episode_repository.create_author_relation(episode_id = episode_id,
                                                              author_id = author_id)


    def episode_exists(self, episode_id: int) -> bool:
        """
        Checks if an episode with the given ID exists in the repository.
        
        Args:
            episode_id (int): The ID of the episode to check.
        
        Returns:
            bool: True if the episode exists, False otherwise.
        """
        return self.episode_repository.exists(episode_id)
