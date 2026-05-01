"""Functions that interact with the Postcode API."""

import requests as req
import os
import json

CACHE_FILE = "./postcode_cache.json"

POSTCODE_URL = "https://api.postcodes.io/postcodes"


def load_cache() -> dict:
    """Loads the cache from a file and converts it from JSON to a dictionary."""
    # This function is used in Task 3, you can ignore it for now.
    ...


def save_cache(cache: dict):
    """Saves the cache to a file as JSON"""
    # This function is used in Task 3, you can ignore it for now.
    ...


def validate_postcode(postcode: str) -> bool:
    """
    Returns if an inputted postcode is valid or not.
    """
    if not isinstance(postcode, str):
        raise TypeError("Function expects a string.")
    response = req.get(
        f"{POSTCODE_URL}/{postcode}/validate")
    if response.status_code == 200:
        json_response = response.json()
        return json_response["result"]
    else:
        if response.status_code == 500:
            raise req.RequestException("Unable to access API.")
        return False


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
    pass


def get_postcodes_details(postcodes: list[str]) -> dict:
    pass
