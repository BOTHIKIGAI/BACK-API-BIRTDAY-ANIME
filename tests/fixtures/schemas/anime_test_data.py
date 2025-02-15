"""
This module contains the data structures with the test information.
"""

RELEASE_DATES_NOT_VALID = {
    "future_date": {
        "release_date": "2999-02-14",
        "error_message": "The date should not be in the future."
    },
    "too_early_date": {
        "release_date": "1906-12-31",
        "error_message": "Date 1906-12-31 is too early. Minimum allowed date is 1907-01-01"
    },
    "invalid_format": {
        "release_date": "not-a-date",
        "error_message": "not-a-date does not match the format YYYY-MM-DD"
    }
}
