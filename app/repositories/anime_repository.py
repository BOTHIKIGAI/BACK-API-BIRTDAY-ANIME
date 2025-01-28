"""
This module represents the abstraction of the
Anime's data access logic.
"""

from typing import List, Optional
from fastapi import Depends
from sqlalchemy.orm import Session, lazyload
from app.config.database import get_db_connection
from app.models.tables.anime_models import Anime

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
            query = query.filter_by(name = name)

        if category:
            query = query.filter_by(category = category)

        if release_date:
            query = query.filter_by(release_date = release_date)

        return query.offset(start).limit(limit).all()


    def get(self, anime_id: int) -> Optional[Anime]:
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
        return self.db.query(Anime).options(
            lazyload(Anime.authors),
            lazyload(Anime.episodes)).filter_by(id = anime_id).first()


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


    def update(self, anime_id: int, anime: Anime) -> Anime:
        """
        Updates an existing anime in the database with the
        provided data and returns the update anime.

        Args:
            anime_id (int): The ID of the anime to update.
            anime (Anime): The updated anime data

        Returns:
            Anime: The update anime, or None if no anime is
            found with the given ID.
        """
        anime.id = anime_id
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


    def exists(self, anime_id: int) -> bool:
        """
        Check if the anime exists by means of the anime id.

        Args:
            anime_id(int): The id of the anime to consult.

        Returns:
            Returns query state.
        """
        query = self.db.query(Anime).filter(Anime.id == anime_id)
        return self.db.query(query.exists()).scalar()


    def name_exists(self, anime_name: str) -> bool:
        """
        Check if the given anime name already exists in
        the database.

        Args:
            name (str): The name of the anime to check.

        Returns:
            bool: True if the name is unique, False otherwise.
        """
        query = self.db.query(Anime).filter(Anime.name == anime_name)
        return self.db.query(query.exists()).scalar()
