"""
This module contains the common validations for entity schemas for date data.
"""
import re
from datetime import date, datetime


def validate_date_format(value: str) -> None:
    """
    Validate if a string matches the format YYYY-MM-DD.

    Args:
        value (str): The date string to validate.

    Raises:
        ValueError: If the date string doesn't match the format YYYY-MM-DD.
    """
    date_pattern = r'^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$'
    if not re.match(date_pattern, value):
        raise ValueError(f"{value} does not match the format YYYY-MM-DD")


def create_date(value: str) -> date:
    """
    Convert a string in ISO format to a date object.

    Args:
        value (str): The date string in ISO format (YYYY-MM-DD).

    Returns:
        date: A date object created from the input string.

    Raises:
        ValueError: If the string cannot be converted to a date.
    """
    date_object = date.fromisoformat(value)
    return date_object


def validate_date_not_in_the_future(value: date) -> None:
    """
    Validate that a date is not in the future.

    Args:
        value (date): The date to validate.

    Raises:
        ValueError: If the date is in the future.
    """
    current_date = datetime.now().date()
    if value > current_date:
        raise ValueError("The date should not be in the future.")


def validate_date_no_less_minimum(value: date, min_date: date) -> None:
    """
    Validate that a date is not earlier than a minimum allowed date.

    Args:
        value (date): The date to validate.
        min_date (date): The minimum allowed date.

    Raises:
        ValueError: If the date is earlier than the minimum allowed date.
    """
    if value < min_date:
            raise ValueError(
                f"Date {value} is too early. "
                f"Minimum allowed date is {min_date}"
            )
