"""
Factory module for creating specific repositories based on entity types.
"""
from typing import List
from app.models.tables.anime_models import Anime
from app.models.tables.author_models import Author


class BirthdayFactory:
    """
    Factory class that creates standardized birthday response dictionaries.
    """

    @staticmethod
    def create(
        match_author: List[Author],
        match_anime: List[Anime],
        match_episode: int = 0
    ):
        """
        Creates a standardized response dictionary with birthday matches.

        Args:
            match_author (List[Author]): List of authors matching a specific date
            match_anime (List[Anime]): List of anime matching a specific date
            match_episode (int): Number of episodes matching a specific date. Defaults to 0

        Returns:
            dict: Structured dictionary containing matched entities
        """
        return {
            "anime": match_anime,
            "author": match_author,
            "episode": match_episode
        }
