"""
This module the factory for author
"""
from app.models.tables.author_models import Author
from app.schemas.author_schema import AuthorSchema

class AuthorFactory:
    """
    Creates an Author instance from an AuthorSchema.

    Args:
        author_body (AuthorSchema): The schema
        containing the author data.

    Returns:
        Author: The created Author instance.
    """
    @staticmethod
    def create(author_body: AuthorSchema) -> Author:
        return Author(name = author_body.name,
                      alias = author_body.alias,
                      birthday = author_body.birthday)
