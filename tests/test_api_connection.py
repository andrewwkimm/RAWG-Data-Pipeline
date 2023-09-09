"""Tests if the API can be connected successfully."""
import requests
from src.utilities.rawg_api_utils import initialize_arguements


def test_api_connection() -> None:
    """Tests response returns status code 200."""
    url, params, dates = initialize_arguements()
    params[dates] = dates[0] + "," + dates[0]

    response = requests.get(url, params=params)
    assert (
        response.status_code == 200
    ), f"Failed to connect to API. Status code: {response.status_code}"
