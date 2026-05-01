"""Functions that interact with the Postcode API."""

import os
import json
import requests as req

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
    response = req.get(f"{POSTCODE_URL}/{postcode}/validate", timeout=30)
    if response.status_code == 200:
        json_response = response.json()
        return json_response["result"]
    if response.status_code == 500:
        raise req.RequestException("Unable to access API.")
    return False


def get_postcode_for_location(lat: float, long: float) -> str:
    """
    Returns the postcode of an inputted latitude and longitude.
    """
    if not isinstance(long, float) or not isinstance(lat, float):
        raise TypeError("Function expects two floats.")
    response = req.get(f"{POSTCODE_URL}?lon={long}&lat={lat}", timeout=30)
    if response.status_code == 200:
        json_response = response.json()
        if json_response["result"] is None:
            raise ValueError("No relevant postcode found.")
        return json_response["result"][0]["postcode"]
    if response.status_code == 500:
        raise req.RequestException("Unable to access API.")
    return None


def get_postcode_completions(postcode_start: str) -> list[str]:
    """
    Returns a list of postcodes that start with the input.
    """
    if not isinstance(postcode_start, str):
        raise TypeError("Function expects a string.")
    response = req.get(
        f"{POSTCODE_URL}/{postcode_start}/autocomplete", timeout=30)
    if response.status_code == 200:
        json_response = response.json()
        return json_response["result"]
    if response.status_code == 500:
        raise req.RequestException("Unable to access API.")
    return None


def get_postcodes_details(postcodes: list[str]) -> list[dict]:
    """
    Returns details about a postcode.
    """
    response = []
    if not isinstance(postcodes, list):
        raise TypeError("Function expects a list of strings.")
    for code in postcodes:
        if not isinstance(code, str):
            raise TypeError("Function expects a list of strings.")
    payload = {
        "postcodes": postcodes
    }
    headers = {
        'Accept': 'application/json'
    }
    response = req.post(f"{POSTCODE_URL}", headers=headers,
                        data=payload, timeout=30)
    if response.status_code == 200:
        json_response = response.json()
        return json_response
    if response.status_code == 500:
        raise req.RequestException("Unable to access API.")
    return response
