"""
This module contains the BirthdayService class, which handles operations
related to matching dates with anime, author, and episode birthdays.
"""

from datetime import date
from typing import List

from fastapi import Depends

from app.factories.birthday_factory import BirthdayFactory
from app.models.tables.anime_models import Anime
from app.models.tables.author_models import Author
from app.repositories.birthday_repository import BirthdayRepository


class BirthdayService:
    """
    Service class for handling birthday-related operations.
    """

    # Attributes
    birthday_repository: BirthdayRepository

    # Constructor
    def __init__(self, birthday_repository: BirthdayRepository = Depends()) -> None:
        """
        Initialize the BirthdayService with a BirthdayRepository.

        Args:
            birthday_repository (BirthdayRepository): The repository to access birthday data.
        """
        self.birthday_repository = birthday_repository

    # Methods
    def match_date(self, target_date: date):
        """
        Match the given date with anime, author, and episode birthdays.

        Args:
            target_date (date): The date to match against.

        Returns:
            dict: A dictionary containing matched anime, authors, and episodes.
        """
        return BirthdayFactory.create(
            match_anime=self.anime_match_date(target_date),
            match_author=self.author_match_date(target_date),
            match_episode=self.episode_match_date(target_date),
        )

    def author_match_date(self, target_date: date) -> List[Author]:
        """
        Get authors whose birthdays match the given date.

        Args:
            target_date (date): The date to match against.

        Returns:
            List[Author]: A list of authors with matching birthdays.
        """
        return self.birthday_repository.get_authors_matching_date(target_date)

    def anime_match_date(self, target_date: date) -> List[Anime]:
        """
        Get anime whose release dates match the given date.

        Args:
            target_date (date): The date to match against.

        Returns:
            List[Anime]: A list of anime with matching release dates.
        """
        return self.birthday_repository.get_animes_matching_date(target_date)

    def episode_match_date(self, target_date: date) -> int:
        """
        Get the number of episodes released on the given date.

        Args:
            target_date (date): The date to match against.

        Returns:
            int: The number of episodes released on the matching date.
        """
        return self.birthday_repository.get_episodes_matching_date(target_date)
