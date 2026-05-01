"""Functions that interact with the Postcode API."""

import requests as req
import os
import json

CACHE_FILE = "./postcode_cache.json"

POSTCODE_URL = "https://api.postcodes.io/postcodes"


def load_cache() -> dict:
    """Loads the cache from a file and converts it from JSON to a dictionary."""
    f = open(f"{CACHE_FILE}")
    cache_data = json.load(f)
    f.close()
    return cache_data


def save_cache(cache: dict):
    """Saves the cache to a file as JSON"""
    with open(f"{CACHE_FILE}", "w") as f:
        json.dump(cache, f, indent=2)


def validate_postcode(postcode: str) -> bool:
    """
    Returns if an inputted postcode is valid or not.
    """
    if not isinstance(postcode, str):
        raise TypeError("Function expects a string.")
    cache = load_cache()
    x = cache.get(postcode)
    if x is None:
        response = req.get(
            f"{POSTCODE_URL}/{postcode}/validate")
        if response.status_code == 200:
            json_response = response.json()
            save_cache(json_response)
            return json_response["result"]
        else:
            if response.status_code == 500:
                raise req.RequestException("Unable to access API.")
            return False
    return cache["postcode"]


def get_postcode_for_location(lat: float, long: float) -> str:
    """
    Returns the postcode of an inputted latitude and longitude.
    """
    if not isinstance(long, float) or not isinstance(lat, float):
        raise TypeError("Function expects two floats.")
    response = req.get(f"{POSTCODE_URL}?lon={long}&lat={lat}")
    if response.status_code == 200:
        json_response = response.json()
        if json_response["result"] is None:
            raise ValueError("No relevant postcode found.")
        return json_response["result"][0]["postcode"]
    else:
        if response.status_code == 500:
            raise req.RequestException("Unable to access API.")


def get_postcode_completions(postcode_start: str) -> list[str]:
    """
    Returns a list of postcodes that start with the input.
    """
    if not isinstance(postcode_start, str):
        raise TypeError("Function expects a string.")
    response = req.get(f"{POSTCODE_URL}/{postcode_start}/autocomplete")
    if response.status_code == 200:
        json_response = response.json()
        return json_response["result"]
    else:
        if response.status_code == 500:
            raise req.RequestException("Unable to access API.")


def get_postcodes_details(postcodes: list[str]) -> list[dict]:
    if not isinstance(postcodes, list):
        raise TypeError("Function expects a list of strings.")
    for code in postcodes:
        if not isinstance(code, str):
            raise TypeError("Function expects a list of strings.")
    response = req.post(f"{POSTCODE_URL}", json=postcodes)
    if response.status_code == 200:
        json_response = response.json()
        return json_response
    if response.status_code == 500:
        raise req.RequestException("Unable to access API.")


if __name__ == "__main__":
    print(get_postcode_completions("SO53"))
