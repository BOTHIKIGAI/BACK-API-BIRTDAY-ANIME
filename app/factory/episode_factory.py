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
        return Episode(anime_id = episode_body.anime_id,
                       arc = episode_body.arc,
                       temp = episode_body.temp,
                       name = episode_body.temp,
                       episode = episode_body.episode,
                       air_date = episode_body.air_date)
