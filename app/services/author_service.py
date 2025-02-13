"""
This module represents the service layer or business logic
for author.
"""
from typing import List, Optional

from fastapi import Depends

from app.factories.author_factory import AuthorFactory
from app.models.tables.anime_models import Anime
from app.models.tables.author_models import Author
from app.models.tables.episode_models import Episode
from app.repositories.anime_repository import AnimeRepository
from app.repositories.author_repository import AuthorRepository
from app.repositories.episode_repository import EpisodeRepository
from app.schemas.author_schema import AuthorAnimeRelationSchema, AuthorSchema
from app.validations.anime_validator import AnimeValidator
from app.validations.author_validator import AuthorValidator


class AuthorService:
    """
    Service class for managing Author data.

    This class provides methods to interact with the AuthorRepository,
    including listing authors with optional filters, retrieving
    a specific author by ID, creating a new author, updating an existing
    author, deleting an author, and creating relationships between authors
    and animes.

    Attributes:
        author_repository (AuthorRepository): The repository used for
        accessing Author data.
        author_validator (AuthorValidator): The validator used for
        validating Author data.
        anime_validator (AnimeValidator): The validator used for
        validating Anime data.
    """
    # Attributes
    author_repository: AuthorRepository
    author_validator: AuthorValidator
    anime_validator: AnimeValidator
    anime_repository: AnimeRepository
    episode_repository: EpisodeRepository


    # Constructor
    def __init__(self,
                 author_repository: AuthorRepository = Depends(),
                 author_validator: AuthorValidator = Depends(),
                 anime_validator: AnimeValidator = Depends(),
                 anime_repositoy: AnimeRepository = Depends(),
                 episode_repository: EpisodeRepository = Depends()) -> None:
        """
        Initializes the AuthorService with repositories and validators
        for accessing and validating Author and Anime data.

        Args:
            author_repository (AuthorRepository): The repository used
            for accessing Author data.
            author_validator (AuthorValidator): The validator used for
            validating Author data.
            anime_validator (AnimeValidator): The validator used for
            validating Anime data.
        """
        self.author_repository = author_repository
        self.author_validator = author_validator
        self.anime_validator = anime_validator
        self.anime_repository = anime_repositoy
        self.episode_repository = episode_repository


    # Methods
    def list(self,
             name: Optional[str] = None,
             alias: Optional[str] = None,
             birthday: Optional[str] = None,
             page_size: Optional[int] = 100,
             start_index: Optional[int] = 0) -> Optional[List[Author]]:
        """
        Retrieves a list of authors with optional filters for name,
        alias, and birthday, and supports pagination.

        Args:
            name (Optional[str]): The name of the author to  filter by.
            alias (Optional[str]): The alias of the author  to filter by.
            birthday (Optional[str]): The birthday of the author to filter by.
            page_size (Optional[int]): The maximum number of results to return.
                Defaults to 100.
            start_index (Optional[int]): The index of the first result to return.
                Defaults to 0.

        Returns:
            List[Author]: A list of authors that match the given filters and
            pagination settings.
        """
        return self.author_repository.list(
            name = name,
            alias = alias,
            birthday = birthday,
            limit = page_size,
            start = start_index)


    def get(self, author_id: int) -> Optional[Author]:
        """
        Retrieves a specific author by ID, including related
        anime's and episodes.

        Args:
            author_id (int): The ID of the author to retrieve.

        Returns:
            Author: The author with the given ID, including
            related anime's and episodes.
        """
        self.author_validator.validate_data_for_get(author_id)
        return self.author_repository.get(author_id)


    def create(self, author_body: AuthorSchema) -> Author:
        """
        Creates a new author in the database.

        Args:
            author_body (AuthorSchema): The data of the author
            to create.

        Returns:
            Author: The created author with the assigned ID.
        """
        self.author_validator.validate_data_for_create(author_body)
        author = AuthorFactory.create(author_body)
        return self.author_repository.create(author)


    def update(self, author_id: int, author_body: AuthorSchema) -> Author:
        """
        Updates an existing author in the database with the provided data.

        Args:
            author_id (int): The ID of the author to update.
            author_body (AuthorSchema): The updated data of the author.

        Returns:
            Author: The updated author with the new data.
        """
        self.author_validator.validate_data_for_update(author_id=author_id, author_body=author_body)
        author = AuthorFactory.create_for_update(author_id=author_id, author_body=author_body)
        return self.author_repository.update(author)


    def delete(self, author_id: int) -> None:
        """
        Deletes an existing author in the database with
        the given ID.

        Args:
            author_id (int): The ID of the author to delete.
        """
        self.author_validator.validate_data_for_delete(author_id)
        self.author_repository.delete(author_id)


    def get_anime(self, author_id: int) -> List[Anime]:
        """
        Retrieves the list of anime's associated with a specific
        author.

        Args:
            author_id (int): The ID of the author.

        Returns:
            List[Anime]: A list of anime's associated with the
            author.
        """
        self.author_validator.validate_data_for_get(author_id)
        return self.anime_repository.get_by_author(author_id)


    def create_anime_relation(self, data_relation: AuthorAnimeRelationSchema):
        """
        Creates a relationship between an author and an anime.

        Args:
            author_id (int): The ID of the author.
            anime_id (int): The ID of the anime.

        Returns:
            AuthorAnimeRelationSchema: The created relationship data.

        Raises:
            HTTPException: If the author does not exist (status code 404).
            HTTPException: If the anime does not exist (status code 404).
            HTTPException: If the relationship already exists (status code 409).
        """
        self.author_validator.validate_data_for_get(data_relation.author_id)
        self.anime_validator.validate_data_for_get(data_relation.anime_id)
        self.author_validator.validate_has_relationship_with_anime(data_relation)
        return self.author_repository.create_anime_relation(data_relation)


    def get_episodes(self, author_id: int) -> List[Episode]:
        """
        Retrieves the list of episodes associated with a specific
        author.

        Args:
            author_id (int): The ID of the author.

        Returns:
            List[Episode]: A list of episodes associated with the
            author.
        """
        self.author_validator.validate_data_for_get(author_id)
        return self.episode_repository.get_by_author(author_id)
