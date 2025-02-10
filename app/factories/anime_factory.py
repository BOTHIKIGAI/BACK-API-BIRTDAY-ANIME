"""
This module the factory for anime
"""

from app.models.tables.anime_models import Anime
from app.schemas.anime_schema import AnimeSchema


class AnimeFactory:
    """
    Creates an Anime instance from an AnimeSchema.

    Args:
        anime_body (AnimeSchema): The schema containing the anime data.

    Returns:
        Anime: The created Anime instance.
    """

    @staticmethod
    def create(anime_body: AnimeSchema) -> Anime:
        return Anime(
            name=anime_body.name,
            category=anime_body.category,
            release_date=anime_body.release_date,
        )


    @staticmethod
    def create_for_update(anime_id: int, anime_body: AnimeSchema) -> Anime:
        return Anime(
            id=anime_id,
            name=anime_body.name,
            category=anime_body.category,
            release_date=anime_body.release_date,
        )
