"""
This module contains the common validations for entity schemas for str data.
"""

def validate_is_instance_str(value: str) -> None:
    """
    Validate if the input value is an instance of string.

    Args:
        value(str): The value to be validated.

    Returns:
        str: The validated string value.

    Raises:
        ValueError: If the value is not an instance of string.
    """
    if not isinstance(value, str):
        raise ValueError(f'{value} is not a string is a {type(value)}')
