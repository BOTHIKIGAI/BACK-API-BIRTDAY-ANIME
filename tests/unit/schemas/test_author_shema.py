"""
This module contains the unit tests for the anime scheme.
"""
from datetime import date

import pytest
from pydantic import ValidationError

from app.schemas.author_schema import AuthorSchemaCreate, AuthorSchemaResponse
from tests.fixtures.schemas.author_test_data import RELEASE_DATES_NOT_VALID


def test_successful_author_schema_create():
    anime_schema = AuthorSchemaCreate(
        name="Author 1",
        alias="Alias 1",
        birthday="2025-02-13"
    )
    assert isinstance(anime_schema, AuthorSchemaCreate)
    assert isinstance(anime_schema.name, str)
    assert isinstance(anime_schema.alias, str)
    assert isinstance(anime_schema.birthday, date)


def test_successful_author_schema_response():
    anime_schema = AuthorSchemaResponse(
        name="Author 1",
        alias="Alias 1",
        birthday=date.fromisoformat("2025-02-13")
    )
    assert isinstance(anime_schema, AuthorSchemaResponse)
    assert isinstance(anime_schema.name, str)
    assert isinstance(anime_schema.alias, str)
    assert isinstance(anime_schema.birthday, date)



def test_validation_author_scheme_create_sanitization():
    anime_schema = AuthorSchemaCreate(
        name="Author with   sPaCes  and  UPPERCASE",
        alias="Alias with   sPaCes  and  UPPERCASE",
        birthday="2025-02-13"
    )
    assert anime_schema.name == "author with spaces and uppercase"
    assert anime_schema.alias == "alias with spaces and uppercase"


def test_validation_author_schema_create_attribute_data_type_exceptions():
    with pytest.raises(ValidationError) as exc_info:
        AuthorSchemaCreate(
            name=1,
            alias=1,
            birthday=1
        )
    errors = exc_info.value.errors()
    assert len(errors) == 3
    error_dict = {error['loc'][0]: error['msg'] for error in errors}
    assert '1 is not a string' in error_dict['name']
    assert '1 is not a string' in error_dict['alias']
    assert '1 is not a string' in error_dict['birthday']


@pytest.mark.parametrize(
    "test_case",
    RELEASE_DATES_NOT_VALID.values(),
    ids=RELEASE_DATES_NOT_VALID.keys()
)
def test_validation_anime_schema_create_release_date_attribute(test_case):
    with pytest.raises(ValidationError) as exc_info:
        AuthorSchemaCreate(
            name="Name 1",
            alias="Category 2",
            birthday=test_case["release_date"]
        )
    errors = exc_info.value.errors()
    assert any(test_case["error_message"] in error["msg"] for error in errors)
