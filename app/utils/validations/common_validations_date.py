"""
This module contains the common validations for entity schemas for date data.
"""
import re
from datetime import date, datetime


def validate_date_format(value: str) -> None:
    date_pattern = r'^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$'
    if not re.match(date_pattern, value):
        raise ValueError(f"{value} does not match the format YYYY-MM-DD")


def create_date(value: str) -> date:
    date_object = date.fromisoformat(value)
    return date_object


def validate_date_not_in_the_future(value: date) -> None:
    current_date = datetime.now().date()
    if value > current_date:
        raise ValueError("The date should not be in the future.")


def validate_date_no_less_minimum(value: date, min_date: date) -> None:
    if value < min_date:
            raise ValueError(
                f"Date {value} is too early. "
                f"Minimum allowed date is {min_date}"
            )
