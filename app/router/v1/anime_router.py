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

@AnimeRouter.get('/',
                 response_model=List[AnimeSchema])
def index(anime_service: AnimeService = Depends(),
          name: Optional[str] = None,
          category: Optional[str] = None,
          release_date: Optional[str] = None,
          page_size: Optional[int] = 100,
          start_index: Optional[int] = 0):
    return anime_service.list(
        name, category, release_date, page_size, start_index)

@AnimeRouter.get('/{anime_id}',
                 response_model=AnimeSchema)
def get(anime_id: int,
        anime_service: AnimeService = Depends()):
    return anime_service.get(anime_id)

@AnimeRouter.post('/',
                  response_model=AnimeSchema,
                  status_code=status.HTTP_201_CREATED)
def create(anime: AnimeSchema,
           anime_service: AnimeService = Depends()):
    return anime_service.create(anime)

@AnimeRouter.put('/{anime_id}')
def update(anime_id: int,
           anime: AnimeSchema,
           anime_service: AnimeService = Depends()):
    return anime_service.update(anime_id, anime)

@AnimeRouter.delete('/{anime_id}',
                    status_code=status.HTTP_204_NO_CONTENT)
def delete(anime_id: int,
           anime_service: AnimeService = Depends()):
    return anime_service.delete(anime_id)

@AnimeRouter.get('/{anime_id}/authors',
                 response_model=List[AuthorSchema])
def get_authors(anime_id: int,
                anime_service: AnimeService = Depends()):
    return anime_service.get_authors(anime_id)

@AnimeRouter.get('/{anime_id}/episodes',
                 response_model=List[EpisodeSchema])
def get_episodes(anime_id: int,
               anime_service: AnimeService = Depends()):
    return anime_service.get_episodes(anime_id)