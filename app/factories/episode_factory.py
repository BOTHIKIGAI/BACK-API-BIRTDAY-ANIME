"""
This module the factory for episode.
"""

from app.models.tables.episode_models import Episode
from app.schemas.episode_schema import EpisodeSchema


class EpisodeFactory:
    """
    Creates an Episode instance from an EpisodeSchema.

    Args:
        episode_body (EpisodeSchema): The schema
        containing the episode data.

    Returns:
        Episode: The created Episode instance.
    """

    @staticmethod
    def create(episode_body: EpisodeSchema) -> Episode:
        return Episode(
            anime_id=episode_body.anime_id,
            arc=episode_body.arc,
            season=episode_body.season,
            name=episode_body.name,
            episode=episode_body.episode,
            air_date=episode_body.air_date,
        )


    @staticmethod
    def create_for_update(episode_id: int, episode_body: EpisodeSchema) -> Episode:
        return Episode(
            id=episode_id,
            anime_id=episode_body.anime_id,
            arc=episode_body.arc,
            season=episode_body.season,
            name=episode_body.name,
            episode=episode_body.episode,
            air_date=episode_body.air_date,
        )
