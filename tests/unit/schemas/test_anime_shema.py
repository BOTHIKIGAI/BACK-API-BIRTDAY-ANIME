"""
This module contains the unit tests for the anime scheme.
"""
from datetime import date

import pytest
from pydantic import ValidationError

from app.schemas.anime_schema import AnimeSchema
from tests.fixtures.schemas.anime_test_data import RELEASE_DATES_NOT_VALID


def test_successful_anime_schema():
    anime_schema = AnimeSchema(
        name="Anime 1",
        category="Category 1",
        release_date=date.fromisoformat("2025-02-13")
    )
    assert isinstance(anime_schema, AnimeSchema)
    assert isinstance(anime_schema.name, str)
    assert isinstance(anime_schema.category, str)
    assert isinstance(anime_schema.release_date, date)


def test_validation_anime_scheme_sanitization():
    anime_schema = AnimeSchema(
        name="Anime with   spaces  and  UPPERCASE",
        category="Category with   spaces  and  UPPERCASE",
        release_date=date.fromisoformat("2025-02-13")
    )
    assert anime_schema.name == "anime with spaces and uppercase"
    assert anime_schema.category == "category with spaces and uppercase"


def test_validation_anime_schema_attribute_data_type_exceptions():
    with pytest.raises(ValidationError) as exc_info:
        AnimeSchema(
            name=1,
            category=1,
            release_date=1
        )
    errors = exc_info.value.errors()
    assert len(errors) == 3
    error_dict = {error['loc'][0]: error['msg'] for error in errors}
    assert '1 is not a string' in error_dict['name']
    assert '1 is not a string' in error_dict['category']
    assert 'Invalid date type' in error_dict['release_date']


@pytest.mark.parametrize(
    "test_case",
    RELEASE_DATES_NOT_VALID.values(),
    ids=RELEASE_DATES_NOT_VALID.keys()
)
def test_validation_anime_schema_release_date_attribute(test_case):
    with pytest.raises(ValidationError) as exc_info:
        AnimeSchema(
            name="Name 1",
            category="Category 2",
            release_date=test_case["release_date"]
        )
    errors = exc_info.value.errors()
    assert any(test_case["error_message"] in error["msg"] for error in errors)
