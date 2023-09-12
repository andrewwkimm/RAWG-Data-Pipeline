"""Utilities for processing RAWG's API."""

import os
import logging
from pathlib import Path
from typing import Tuple
from datetime import date, datetime, timedelta

import pandas as pd

log = logging.getLogger(__name__)


def add_dates_to_dataframe(data: pd.DataFrame) -> pd.DataFrame:
    """Adds week, month, and year columns."""
    data["release_date"] = pd.to_datetime(data["release_date"])
    data["year"] = data["release_date"].dt.year
    data["month"] = data["release_date"].dt.strftime("%B")
    data["week"] = data["release_date"].dt.to_period("W-SAT").dt.start_time

    # Format dates to datetime mm-dd-yyyy
    data["release_date"] = pd.to_datetime(data["release_date"].dt.strftime("%m-%d-%Y"))
    data["week"] = pd.to_datetime(data["week"], format="%m-%d-%Y")

    return data


def write_data_to_disk(data: pd.DataFrame) -> None:
    """Save the DataFrame as a .csv file."""
    log.info("Writing to disk.")

    file_path = Path("data")
    file_name = "video_game_data.csv"
    csv_path = file_path / file_name
    if csv_path.exists():
        data.to_csv(csv_path, mode="a", header=False, index=False)
    else:
        data.to_csv(csv_path, index=False)

    log.info("Successfully wrote to disk.")


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


def initialize_arguements() -> Tuple[str, dict, list]:
    """Initializes arguements to pass onto requests."""
    API_KEY = os.getenv("API_KEY")
    today = datetime.now().date()
    dates = get_dates_from_two_weeks_ago(today)
    url = "https://api.rawg.io/api/games"
    params = {
        "key": API_KEY,
        "ordering": "-added",
        "page_size": 40,  # Max amount that can be set
        "page": 1,
    }
    return url, params, dates
