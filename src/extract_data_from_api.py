"""Extract and parse the data into tabular form."""

import logging
from pathlib import Path

import pandas as pd
import requests
from utilities.rawg_api_utils import (
    initialize_arguements,
    contains_non_english_chars,
)

log = logging.getLogger(__name__)


def extract_all_data_from_response(
    url: str,
    params: dict,
    dates: list,
) -> list:
    """Extracts data from the API."""
    log.info("Extracting data.")

    data = []

    for i in range(len(dates)):
        params["dates"] = dates[i] + "," + dates[i]
        params["page"] = 1
        while True:
            response = requests.get(url, params=params)
            try:
                response = response.json()
                data.extend(response["results"])
                params["page"] += 1
            except (KeyError, ValueError):
                break

    return data


def parse_data_from_response(response: list) -> pd.DataFrame:
    """Parses the response into a dataframe."""
    log.info("Parsing data.")

    names = []
    release_dates = []
    genres = []
    ratings = []
    game_ids = []
    playtimes = []

    for game in response:
        if not contains_non_english_chars(game["name"]) and game["rating"] != 0:
            names.append(game["name"])
            try:
                genres.append(game["genres"][0]["name"])
            except IndexError:
                genres.append("N/A")
            release_dates.append(game["released"])
            game_ids.append(game["id"])
            ratings.append(game["rating"])
            playtimes.append(game.get("playtime", "N/A"))

    data = pd.DataFrame(
        {
            "name": names,
            "release_date": release_dates,
            "genre": genres,
            "rating": ratings,
            "game_id": game_ids,
            "playtime": playtimes,
        }
    )
    data = data.sort_values(by=["release_date", "name"])
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


if __name__ == "__main__":
    url, params, dates = initialize_arguements()
    response = extract_all_data_from_response(url, params, dates)
    data = parse_data_from_response(response)
    write_data_to_disk(data)
    print("Success.")
