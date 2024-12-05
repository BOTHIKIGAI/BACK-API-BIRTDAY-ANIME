"""
This module contains the routes for the management }
of the authors 
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, status, HTTPException
from app.schemas.author_schema import AuthorSchema
from app.schemas.anime_schema import AnimeSchema
from app.schemas.episode_schema import EpisodeSchema
from app.services.author_service import AuthorService

AuthorRouter = APIRouter(
    tags=["Author"],
    prefix='/v1/authors')

@AuthorRouter.get('/', response_model=List[AuthorSchema])
def list(
    author_service: AuthorService = Depends(),
    name: Optional[str] = None,
    alias: Optional[str] = None,
    birthday: Optional[str] = None,
    page_size: Optional[int] = 100,
    start_index: Optional[int] = 0):

    return author_service.list(
            name, alias, birthday, page_size, start_index)

@AuthorRouter.get('/{author_id}',
                  response_model=AuthorSchema)
def get(author_id: int, author_service: AuthorService = Depends()):
    author = author_service.get(author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author

@AuthorRouter.post('/',
                   response_model=AuthorSchema,
                   status_code=status.HTTP_201_CREATED)
def create(author: AuthorSchema,
           author_service: AuthorService = Depends()):
    return author_service.create(author)

@AuthorRouter.put("/{author_id}",
                  response_model=AuthorSchema)
def update(author_id: int,
           author: AuthorSchema,
           author_service: AuthorService = Depends()):
    return author_service.update(author_id, author)

@AuthorRouter.delete('/{author_id}',
                     response_model=AuthorSchema)
def delete(author_id: int, author_service: AuthorService = Depends()):
    return author_service.delete(author_id)
