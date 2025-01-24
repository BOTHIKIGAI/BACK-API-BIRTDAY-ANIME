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
from app.schemas.episode_schema import EpisodeSchema

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
    
    # Constructor
    def __init__(self, episode_repository: EpisodeRepository = Depends()) -> None:
        """
        Initializes the EpisodeService with a repository for
        accessing Episode data.

        Args:
            episode_repository (EpisodeRepository):
                The repository used for
                accessing Episode data.
        """
        self.episode_repository = episode_repository
    
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
            arc=arc,
            temp=temp,
            name=name,
            episode=episode,
            air_date=air_date,
            limit=page_size,
            start=start_index)
    
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
        episode = self.episode_repository.get(episode_id)
        if not episode:
            raise HTTPException(
                status_code=404,
                detail="Episode not found")
        return episode
    
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
        self.get(episode_id)
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
        self.get(episode_id)
        self.episode_repository.delete(episode_id)
    
    def get_anime(self, episode_id: int) -> Anime:
        """
        Retrieves the Anime associated with a specific episode.

        Args:
            episode_id (int): The ID of the episode.

        Returns:
            Anime: A anime associated with the episode.
        """
        self.get(episode_id)
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
        self.get(episode_id)
        return self.episode_repository.get(episode_id).authors
