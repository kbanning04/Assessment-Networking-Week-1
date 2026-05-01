"""A CLI application for interacting with the Postcode API."""

from argparse import ArgumentParser
from postcode_functions import validate_postcode, get_postcode_completions


def adding_parsers():
    """
    Receives inputs from CLI
    """
    parser = ArgumentParser()
    parser.add_argument(
        "--mode", "-m", choices=["validate", "complete"], required=True)
    parser.add_argument("postcode", help="A postcode to input", type=str)
    args = parser.parse_args()
    return args


def main():
    """
    Either, returns if a postcode is valid or not. Or returns a list of postcodes that start with the input.
    """
    args = adding_parsers()
    mode = args.mode
    postcode = args.postcode
    postcode = postcode.upper()
    postcode = postcode.strip()
    if mode == "validate":
        valid = validate_postcode(postcode)
        if valid is True:
            return f"{postcode} is a valid postcode."
        return f"{postcode} is not a valid postcode."
    possible_postcodes = get_postcode_completions(postcode)
    if possible_postcodes is None:
        return f"No matches for {postcode}."
    i = 1
    list_of_possibles = possible_postcodes[0]
    while i < 5:
        list_of_possibles += "\n" + possible_postcodes[i]
        i += 1
    return list_of_possibles


if __name__ == "__main__":
    print(main())
