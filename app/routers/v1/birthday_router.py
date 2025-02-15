"""
This module contains the path to consult the
coincidence of a date with anime, episodes and authors.
"""

from datetime import date
from typing import List

from fastapi import APIRouter, Depends, status

from app.schemas.anime_schema import AnimeSchemaResponse
from app.schemas.author_schema import AuthorSchema
from app.schemas.birthday_schema import BirthdaySchemaResponse
from app.services.birthday_service import BirthdayService


BirthdayRouter = APIRouter()


@BirthdayRouter.get(
    "/{target_date}",
    response_model=BirthdaySchemaResponse,
    status_code=status.HTTP_200_OK,
)
def get_match(target_date: date, birthday_service: BirthdayService = Depends()):
    """
    Get the match for a given date with anime, authors, and episodes.

    Args:
        target_date (date): The date to match against.
        birthday_service (BirthdayService): The service to handle birthday-related operations.

    Returns:
        BirthdaySchemaResponse: The response containing matched anime, authors, and episodes.
    """
    return birthday_service.match_date(target_date)


@BirthdayRouter.get(
    "/{target_date}/author",
    response_model=List[AuthorSchema],
    status_code=status.HTTP_200_OK,
)
def get_match_author(target_date: date, birthday_service: BirthdayService = Depends()):
    """
    Get the authors whose birthdays match the given date.

    Args:
        target_date (date): The date to match against.
        birthday_service (BirthdayService): The service to handle birthday-related operations.

    Returns:
        List[AuthorSchema]: A list of authors with matching birthdays.
    """
    return birthday_service.author_match_date(target_date)


@BirthdayRouter.get(
    "/{target_date}/anime",
    response_model=List[AnimeSchemaResponse],
    status_code=status.HTTP_200_OK,
)
def get_match_anime(target_date: date, birthday_service: BirthdayService = Depends()):
    """
    Get the anime whose release dates match the given date.

    Args:
        target_date (date): The date to match against.
        birthday_service (BirthdayService): The service to handle birthday-related operations.

    Returns:
        List[AnimeSchema]: A list of anime with matching release dates.
    """
    return birthday_service.anime_match_date(target_date)


@BirthdayRouter.get(
    "/{target_date}/episode", response_model=int, status_code=status.HTTP_200_OK
)
def get_match_episode(target_date: date, birthday_service: BirthdayService = Depends()):
    """
    Get the number of episodes released on the given date.

    Args:
        target_date (date): The date to match against.
        birthday_service (BirthdayService): The service to handle birthday-related operations.

    Returns:
        int: The number of episodes released on the matching date.
    """
    return birthday_service.episode_match_date(target_date)
