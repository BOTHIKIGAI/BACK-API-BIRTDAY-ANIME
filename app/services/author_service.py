"""
This module represents the service layer or
business logic for author.
"""

from typing import List, Optional
from fastapi import Depends, HTTPException
from app.models.tables.author_models import Author
from app.models.tables.anime_models import Anime
from app.models.tables.episode_models import Episode
from app.repositories.author_repository import AuthorRepository
from app.schemas.author_schema import AuthorSchema

class AuthorService:
    """
    Service class for managing Author data.

    This class provides methods to interact with the
    AuthorRepository, including listing authors with
    optional filters, retrieving a specific author by
    ID, creating a new author, updating an existing
    author, and deleting an author.

    Attributes:
        author_repository (AuthorRepository): The repository
        used for accessing Author data.
    """
    authorRepository: AuthorRepository

    def __init__(self, author_repository: AuthorRepository = Depends()) -> None:
        """
        Initializes the AuthorService with a repository
        for accessing Author data.

        Args:
            author_repository (AuthorRepository): The 
            repository used for accessing Author data.
        """

        self.author_repository = author_repository

    def list(self,
             name: Optional[str] = None,
             alias: Optional[str] = None,
             birthday: Optional[str] = None,
             page_size: Optional[int] = 100,
             start_index: Optional[int] = 0) -> Optional[List[Author]]:
        """
        Retrieves a list of authors with optional filters
        for name, alias, and birthday, and supports pagination.

        Args:
            name (Optional[str]): The name of the author to 
            filter by.
            alias (Optional[str]): The alias of the author 
            to filter by.
            birthday (Optional[str]): The birthday of the
            uthor to filter by.
            page_size (Optional[int]): The maximum number
            of results to return. Defaults to 100.
            start_index (Optional[int]): The index of the
            first result to return. Defaults to 0.

        Returns:
            List[Author]: A list of authors that match the
            given filters and pagination settings.
        """
        return self.author_repository.list(
            name, alias, birthday, page_size, start_index
        )

    def get(self, author_id: int) -> Optional[Author]:
        """
        Retrieves a specific author by ID, including related
        animes and episodes.

        Args:
            author_id (int): The ID of the author to retrieve.

        Returns:
            Author: The author with the given ID, including
            related animes and episodes.
        """
        author = self.author_repository.get(author_id=author_id)
        if not author:
            raise HTTPException(status_code=404,
                                detail="Author not found")
        return author

    def create(self, author_body: AuthorSchema) -> Author:
        """
        Creates a new author in the database.

        Args:
            author_body (AuthorSchema): The data of the author
            to create.

        Returns:
            Author: The created author with the assigned ID.
        """
        return self.author_repository.create(
            Author(name=author_body.name,
                   alias=author_body.alias,
                   birthday=author_body.birthday))

    def update(self,
               author_id: int,
               author_body: AuthorSchema) -> Author:
        """
        Updates an existing author in the database with the
        provided data.

        Args:
            author_id (int): The ID of the author to update.
            author_body (AuthorSchema): The updated data of
            the author.

        Returns:
            Author: The updated author with the new data.
        """
        return self.author_repository.update(
            author_id,
            Author(name=author_body.name,
                   alias=author_body.alias,
                   birthday=author_body.birthday))

    def delete(self, author_id: int) -> None:
        """
        Deletes an existing author in the database with
        the given ID.

        Args:
            author_id (int): The ID of the author to delete.
        """
        return self.author_repository.delete(author_id)

    def get_animes(self, author_id: int) -> List[Anime]:
        """
        Retrieves the list of animes associated with a specific
        author.

        Args:
            author_id (int): The ID of the author.

        Returns:
            List[Anime]: A list of animes associated with the
            author.
        """
        return self.author_repository.get(author_id).animes

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
        return self.author_repository.get(author_id).episodes
