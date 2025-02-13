"""
This module represents the abstraction of the
Author's data access logic.
"""

from datetime import date
from typing import List, Optional

from fastapi import Depends
from sqlalchemy.orm import Query, Session

from app.config.database import get_db_connection
from app.models.relationships.episode_author_association import episode_author_association
from app.models.relationships.anime_author_association import anime_author_association
from app.models.tables.author_models import Author
from app.schemas.author_schema import AuthorAnimeRelationSchema


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


    def get(self, author_id: int) -> Author:
        """
        Retrieves a specific author by ID, including
        related anime and episodes.

        Args:
            author_id (int): The ID of the author to
            retrieve.

        Returns:
            Author: The author with the given ID,
            including related anime and episodes, or None
            if no author is found.
        """
        return self.db.query(Author).filter_by(id=author_id).first()


    def get_by_anime(self, anime_id: int) -> List[Author]:
        """
        Retrieve a list of authors associated with a specific anime.

        This method queries the database to join the Author table with the anime-author
        association table and filters the results based on the provided anime ID.

        Args:
            anime_id (int): The ID of the anime for which to retrieve associated authors.

        Returns:
            List[Author]: A list of Author instances linked to the specified anime.
        """
        query = self.db.query(Author).join(
            anime_author_association,
            Author.id == anime_author_association.c.author_id,
        ).filter(anime_author_association.c.anime_id == anime_id)
        return query.all()


    def get_by_episode(self, episode_id: int) -> List[Author]:
        """
        Retrieve authors associated with a given episode.

        This method queries the database to find all Author instances linked to the specified
        episode. It performs a join on the episode_author_association table using the author ID
        and then filters the results based on the provided episode ID.

        Args:
            episode_id (int): The unique identifier of the episode for which authors are retrieved.

        Returns:
            List[Author]: A list of Author objects associated with the given episode.
        """
        query = self.db.query(Author).join(
            episode_author_association,
            Author.id == episode_author_association.c.author_id,
        ).filter(episode_author_association.c.episode_id == episode_id)
        return query.all()


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


    def update(self, author: Author) -> Author:
        """
        Updates an existing author in the database with
        the provided data and returns the updated author.

        Args:
            author_id (int): The ID of the author to update.
            author (Author): The updated author data.

        Returns:
            Author: The updated author, or None
            if no author is found with the given ID.
        """
        self.db.merge(author)
        self.db.commit()
        return author


    def delete(self, author_id: int) -> None:
        """
        Deletes an existing author in the database with
        the given ID.

        Args:
            author_id (int): The ID of the author to delete.
        """
        author = self.db.query(Author).filter_by(id = author_id).first()
        self.db.delete(author)
        self.db.commit()


    def create_anime_relation(
        self,
        data_relation: AuthorAnimeRelationSchema
    ) -> AuthorAnimeRelationSchema:
        """
        Creates a relationship between an author and an anime.

        Args:
            data_relation (AuthorAnimeRelationSchema): Scheme with author and episode ids

        Returns:
            dict: A dictionary containing the author_id and anime_id.
        """

        insert_statement  = anime_author_association.insert().\
            values(
                author_id = data_relation.author_id,
                anime_id = data_relation.anime_id
            )
        self.db.execute(insert_statement)
        self.db.commit()
        return data_relation


    def has_relationship_with_anime(self, data_relation: AuthorAnimeRelationSchema) -> bool:
        """
        Checks if the relationship between the author and anime exists.

        Args:
            data_relation (AuthorAnimeRelationSchema): Scheme with author and episode ids

        Returns:
            bool: True if the relationship exists, False otherwise.
        """
        query = self.db.query(anime_author_association).\
            filter(
                anime_author_association.c.author_id == data_relation.author_id,
                anime_author_association.c.anime_id == data_relation.anime_id
            )
        return self.db.query(query.exists()).scalar()


    def exists_by_id(self, author_id: int) -> bool:
        """
        Checks if the author exists by means of the author ID.

        Args:
            author_id (int): The ID of the author to check.

        Returns:
            bool: True if the author exists, False otherwise.
        """
        query = self.db.query(Author).filter(Author.id == author_id)
        return self.db.query(query.exists()).scalar()


    def is_related_to_animes(self, author_id: int) -> bool:
        """
        Checks if the author is related to any anime.

        Args:
            author_id (int): The ID of the author to check.

        Returns:
            bool: True if the author is related to any anime, False otherwise.
        """
        query = self.db.query(Author).filter(Author.id == author_id).join(Author.anime)
        return self.db.query(query.exists()).scalar()


    def is_related_to_episodes(self, author_id: int) -> bool:
        """
        Checks if the author is related to any anime.

        Args:
            author_id (int): The ID of the author to check.

        Returns:
            bool: True if the author is related to any episode, False otherwise.
        """
        query = self.db.query(Author).filter(Author.id == author_id).join(Author.episodes)
        return self.db.query(query.exists()).scalar()


    def is_name_taken_for_create(self, author_name: str) -> bool:
        """
        Checks if the given author name already exists in the database.

        Args:
            author_name (str): The name of the author to check.

        Returns:
            bool: True if the name is taken, False otherwise.
        """
        query = self.query_is_name_taken(author_name)
        return self.db.query(query.exists()).scalar()


    def is_name_taken_for_update(self, exclude_id: int, author_name: str) -> bool:
        """
        Checks if the given author name already exists in the database,
        excluding the current author.

        Args:
            exclude_id (int): The ID of the current author.
            author_name (str): The name of the author to check.

        Returns:
            bool: True if the name is taken, False otherwise.
        """
        query = self.query_is_name_taken(author_name).filter(Author.id != exclude_id)
        return self.db.query(query.exists()).scalar()


    def get_by_birthday(self, target_date: date) -> List[Author]:
        """
        Retrieves all authors whose birthday matches the specified date.

        This method queries the database to find authors with a birthday
        that exactly matches the provided date.

        Args:
            target_date (date): The date to match against authors' birthdays.

        Returns:
            List[Author]: A list of Author instances whose birthday matches
            the specified date.
        """
        query = self.db.query(Author).filter(Author.birthday == target_date)
        return query.all()


    # Query base
    def query_is_name_taken(self, author_name: str) -> Query:
        """
        Base query to check if an author name is taken.

        Args:
            author_name (str): The name of the author to check.

        Returns:
            Query: The query object to check if the name is taken.
        """
        return self.db.query(Author).filter(Author.name == author_name)
