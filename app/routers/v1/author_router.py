"""
This module contains the routes for the management
of the authors 
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, status
from app.schemas.author_schema import AuthorSchema, AuthorAnimeRelationSchema
from app.schemas.anime_schema import AnimeSchema
from app.schemas.episode_schema import EpisodeSchema
from app.services.author_service import AuthorService

AuthorRouter = APIRouter()

@AuthorRouter.get('/', response_model = List[AuthorSchema])
def index(
    author_service: AuthorService = Depends(),
    name: Optional[str] = None,
    alias: Optional[str] = None,
    birthday: Optional[str] = None,
    page_size: Optional[int] = 100,
    start_index: Optional[int] = 0):
    """
    Retrieves a list of authors based on the provided filters.

    Args:
        author_service (AuthorService): The service to handle author operations.
        name (Optional[str]): Filter by author name.
        alias (Optional[str]): Filter by author alias.
        birthday (Optional[str]): Filter by author birthday.
        page_size (Optional[int]): Number of authors to retrieve.
        start_index (Optional[int]): Starting index for pagination.

    Returns:
        List[AuthorSchema]: A list of authors matching the filters.
    """
    return author_service.list(
        name = name,
        alias = alias,
        birthday = birthday,
        page_size = page_size,
        start_index = start_index)


@AuthorRouter.get('/{author_id}', response_model = AuthorSchema)
def get(author_id: int, author_service: AuthorService = Depends()):
    """
    Retrieves an author by their ID.

    Args:
        author_id (int): The ID of the author to retrieve.
        author_service (AuthorService): The service to handle author operations.

    Returns:
        AuthorSchema: The author with the specified ID.
    """
    return author_service.get(author_id)


@AuthorRouter.post('/', response_model = AuthorSchema, status_code = status.HTTP_201_CREATED)
def create(author: AuthorSchema, author_service: AuthorService = Depends()):
    """
    Creates a new author.

    Args:
        author (AuthorSchema): The author data to create.
        author_service (AuthorService): The service to handle author operations.

    Returns:
        AuthorSchema: The created author.
    """
    return author_service.create(author)


@AuthorRouter.put("/{author_id}", response_model = AuthorSchema)
def update(author_id: int, author: AuthorSchema, author_service: AuthorService = Depends()):
    """
    Updates an existing author.

    Args:
        author_id (int): The ID of the author to update.
        author (AuthorSchema): The new author data.
        author_service (AuthorService): The service to handle author operations.

    Returns:
        AuthorSchema: The updated author.

    Raises:
        HTTPException: If the author is not found.
    """
    return author_service.update(author_id, author)


@AuthorRouter.delete('/{author_id}', status_code = status.HTTP_204_NO_CONTENT)
def delete(author_id: int, author_service: AuthorService = Depends()):
    """
    Deletes an author by their ID.

    Args:
        author_id (int): The ID of the author to delete.
        author_service (AuthorService): The service to handle author operations.

    Returns:
        AuthorSchema: The deleted author.

    Raises:
        HTTPException: If the author is not found.
    """
    author_service.delete(author_id)


@AuthorRouter.get('/{author_id}/anime', response_model = List[AnimeSchema])
def get_anime(author_id: int, author_service: AuthorService = Depends()):
    """
    Get anime author by their ID.

    Args:
        author_id (int): The id of the author to get their anime
        author_service (AuthorService): The service to handle author operations.

    Returns:
        AnimeSchema: The anime author
    """
    return author_service.get_anime(author_id)


@AuthorRouter.post('/{author_id}/anime/{anime_id}',
                   response_model = AuthorAnimeRelationSchema,
                   status_code = status.HTTP_201_CREATED)
def create_anime_relation(author_id: int,
                          anime_id: int,
                          author_service: AuthorService = Depends()):
    """
    Creates a relationship between an author and an anime.

    Args:
        author_id (int): The ID of the author.
        anime_id (int): The ID of the anime.
        author_service (AuthorService): The service to handle author operations.

    Returns:
        AnimeAuthorRelationSchema: The created relationship data.
    """
    return author_service.create_anime_relation(author_id = author_id,
                                                anime_id = anime_id)


@AuthorRouter.get('/{author_id}/episodes', response_model = List[EpisodeSchema])
def get_episodes(author_id: int, author_service: AuthorService = Depends()):
    """
    Get episodes author by their ID.

    Args:
        author_id (int): The id of the author to get their episodes
        author_service (AuthorService): The service to handle author operations.

    Returns:
        EpisodeSchema: The episode author
    """
    return author_service.get_episodes(author_id)
