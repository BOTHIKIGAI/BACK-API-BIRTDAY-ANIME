"""
This module contains the validation for the episode.
"""
from datetime import datetime

from fastapi import Depends, HTTPException

from app.repositories.anime_repository import AnimeRepository
from app.repositories.episode_repository import EpisodeRepository
from app.schemas.episode_schema import EpisodeSchema


class EpisodeValidator:
    """
    Validator class for validating Episode data.

    This class provides methods to validate the Episode data, including checking if an episode
    exists by ID, validating the episode, and validating the air_date.

    Attributes:
        episode_repository (EpisodeRepository): The repository used for accessing Episode data.
        anime_repository (AnimeRepository): The repository used for accessing Anime data.
    """

    # Constructor
    def __init__(self,
                 episode_repository: EpisodeRepository = Depends(),
                 anime_repository: AnimeRepository = Depends()) -> None:
        """
        Initializes the EpisodeValidator with a repository for accessing episode data.

        Args:
            episode_repository (EpisodeRepository): The repository used for accessing episode data.
            anime_repository (AnimeRepository): The repository used for accessing anime data.
        """
        self.episode_repository = episode_repository
        self.anime_repository = anime_repository


    # High Level Function
    def validate_data_for_get(self, episode_id: int) -> None:
        self.validate_exists_by_id(episode_id)


    def validate_data_for_create(self, episode: EpisodeSchema) -> None:
        """
        Validates the given episode data.

        Args:
            episode (EpisodeSchema): The episode data to validate.

        Raises:
            HTTPException: If the air date is in the future (status code 409).
            HTTPException: If the episode number is already registered (status code 409).
            HTTPException: If the episode name is already registered (status code 409).
        """

        self.validate_air_date_not_in_future(episode.air_date)

        if self.validate_anime_has_episodes(episode.anime_id):
            self.validate_unique_episode_name_for_create(episode)
            self.validate_if_episode_num_taken_in_season_for_create(episode)


    def validate_data_for_update(self, episode_id: int, episode: EpisodeSchema) -> None:
        self.validate_exists_by_id(episode_id)
        self.validate_air_date_not_in_future(episode.air_date)
        self.validate_unique_episode_name_for_update(exclude_anime_id=episode.anime_id,
                                                     data_episode=episode)
        self.validate_if_episode_num_taken_in_season_for_update(exclude_anime_id=episode.anime_id,
                                                                data_episode=episode)


    def validate_data_for_delete(self, episode_id: int) -> None:
        self.validate_exists_by_id(episode_id)


    # Low Level Function
    def validate_anime_has_episodes(self, anime_id: int) -> bool:
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
            raise HTTPException(detail='The episode does not exist.',
                                status_code=404)


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
            raise HTTPException(detail="The air date should not be in the future.",
                                status_code=409)


    def validate_unique_episode_name_for_create(self, data_episode: EpisodeSchema) -> None:
        if self.episode_repository.is_episode_name_taken_for_create(data_episode):
            self.exception_unique_episode_name()


    def validate_unique_episode_name_for_update(self, exclude_anime_id: int, data_episode: EpisodeSchema) -> None:
        if self.episode_repository.is_episode_name_taken_for_update(exclude_anime_id, data_episode):
            self.exception_unique_episode_name()


    def validate_if_episode_num_taken_in_season_for_create(self, episode: EpisodeSchema) -> None:
        if self.episode_repository.is_episode_number_taken_in_season_for_create(episode):
            self.exception_episode_num_taken_in_season()


    def validate_if_episode_num_taken_in_season_for_update(self, exclude_anime_id: int, data_episode: EpisodeSchema) -> None:
        if self.episode_repository.is_episode_number_taken_in_temp_for_update(exclude_anime_id, data_episode):
            self.exception_episode_num_taken_in_season()


    # Exception
    def exception_unique_episode_name(self):
        raise HTTPException(detail="There is an episode with that name.",
                            status_code=409)


    def exception_episode_num_taken_in_season(self):
        raise HTTPException(detail="There is an episode with that num in season.",
                            status_code=409)
