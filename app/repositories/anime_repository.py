"""
This module represents the abstraction of the
Anime's data access logic.
"""
from typing import List, Optional

from fastapi import Depends
from sqlalchemy.orm import Query, Session

from app.config.database import get_db_connection
from app.models.relationships.anime_author_association import anime_author_association
from app.models.tables.anime_models import Anime
from app.models.tables.episode_models import Episode


class AnimeRepository:
    """
    Repository class fot accessing Anime data.

    This class provides methods to interact with the Anime table
    in the database, including listing anime with optional
    filters, and retrieving a specific anime by ID with related
    author and episodes.

    Attributes:
        db (Session): The database session used for querying the
        database.
    """

    # Attributes
    db: Session


    # Constructor
    def __init__(self, db: Session = Depends(get_db_connection)) -> None:
        """
        Initializes the AnimeRepository with a database session.

        Args:
            db (Session): The database session used for querying
            the database.
        """
        self.db = db


    # Methods
    def list(self,
             name: Optional[str],
             category: Optional[str],
             release_date: Optional[str],
             limit: Optional[int],
             start: Optional[int]) -> List[Anime]:
        """
        Retrieves a list of anime with optional filters for name,
        category and release date and supports pagination.

        Args:
            name (Optional[str]): The name of the anime to filter by.
            category (Optional[str]): The name of category to filter by.
            release_date (Optional[str]): The release date of the
            anime to filter by.
            limit (Optional[int]): The maximum number of results to return.
            start (Optional[int]): The index of the first result to return.

        Returns:
            List[Anime]: A list of authors that match the given filters and
            pagination settings.
        """

        query = self.db.query(Anime)

        if name:
            query = query.filter_by(name=name)

        if category:
            query = query.filter_by(category=category)

        if release_date:
            query = query.filter_by(release_date=release_date)

        return query.offset(start).limit(limit).all()


    # CRUD Methods
    def get(self, anime_id: int) -> Anime:
        """
        Retrieves a specific anime by ID, include related author
        and episodes.

        Args:
            anime_id (int): The ID of the anime to retrieve.

        Returns:
            Optional[Anime]: The anime with the given ID,
            including related author and episodes, or
            None if no author is found.
        """
        return self.db.query(Anime).filter_by(id=anime_id).first()


    def get_by_author(self, author_id: int) -> List[Anime]:
        """
        Retrieves a list of Anime associated with a given author.

        This function performs a join between the Anime table and the anime_author_association
        table, filtering the results by the specified author_id. It returns all Anime records
        that are related to the provided author identifier.

        Args:
            author_id (int): The unique identifier of the author whose animes are to be retrieved.

        Returns:
            List[Anime]: A list of Anime objects associated with the author. Returns an empty list
                         if no associations exist.
        """
        query = self.db.query(Anime).join(
            anime_author_association,
            Anime.id == anime_author_association.c.anime_id
        ).filter(anime_author_association.c.author_id == author_id)
        return query.all()


    def get_by_episode(self, episode_id: int) -> Anime:
        """
        Retrieve the Anime associated with a given episode.

        This method performs a join between the Anime and Episode tables and filters
        the result using the provided episode ID. It returns the first matching Anime
        instance found.

        Args:
            episode_id (int): The unique identifier of the episode.

        Returns:
            Anime: The first Anime instance associated with the given episode ID,
                    or None if no such Anime exists.
        """
        query = self.db.query(Anime).join(
            Episode,
            Anime.id == Episode.id
        ).filter(Episode.id == episode_id)
        return query.first()


    def create(self, anime: Anime) -> Anime:
        """
        Creates a new anime in the database and return the created Anime.

        Args:
            anime (Anime): The Anime data to create.

        Returns:
            Anime: The created anime with the assigned ID.
        """
        self.db.add(anime)
        self.db.commit()
        self.db.refresh(anime)
        return anime


    def update(self, anime: Anime) -> Anime:
        """
        Updates an existing anime in the database with the provided data and returns
        the update anime.

        Args:
            anime (Anime): The updated anime data

        Returns:
            Anime: The update anime, or None if no anime is found with the given ID.
        """
        self.db.merge(anime)
        self.db.commit()
        return anime


    def delete(self, anime_id: int) -> None:
        """
        Deletes an existing anime in the database with the
        given ID.

        Args:
            anime_id (int): The ID of the anime to delete
        """
        anime = self.db.query(Anime).filter_by(id = anime_id).first()
        self.db.delete(anime)
        self.db.commit()


    # Operations Methods
    def exists_by_id(self, anime_id: int) -> bool:
        """
        Checks if the anime exists by means of the anime ID.

        Args:
            anime_id (int): The ID of the anime to check.

        Returns:
            bool: True if the anime exists, False otherwise.
        """
        query = self.db.query(Anime).filter(Anime.id==anime_id)
        return self.db.query(query.exists()).scalar()


    def is_related_to_episode(self, anime_id: int) -> bool:
        """
        Checks if the anime is related to any episode.

        Args:
            anime_id (int): The ID of the anime to check.

        Returns:
            bool: True if the anime is related to any episode, False otherwise.
        """
        query = self.db.query(Anime).filter(Anime.id == anime_id).join(Anime.episodes)
        return self.db.query(query.exists()).scalar()


    def is_name_taken_for_create(self, anime_name: str) -> bool:
        """
        Checks if the given anime name already exists in the database.

        Args:
            anime_name (str): The name of the anime to check.

        Returns:
            bool: True if the name is taken, False otherwise.
        """
        query = self.is_name_taken(anime_name)
        return self.db.query(query.exists()).scalar()


    def is_name_taken_for_update(self, exclude_id: int, anime_name: str) -> bool:
        """
        Checks if the given anime name already exists in the database,
        excluding the current anime.

        Args:
            exclude_id (int): The ID of the current anime.
            anime_name (str): The name of the anime to check.

        Returns:
            bool: True if the name is taken, False otherwise.
        """
        query = self.is_name_taken(anime_name).filter(Anime.id != exclude_id)
        return self.db.query(query.exists()).scalar()


    # Base Query
    def is_name_taken(self, anime_name: str) -> Query:
        """
        Base query to check if an anime name is taken.

        Args:
            anime_name (str): The name of the anime to check.

        Returns:
            Query: The query object to check if the name is taken.
        """
        return self.db.query(Anime).filter(Anime.name == anime_name)
