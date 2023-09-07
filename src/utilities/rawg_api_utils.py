"""Utilities for processing RAWG's API."""

import os
from datetime import datetime, timedelta


def contains_non_english_chars(text: str) -> bool:
    """Checks for non alphanumeric characters."""
    return not all(ord(char) < 128 for char in text)


def initialize_arguements() -> dict:
    """Initializes arguements to pass onto requests."""
    API_KEY = os.getenv("API_KEY")
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    yesterday = yesterday.strftime("%Y-%m-%d")

    args = {
        "url": "https://api.rawg.io/api/games",
        "params": {
            "key": API_KEY,
            "dates": f"{yesterday},{yesterday}",
            "ordering": "-added",
            "page_size": 40,  # Max amount that can be set
            "page": 1,
        },
    }
    return args
