"""Extract and parse the data into tabular form."""

import logging

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

    all_data = []

    for i in range(len(dates)):
        params["dates"] = dates[i] + "," + dates[i]
        params["page"] = 1
        while True:
            response = requests.get(url, params=params)
            try:
                data = response.json()
                all_data.extend(data["results"])
                params["page"] += 1
            except (KeyError, ValueError):
                break

    return all_data


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


if __name__ == "__main__":
    url, params, dates = initialize_arguements()
    response = extract_all_data_from_response(url, params, dates)
    data = parse_data_from_response(response)
    print("Success.")
