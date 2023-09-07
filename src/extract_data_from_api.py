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
) -> list:
    """Extracts data from the API."""
    log.info("Extracting data.")

    all_data = []

    while True:
        response = requests.get(url, params=params)
        print(params["page"])
        try:
            data = response.json()
            all_data.extend(data["results"])
            params["page"] += 1
        except KeyError:
            print(params["page"])
            break

    return all_data


def parse_api_data(response: list) -> pd.DataFrame:
    """Parses the response into a dataframe."""
    log.info("Parsing data.")

    names = []
    release_dates = []
    genres_list = []
    ratings = []
    prices = []
    game_ids = []
    playtimes = []
    platforms_list = []

    for game in response:
        if not contains_non_english_chars(game["name"]):
            names.append(game["name"])
            try:
                genres = [genre["name"] for genre in game["genres"]]
            except TypeError:
                genres = []
            genres_list.append(genres)
            release_dates.append(game["released"])
            ratings.append(game["rating"])
            prices.append(game.get("price", "N/A"))
            game_ids.append(game["id"])
            playtimes.append(game.get("playtime", "N/A"))
            try:
                platforms = [
                    platform["platform"]["name"] for platform in game["platforms"]
                ]
            except TypeError:
                platforms = []
            platforms_list.append(platforms)

    data = pd.DataFrame(
        {
            "name": names,
            "release_date": release_dates,
            "genres": genres_list,
            "rating": ratings,
            "price": prices,
            "game_id": game_ids,
            "playtime": playtimes,
            "platforms": platforms_list,
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
    args = initialize_arguements()
    response = extract_all_data_from_response(args["url"], args["params"])
    data = parse_api_data(response)
    write_data_to_disk(data)
