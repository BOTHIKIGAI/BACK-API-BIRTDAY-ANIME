"""
This module represents the abstraction of the 
Author's data access logic.
"""

from typing import List, Optional
from fastapi import Depends
from sqlalchemy.orm import Session, lazyload
from app.config.database import get_db_connection
from app.models.tables.author_models import Author
from app.models.relationships.anime_author_association import anime_author_association

class AuthorRepository:
    """
    Repository class for accessing Author data.

    This class provides methods to interact with the Author table
    in the database, including listing authors with optional filters,
    and retrieving a specific author by ID with related anime and
    episodes.

    Attributes:
        db (Session): The database session used for querying the database.
    """

    # Attributes
    db: Session


    # Constructor
    def __init__(self,
                 db: Session = Depends(get_db_connection)) -> None:
        """
        Initializes the AuthorRepository with a database session.

        Args:
            db (Session): The database session used for querying the database.
        """
        self.db = db


    # Methods
    def list(self,
             name: Optional[str],
             alias: Optional[str],
             birthday: Optional[str],
             limit: Optional[int],
             start: Optional[int]) -> List[Author]:
        """
        Retrieves a list of authors with optional filters for name, alias, and
        birthday, and supports pagination.

        Args:
            name (Optional[str]): The name of the author to filter by.
            alias (Optional[str]): The alias of the author to filter by.
            birthday (Optional[str]): The birthday of the author to filter by.
            limit (Optional[int]): The maximum number of results to return.
            start (Optional[int]): The index of the first result to return.

        Returns:
            List[Author]: A list of authors that match
            the given filters and pagination settings.
        """
        query = self.db.query(Author)

        if name:
            query = query.filter_by(name = name)

        if alias:
            query = query.filter_by(alias = alias)

        if birthday:
            query = query.filter_by(birthday = birthday)

        return query.offset(start).limit(limit).all()


    def get(self, author_id: int) -> Optional[Author]:
        """
        Retrieves a specific author by ID, including
        related anime and episodes.

        Args:
            author_id (int): The ID of the author to
            retrieve.

        Returns:
            Optional[Author]: The author with the given ID,
            including related anime and episodes, or None
            if no author is found.
        """
        return self.db.query(Author).options(
            lazyload(Author.anime),
            lazyload(Author.episodes)).filter_by(id = author_id).first()


    def create(self, author: Author) -> Author:
        """
        Creates a new author in the database and returns the
        created author.

        Args:
            author (Author): The author data to create.

        Returns:
            Author: The created author with the assigned ID.
        """
        self.db.add(author)
        self.db.commit()
        self.db.refresh(author)
        return author


    def update(self, author_id: int, author: Author) -> Author:
        """
        Updates an existing author in the database with
        the provided data and returns the updated author.

        Args:
            author_id (int): The ID of the author to update.
            author (Author): The updated author data.

        Returns:
            Optional[Author]: The updated author, or None
            if no author is found with the given ID.
        """
        author.id = author_id
        self.db.merge(author)
        self.db.commit()
        return author


    def delete(self, author_id: Author) -> None:
        """
        Deletes an existing author in the database with
        the given ID.

        Args:
            author_id (int): The ID of the author to delete.
        """
        author = self.db.query(Author).filter_by(id = author_id).first()
        self.db.delete(author)
        self.db.commit()


    def create_anime_relation(self, author_id: int, anime_id: int):
        """
        Creates a relationship between an author and an anime.

        Args:
            author_id (int): The ID of the author.
            anime_id (int): The ID of the anime.

        Returns:
            dict: A dictionary containing the author_id and anime_id.
        """
        insert_statement  = anime_author_association.insert().values(author_id = author_id,
                                                                     anime_id = anime_id)
        self.db.execute(insert_statement)
        self.db.commit()

        return {"author_id": author_id, "anime_id": anime_id}


    def exists_by_id(self, author_id: int) -> bool:
        """
        Check if the author exists by means of the author id.
        Args:
            author_id(int): The id of the author to consult.

        Returns:
            Returns query state.
        """
        query = self.db.query(Author).filter(Author.id == author_id)
        return self.db.query(query.exists()).scalar()


    def is_related_to_anime(self, author_id: int) -> bool:
        """
        Checks if the author is related to any anime.

        Args:
            author_id (int): The ID of the author to check.

        Returns:
            bool: True if the author is related to any anime, False otherwise.
        """
        query = self.db.query(Author).filter(Author.id == author_id).join(Author.anime)
        return self.db.query(query.exists()).scalar()


    def is_related_to_episode(self, author_id: int) -> bool:
        """
        Checks if the author is related to any anime.

        Args:
            author_id (int): The ID of the author to check.

        Returns:
            bool: True if the author is related to any episode, False otherwise.
        """
        query = self.db.query(Author).filter(Author.id == author_id).join(Author.episodes)
        return self.db.query(query.exists()).scalar()


    def is_name_taken(self, author_name: str) -> bool:
        """
        Check if the given author name already exists in
        the database.

        Args:
            name (str): The name of the author to check.

        Returns:
            bool: True if the author is unique, False otherwise.
        """
        query = self.db.query(Author).filter(Author.name == author_name)
        return self.db.query(query.exists()).scalar()
