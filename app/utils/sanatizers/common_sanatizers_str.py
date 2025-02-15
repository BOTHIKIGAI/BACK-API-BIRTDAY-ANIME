"""
This module contains the common sanitizations for schema str data.
"""

def remove_extra_spaces(value: str) -> str:
    """
    Remove multiple spaces between words and leading/trailing spaces from a string.

    Args:
        value (str): The input string to be sanitized.

    Returns:
        str: The sanitized string with single spaces between words and no leading/trailing spaces.

    Example:
        >>> remove_extra_spaces("  hello   world  ")
        "hello world"
    """
    return ' '.join(value.split())


def convert_to_lowercase(value: str) -> str:
    """
    Convert a string to lowercase.

    Args:
        value (str): The input string to be converted.

    Returns:
        str: The lowercase version of the input string.

    Example:
        >>> convert_to_lowercase("Hello World")
        "hello world"
    """
    return value.lower()
