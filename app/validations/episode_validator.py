"""
This module contains the validation for the episode.
"""
from datetime import date, datetime

from fastapi import Depends, HTTPException

from app.repositories.episode_repository import EpisodeRepository
from app.schemas.episode_schema import EpisodeAuthorRelationSchema, EpisodeSchema
from app.validations.anime_validator import AnimeValidator
from app.validations.author_validator import AuthorValidator


class EpisodeValidator:
    """
    Validator class for validating Episode data.

    This class provides methods to validate the Episode data, including checking if an episode
    exists by ID, validating the episode, and validating the air_date.

    Attributes:
        episode_repository (EpisodeRepository): The repository used for accessing Episode data.
        anime_validator (AnimeValidator): The validator used for validate Anime operations.
        author_validator (AuthorValidator): The validator used for validate Author operations.
    """

    # Constructor
    def __init__(self,
                 episode_repository: EpisodeRepository=Depends(),
                 anime_validator: AnimeValidator=Depends(),
                 author_validator: AuthorValidator=Depends()) -> None:
        """
        Initializes the EpisodeValidator with a repository for accessing episode data.

        Args:
            episode_repository (EpisodeRepository): The repository used for accessing episode data.
            anime_validator (AnimeValidator): The validator used for validate Anime operations.
            author_validator (AuthorValidator): The validator used for validate Author operations.
        """
        self.episode_repository = episode_repository
        self.anime_validator = anime_validator
        self.author_validator = author_validator


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
        self.anime_validator.validate_exists_by_id(episode.anime_id)

        if self.validate_anime_has_episodes(episode.anime_id):
            self.validate_unique_episode_name_for_create(episode)
            self.validate_if_episode_num_taken_in_season_for_create(episode)


    def validate_data_for_update(self, episode_id: int, episode: EpisodeSchema) -> None:
        """
        Validates the data for updating an existing episode.

        This function performs several validations:
        - Checks if the episode exists
        - Validates the air date is not in the future
        - Ensures the episode name is unique for the update
        - Verifies the episode number is not taken in the season

        Args:
            episode_id (int): The ID of the episode to be updated.
            episode (EpisodeSchema): The episode data containing the updates.

        Raises:
            HTTPException: If the episode doesn't exist (status code 404).
            HTTPException: If the air date is in the future (status code 409).
            HTTPException: If there's another episode with the same name (status code 409).
            HTTPException: If there's another episode with the same number
                           in the season (status code 409).
        """
        self.validate_exists_by_id(episode_id)
        self.validate_air_date_not_in_future(episode.air_date)
        self.validate_unique_episode_name_for_update(exclude_anime_id=episode.anime_id,
                                                     data_episode=episode)
        self.validate_if_episode_num_taken_in_season_for_update(exclude_anime_id=episode.anime_id,
                                                                data_episode=episode)


    def validate_data_for_delete(self, episode_id: int) -> None:
        """
        Validates the data before deleting an episode.

        This function checks if the episode exists before allowing its deletion.

        Args:
            episode_id (int): The ID of the episode to be deleted.

        Raises:
            HTTPException: If the episode does not exist (status code 404).
        """
        self.validate_exists_by_id(episode_id)


    def validate_data_for_create_relation_author(
        self,
        data_relation: EpisodeAuthorRelationSchema
    ) -> None:
        """
        Validates the data for creating a relation between an episode and an author.

        This function performs several validations:
        - Checks if the episode exists
        - Checks if the author exists
        - Verifies that the relation between episode and author doesn't already exist

        Args:
            data_relation (EpisodeAuthorRelationSchema): The data containing the episode_id
            and author_id for the relation.

        Raises:
            HTTPException: If the episode does not exist (status code 404).
            HTTPException: If the author does not exist (status code 404).
            HTTPException: If the relation between episode and author
                           already exists (status code 409).
        """
        self.validate_data_for_get(data_relation.episode_id)
        self.author_validator.validate_data_for_get(data_relation.author_id)
        self.validate_unique_episode_author_relation(data_relation)


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


    def validate_air_date_not_in_future(self, air_date: date) -> None:
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
        """
        Validates that the episode name is unique when creating a new episode.

        This function checks if there is already an episode with the same name
        in the anime's episode list.

        Args:
            data_episode (EpisodeSchema): The episode data containing the name to validate.

        Raises:
            HTTPException: If there is already an episode with the same name (status code 409).
        """
        if self.episode_repository.is_episode_name_taken_for_create(data_episode):
            self.exception_unique_episode_name()


    def validate_unique_episode_name_for_update(
        self, exclude_anime_id: int, data_episode: EpisodeSchema) -> None:
        """
        Validates that the episode name is unique when updating an existing episode.

        This function checks if there is already another episode with the same name
        in the anime's episode list, excluding the current episode being updated.

        Args:
            exclude_anime_id (int): The ID of the anime to exclude from the validation.
            data_episode (EpisodeSchema): The episode data containing the new name to validate.

        Raises:
            HTTPException: If there is already another episode with the same name
                            (status code 409).
        """
        if self.episode_repository.is_episode_name_taken_for_update(exclude_anime_id, data_episode):
            self.exception_unique_episode_name()


    def validate_if_episode_num_taken_in_season_for_create(self, episode: EpisodeSchema) -> None:
        """
        Validates that the episode number is not already taken in the season when
        creating a new episode.

        This function checks if there is already an episode with the same number
        in the same season of the anime.

        Args:
            episode (EpisodeSchema): The episode data containing the episode number and season
                information to validate.

        Raises:
            HTTPException: If there is already an episode with the same number in the
                specified season (status code 409).
        """
        if self.episode_repository.is_episode_number_taken_in_season_for_create(episode):
            self.exception_episode_num_taken_in_season()


    def validate_if_episode_num_taken_in_season_for_update(
        self,
        exclude_anime_id: int,
        data_episode: EpisodeSchema
    ) -> None:
        """
        Validates that the episode number is not already taken in the season when
        updating an episode.

        This function checks if there is already another episode with the same number
        in the same season of the anime, excluding the current episode being updated.

        Args:
            exclude_anime_id (int): The ID of the anime to exclude from the validation.
            data_episode (EpisodeSchema): The episode data containing the new episode number
                and season information to validate.

        Raises:
            HTTPException: If there is already another episode with the same number
                in the specified season (status code 409).
        """
        if self.episode_repository.is_episode_number_taken_in_temp_for_update(exclude_anime_id, data_episode):
            self.exception_episode_num_taken_in_season()


    def validate_unique_episode_author_relation(
            self,
            data_relation: EpisodeAuthorRelationSchema
        ) -> None:
            """
            Validates that the relation between an episode and an author is unique.

            This function checks if a relation between the specified episode and author
            already exists in the database.

            Args:
                data_relation (EpisodeAuthorRelationSchema): The data containing the episode_id
                    and author_id for the relation to validate.

            Raises:
                HTTPException: If a relation between the specified episode and author
                    already exists (status code 409).
            """
            if self.episode_repository.exists_relation_between_episode_and_author(
                episode_id=data_relation.episode_id,
                author_id=data_relation.author_id
            ):
                raise HTTPException(
                    detail="The relationship between the episode and author already exists.",
                    status_code=409
                )


    # Exception
    def exception_unique_episode_name(self) -> None:
        """
        Raises an HTTP exception for duplicate episode name.

        This function is called when an attempt is made to create or update an episode
        with a name that already exists in the anime's episode list.

        Raises:
            HTTPException: With a message indicating that the episode name is already
                taken (status code 409).
        """
        raise HTTPException(detail="There is an episode with that name.",
                            status_code=409)


    def exception_episode_num_taken_in_season(self) -> None:
        """
        Raises an HTTP exception for duplicate episode number in a season.

        This function is called when an attempt is made to create or update an episode
        with a number that already exists in the same season of the anime.

        Raises:
            HTTPException: With a message indicating that the episode number is already
                taken in the season (status code 409).
        """
        raise HTTPException(detail="There is an episode with that num in season.",
                            status_code=409)
