"""
This module contains the routes for the
management of the anime
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, status
from app.schemas.episode_schema import EpisodeSchema, EpisodeAuthorRelationSchema
from app.services.episode_service import EpisodeService

EpisodeRouter = APIRouter()

@EpisodeRouter.get('/', response_model = List[EpisodeSchema])
def index(
    episode_service: EpisodeService = Depends(),
    arc: Optional[str] = None,
    temp: Optional[int] = None,
    name: Optional[str] = None,
    episode: Optional[int] = None,
    air_date: Optional[str] = None,
    page_size: Optional[int] = 100,
    start_index: Optional[int] = None):
    """
    Retrieves a list of episodes based
    on the provided filters.

    Args:
        episode_service (EpisodeService): The service to handle episode operations.
        arc (Optional[str]): Filter by episode arc.
        temp (Optional[int]): Filter by episode temp.
        name (Optional[str]): Filter by name.
        episode (Optional[int]): Filter by episode number.
        air_date (Optional[str]): Filter by episode air_date.
        page_size (Optional[int]): Number of authors to retrieve.
        start_index (Optional[int]): Starting index for pagination.

    Returns:
        List[EpisodeSchema]: A list of episode matching the filters.
    """
    return episode_service.list(
        arc = arc,
        temp = temp,
        name = name,
        episode = episode,
        air_date = air_date,
        page_size = page_size,
        start_index = start_index
    )


@EpisodeRouter.get('/{episode_id}', response_model = EpisodeSchema)
def get(episode_id: int, episode_service: EpisodeService = Depends()):
    """
    Retrieves an episode by their ID.

    Args:
        episode_id (int): The ID of the episode to retrieve.
        episode_service (EpisodeService): The service to handle episode operations.

    Returns:
        EpisodeSchema: The episode with the specified ID.
    """
    return episode_service.get(episode_id)


@EpisodeRouter.post('/', response_model = EpisodeSchema, status_code = status.HTTP_201_CREATED)
def create(episode: EpisodeSchema, episode_service: EpisodeService = Depends()):
    """
    Creates a new episode.

    Args:
        episode (EpisodeSchema): The episode data to create.
        episode_service (EpisodeService): The service to handle episode operations.

    Returns:
        EpisodeSchema: The created episode.
    """
    return episode_service.create(episode)


@EpisodeRouter.put('/{episode_id}', response_model = EpisodeSchema)
def update(episode_id: int, episode: EpisodeSchema, episode_service: EpisodeService = Depends()):
    """
    Updates an existing episode.

    Args:
        episode_id (int): The ID of the episode to update.
        episode (EpisodeSchema): The new episode data.
        episode_service (EpisodeService): The service to handle episode operations.

    Returns:
        EpisodeSchema: The updated episode.

    Raises:
        HTTPException: If the episode is not found.
    """
    return episode_service.update(episode_id = episode_id, episode_body = episode)


@EpisodeRouter.delete('/{episode_id}', status_code = status.HTTP_204_NO_CONTENT)
def delete(episode_id: int, episode_service: EpisodeService = Depends()):
    """
    Deletes an episode by their ID.

    Args:
        episode_id (int): The ID of the episode to delete.
        episode_service (EpisodeService): The service to handle episode operations.

    Returns:
        EpisodeSchema: The deleted episode.

    Raises:
        HTTPException: If the episode is not found.
    """
    return episode_service.delete(episode_id)


@EpisodeRouter.get('/{episode_id}/anime')
def get_anime(episode_id: int, episode_service: EpisodeService = Depends()):
    """
    Get anime by their episode ID.

    Args:
        episode_id (int): The id of the episode to get their episode.
        episode_service (EpisodeService): The service to handle author operations.

    Returns:
        AnimeSchema: The episode anime
    """
    return episode_service.get_anime(episode_id)


@EpisodeRouter.get('/{episode_id}/authors')
def get_author(episode_id: int, episode_service: EpisodeService = Depends()):
    """
    Get author/s episode by their ID.

    Args:
        episode_id (int): The id of the episode to get their author/s
        episode_service (EpisodeService): The service to handle episode operations.

    Returns:
        AuthorSchema: The episode author
    """
    return episode_service.get_author(episode_id)


@EpisodeRouter.post('/{episode_id}/author/{author_id}',
                    response_model = EpisodeAuthorRelationSchema,
                    status_code = status.HTTP_201_CREATED)
def create_author_relation(episode_id: int,
                           author_id: int,
                           episode_service: EpisodeService = Depends()):
    """
    Creates a relationship between an episode and an author.

    Args:
        episode_id (int): The ID of the episode.
        author_id (int): The ID of the author.
        episode_service (EpisodeService): The service to
        handle episode operations.

    Returns:
        EpisodeAuthorRelationSchema: The created relationship
        data.
    """
    return episode_service.create_author_relation(episode_id = episode_id,
                                                  author_id = author_id)
