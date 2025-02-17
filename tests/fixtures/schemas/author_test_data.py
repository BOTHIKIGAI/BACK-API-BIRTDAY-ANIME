"""
This module contains the data structures with the test information.
"""

RELEASE_DATES_NOT_VALID = {
    "future_date": {
        "release_date": "2999-02-14",
        "error_message": "The date should not be in the future."
    },
    "too_early_date": {
        "release_date": "1800-11-04",
        "error_message": "Date 1800-11-04 is too early. Minimum allowed date is 1877-11-04"
    },
    "invalid_format": {
        "release_date": "not-a-date",
        "error_message": "not-a-date does not match the format YYYY-MM-DD"
    }
}
