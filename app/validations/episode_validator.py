"""
This module contains the validation for the episode.
"""
from datetime import datetime
from fastapi import Depends, HTTPException
from app.schemas.episode_schema import EpisodeSchema
from app.repositories.episode_repository import EpisodeRepository
from app.repositories.anime_repository import AnimeRepository

class EpisodeValidator:
    """
    Validator class for validating Episode data.

    This class provides methods to validate the Episode data,
    including checking if an episode exists by ID, validating
    the episode, and validating the air_date.

    Attributes:
        episode_repository (EpisodeRepository): The repository used for
        accessing Episode data.
        anime_repository (AnimeRepository): The repository used for
        accessing Anime data.
    """

    # Constructor
    def __init__(self,
                 episode_repository: EpisodeRepository = Depends(),
                 anime_repository: AnimeRepository = Depends()) -> None:
        """
        Initializes the EpisodeValidator with a repository
        for accessing episode data.

        Args:
            episode_repository (EpisodeRepository): The repository
            used for accessing episode data.
            anime_repository (AnimeRepository): The repository
            used for accessing anime data.
        """
        self.episode_repository = episode_repository
        self.anime_repository = anime_repository


    # High Level Function
    def validate_data(self, episode: EpisodeSchema) -> None:
        """
        Validates the given episode data.

        Args:
            episode (EpisodeSchema): The episode data to validate.

        Raises:
            HTTPException: If the air date is in the future (status code 409).
            HTTPException: If the episode number is already registered (status code 409).
            HTTPException: If the episode name is already registered (status code 409).
        """
        self.validate_air_date_not_in_future(air_date = episode.air_date)
        
        if self.validate_anime_has_episodes(episode.anime_id):
            self.validate_unique_episode_name(anime_id = episode.anime_id,
                                              name = episode.name)


    # Low Level Function
    def validate_anime_has_episodes(self, anime_id: int) -> None:
        """
        Validates if the given anime has episodes.

        Args:
            anime_id (int): The ID of the anime to validate.

        Raises:
            HTTPException: If the anime does not have any episodes (status code 404).
        """
        return self.episode_repository.anime_has_episodes(anime_id)


    def validate_exists_by_id(self, episode_id: int) -> None:
        """
        Validates if an episode with the given ID exists.

        Args:
            episode_id (int): The ID of the episode to validate.

        Raises:
            HTTPException: If the episode does not exist (status code 404).
        """
        if not self.episode_repository.exists_by_id(episode_id):
            raise HTTPException(status_code = 404,
                                detail = 'The episode does not exist.')


    def validate_air_date_not_in_future(self, air_date: str) -> None:
        """
        Validates that the air date of an episode is not in
        the future.

        Args:
            air_date (str): The air date to validate in
            format '%Y-%m-%d'.

        Raises:
            HTTPException: If the air date is in the future (status code 409).
        """
        current_date = datetime.now().date()
        if air_date > current_date:
            raise HTTPException(status_code=409,
                                detail = "The air date should not be in the future.")


    def validate_unique_episode_name(self, anime_id: int, name: str) -> None:
        """
        Validates if an episode name is already registered for a given anime.

        Args:
            anime_id (int): The ID of the anime.
            name (str): The name of the episode to validate.

        Raises:
            HTTPException: If the episode name is already registered (status code 409).
        """
        if self.episode_repository.is_episode_name_taken(anime_id = anime_id, name = name):
            raise HTTPException(status_code=409,
                                detail = "There is an episode with that name.")
