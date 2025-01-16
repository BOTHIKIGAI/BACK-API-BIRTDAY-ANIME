"""
This module represents the abstraction
of the Episode's data access logic.
"""

from typing import List, Optional
from fastapi import Depends
from sqlalchemy.orm import Session, lazyload
from app.config.database import get_db_connection
from app.models.tables.episode_models import Episode

class EpisodeRepository:
    """
    Repository class for accessing Episode
    data.
    
    This class provides methods to interact
    with the Episode table in the database,
    incluiding listing episode with optional
    filters, and retrieving a specific anime
    by ID with related author and episodes.
    
    Attributes:
        db (Session): The database session
                      used for queryng the
                      database.
    """
    
    # Attributes
    db: Session
    
    # Constructor
    def __init__(self,
                 db: Session = Depends(get_db_connection)) -> None:
        """
        Initializes the EpisodeRepository with
        a database session.
        
        Args:
            db (Session): The database session
            used for queryng the database.
        """
        self.db = db
    
    # Methods
    def list(self,
             arc: Optional[str],
             temp: Optional[int],
             name: Optional[str],
             episode: Optional[int],
             air_date: Optional[str],
             limit: Optional[int],
             start: Optional[int]) -> Optional[List[Episode]]:
        """
        Retrieves a list of episodes with optional
        filters for name, category and release
        date and supports pagination.
        
        Args:
            anime (Optional[str]): The name of the
            anime to filter by.
            arc (Optional[str]): The name of the
            arc to filter by.
            temp (Optional[str]): The name of the
            temp to filter by.
            name (Optional[str]): The name of the
            name episode to filter by.
            episode (Optional[int]): The number of
            the episode to filter by.
            air_date (Optional[str]): The air date
            of the episode to filter by.
        
        Returns:
            List[Episode]: A list of episode that
            match the given filters and pagination
            settings.
        """
        
        query = self.db.query(Episode)

        if arc:
            query = query.filter_by(arc)
        
        if temp:
            query = query.filter_by(temp)
        
        if name:
            query = query.filter_by(name)
        
        if episode:
            query = query.filter_by(episode)
        
        if air_date:
            query = query.filter_by(air_date)
        
        return query.offset(start).limit(limit).all()
    
    def get(self, episode_id: int) -> Optional[Episode]:
        """
        Retrieves a specific episode by ID, incluidig
        related author and anime.

        Args:
            episode_id (int): The ID of the episode to
            retrieve.

        Returns:
            Optional[Episode]: The episode with the 
            given ID, incluiding related author
            and anime, or None if no author
            is found.
        """
        return self.db.query(Episode).options(
                lazyload(Episode.anime),
                lazyload(Episode.authors)
            ).filter_by(id=episode_id).first()
    
    def create(self, episode: Episode) -> Episode:
        """
        Creates a new episode in the database
        and return the created Episode.

        Args:
            episode (Episode): The Episode data
            to create.
        
        Returns:
            Episode: The created episode with the
            asigned ID.
        """
        self.db.add(episode)
        self.db.commit()
        self.db.refresh(episode)
        return episode
    
    def update(self,
               episode_id: int,
               episode: Episode) -> Episode:
        """
        Updates an existing episode in the
        database with the provided data and
        returns the update episode.

        Args:
            episode_id (int): The ID of the
            episode to update.
            episode (Episode): The updated
            episode data.

        Returns:
            Episode: The update episode, or None
            if no episode is found with the given
            ID.
        """
        episode.id = episode_id
        self.db.merge(episode)
        self.db.commit()
        return episode

    def delete(self, episode_id: int) -> None:
        """
        Deletes an existing episode in the
        database with the given ID.

        Args:
            epsisode_id (int): The ID of the
            episode to delete.
        """
        episode = self.db.query(Episode).\
                  filter_by(id=episode_id).first()
        self.db.delete(episode)
        self.db.commit()
