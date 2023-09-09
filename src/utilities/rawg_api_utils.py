"""Utilities for processing RAWG's API."""

import os
from typing import Tuple, Dict, List
from datetime import date, datetime, timedelta


def contains_non_english_chars(text: str) -> bool:
    """Checks for non alphanumeric characters."""
    return not all(ord(char) < 128 for char in text)


def get_dates_from_two_weeks_ago(today: date) -> list:
    """Returns a list of a dates from two weeks ago."""
    dates = []

    one_week_ago = today - timedelta(days=7)
    two_weeks_ago = today - timedelta(days=14)

    while two_weeks_ago <= one_week_ago:
        dates.append(two_weeks_ago.strftime("%Y-%m-%d"))
        two_weeks_ago += timedelta(days=1)

    return dates


def initialize_arguements() -> Tuple[Dict[str, str], List[str]]:
    """Initializes arguements to pass onto requests."""
    API_KEY = os.getenv("API_KEY")
    today = datetime.now().date()

    dates = get_dates_from_two_weeks_ago(today)

    args = {
        "url": "https://api.rawg.io/api/games",
        "params": {
            "key": API_KEY,
            "ordering": "-added",
            "page_size": 40,  # Max amount that can be set
            "page": 1,
        },
    }
    return args, dates
