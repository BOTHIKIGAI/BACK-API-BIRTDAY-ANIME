"""
This module represents the abstraction of the 
Author's data access logic.
"""

from typing import List, Optional
from fastapi import Depends
from sqlalchemy.orm import Session, lazyload
from app.config.database import get_db_connection
from app.models.tables.author_models import Author

class AuthorRepository:
    """
    Repository class for accessing Author data.

    This class provides methods to interact with
    the Author table in the database, including
    listing authors with optional filters, and
    retrieving a specific author by ID with 
    related animes and episodes.

    Attributes:
        db (Session): The database session used
                      for querying the database.

    Methods:
        list(
            name: Optional[str],
            alias: Optional[str],
            birthday: Optional[str],
            limit: Optional[int],
            start: Optional[int]) -> List[Author]:
                Retrieves a list of authors with
                optional filters for name, alias,
                and birthday, and supports pagination.
        
        get(author_id: int) -> Optional[Author]:
            Retrieves a specific author by ID, 
            including related animes and episodes.

        create(author: Author) -> Author:
            Returns the author created with his data

        update(author_id: int, author: Author) -> Author:
            Update an existing author in the
            database with the provided data
            and returns the update authors.
        
        delete(self, author: Author) -> None:
            Delete an existing author in the
            database with the id author.
    """

    # Attributes
    db: Session

    def __init__(self,
                 db: Session = Depends(get_db_connection)) -> None:
        """
        Initializes the AuthorRepository with 
        a database session.

        Args:
            db (Session): The database session
            used for querying the database.
        """
        self.db = db

    # Methods

    def list(self,
             name: Optional[str],
             alias: Optional[str],
             birthday: Optional[str],
             limit: Optional[int],
             start: Optional[int]) -> Optional[List[Author]]:
        """
        Retrieves a list of authors with optional
        filters for name, alias, and birthday, and
        supports pagination.

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
            query = query.filter_by(name=name)

        if alias:
            query = query.filter_by(alias=alias)

        if birthday:
            query = query.filter_by(birthday=birthday)

        return query.offset(start).limit(limit).all()

    def get(self, author_id: int) -> Optional[Author]:
        """
        Retrieves a specific author by ID, including
        related animes and episodes.

        Args:
            author_id (int): The ID of the author to
            retrieve.

        Returns:
            Optional[Author]: The author with the given
            ID, including related animes and episodes,
            or None if no author is found.
        """
        return self.db.query(Author).options(
            lazyload(Author.animes),
            lazyload(Author.episodes)
        ).filter_by(id=author_id).first()

    def create(self, author: Author) -> Author:
        """
        Creates a new author in the database and returns
        the created author.

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
        author = self.db.query(Author).filter_by(id=author_id).first()
        self.db.delete(author)
        self.db.commit()
