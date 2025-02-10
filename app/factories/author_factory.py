"""
This module the factory for author
"""

from app.models.tables.author_models import Author
from app.schemas.author_schema import AuthorAnimeRelationSchema, AuthorSchema


class AuthorFactory:
    """
    Creates an Author instance from an AuthorSchema.

    Args:
        author_body (AuthorSchema): The schema containing the author data.

    Returns:
        Author: The created Author instance.
    """

    @staticmethod
    def create(author_body: AuthorSchema) -> Author:
        return Author(
            name=author_body.name,
            alias=author_body.alias,
            birthday=author_body.birthday,
        )

    @staticmethod
    def create_for_update(author_id: int, author_body: AuthorSchema) -> Author:
        return Author(
            id=author_id,
            name=author_body.name,
            alias=author_body.alias,
            birthday=author_body.birthday,
        )


class AuthorAnimeFactory:
    """
    A factory class for creating a dictionary representation of an author-anime relationship.

    This class provides a static method to convert an instance of
    AuthorAnimeRelationSchema into a dictionary containing the author and anime identifiers.

    Methods:
        create(data_relation: AuthorAnimeRelationSchema) -> dict:
            Converts the given data_relation into a dictionary with keys 'author_id'
            and 'anime_id'.
    """
    @staticmethod
    def create(data_relation: AuthorAnimeRelationSchema) -> dict:
        return {
            "author_id": data_relation.author_id,
            "anime_id": data_relation.anime_id,
        }
