"""
This module contains the routes for the management
of the anime
"""
from typing import List, Optional

from fastapi import APIRouter, Depends, status

from app.schemas.anime_schema import AnimeSchema
from app.schemas.author_schema import AuthorSchema
from app.schemas.episode_schema import EpisodeSchema
from app.services.anime_service import AnimeService

AnimeRouter = APIRouter()

@AnimeRouter.get('/', response_model = List[AnimeSchema])
def index(anime_service: AnimeService = Depends(),
          name: Optional[str] = None,
          category: Optional[str] = None,
          release_date: Optional[str] = None,
          page_size: Optional[int] = 100,
          start_index: Optional[int] = 0):
    """
    Retrieves a list of anime based on the provided filters.

    Args:
        anime_service (AnimeService): The service to handle anime operations.
        name (Optional[str]): Filter by author name.
        category (Optional[str]): Filter by author category.
        release_date (Optional[str]): Filter by author release_date.
        page_size (Optional[int]): Number of anime to retrieve.
        start_index (Optional[int]): Starting index for pagination.

    Returns:
        List[AnimeSchema]: A list of anime matching the filters.
    """
    return anime_service.list(
        name = name,
        category = category,
        release_date = release_date,
        page_size = page_size,
        start_index = start_index)


@AnimeRouter.get('/{anime_id}', response_model = AnimeSchema)
def get(anime_id: int, anime_service: AnimeService = Depends()):
    """
    Retrieves an anime by their ID.

    Args:
        anime_id (int): The ID of the anime to retrieve.
        anime_service (AnimeService): The service to handle anime operations.

    Returns:
        AnimeSchema: The author with the specified ID.
    """
    return anime_service.get(anime_id)


@AnimeRouter.post('/', response_model = AnimeSchema, status_code = status.HTTP_201_CREATED)
def create(anime: AnimeSchema, anime_service: AnimeService = Depends()):
    """
    Creates a new anime.

    Args:
        anime (AnimeSchema): The anime data to create.
        anime_service (AnimeService): The service to handle anime operations.

    Returns:
    AnimeSchema: The created anime.
    """
    return anime_service.create(anime)


@AnimeRouter.put('/{anime_id}', response_model = AnimeSchema)
def update(anime_id: int, anime: AnimeSchema, anime_service: AnimeService = Depends()):
    """
    Updates an existing anime.

    Args:
        anime_id (int): The ID of the anime to update.
        anime (AnimeSchema): The new anime data.
        anime_service (AnimeService): The service to handle anime operations.

    Returns:
        AnimeSchema: The updated anime.

    Raises:
        HTTPException: If the author is not found.
    """
    return anime_service.update(anime_id, anime)


@AnimeRouter.delete('/{anime_id}', status_code = status.HTTP_204_NO_CONTENT)
def delete(anime_id: int, anime_service: AnimeService = Depends()):
    """
    Deletes an anime by their ID.

    Args:
        anime_id (int): The ID of the anime to delete.
        anime_service (AnimeService): The service to handle anime operations.

    Returns:
        AnimeSchema: The deleted anime.

    Raises:
        HTTPException: If the anime is not found.
    """
    return anime_service.delete(anime_id)


@AnimeRouter.get('/{anime_id}/authors', response_model = List[AuthorSchema])
def get_authors(anime_id: int, anime_service: AnimeService = Depends()):
    """
    Get author anime by their ID.

    Args:
        anime_id (int): The id of the anime to get their authors.
        anime_service (AnimeService): The service to handle anime operations.

    Returns:
        AuthorSchema: The author anime
    """
    return anime_service.get_authors(anime_id)


@AnimeRouter.get('/{anime_id}/episodes', response_model = List[EpisodeSchema])
def get_episodes(anime_id: int, anime_service: AnimeService = Depends()):
    """
    Get anime episodes by their ID.

    Args:
        anime_id (int): The id of the anime to get their episodes.
        anime_service (AnimeService): The service to handle anime operations.

    Returns:
        EpisodeSchema: The anime episode.
    """
    return anime_service.get_episodes(anime_id)
