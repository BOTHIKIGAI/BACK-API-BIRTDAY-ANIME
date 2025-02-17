"""
This module the factory for author
"""

from app.models.tables.author_models import Author
from app.schemas.author_schema import AuthorSchemaCreate


class AuthorFactory:
    """
    Creates an Author instance from an AuthorSchema.

    Args:
        author_body (AuthorSchema): The schema containing the author data.

    Returns:
        Author: The created Author instance.
    """

    @staticmethod
    def create(author_body: AuthorSchemaCreate) -> Author:
        return Author(
            name=author_body.name,
            alias=author_body.alias,
            birthday=author_body.birthday,
        )

    @staticmethod
    def create_for_update(author_id: int, author_body: AuthorSchemaCreate) -> Author:
        return Author(
            id=author_id,
            name=author_body.name,
            alias=author_body.alias,
            birthday=author_body.birthday,
        )
