import requests


# Function that has a parameter of URL, whenever called it tries to request the given URL, checks for any exceptions,
# then checks its response and returns it back in the correct
def get_response(url):
    # Tries to get URL
    try:
        res = requests.get(url)
    # Any exceptions that might happen call for the program to exit with the details of the occurred exception
    except requests.exceptions.Timeout as ex:
        raise SystemExit(ex)
    except requests.exceptions.TooManyRedirects as ex:
        raise SystemExit(ex)
    except requests.exceptions.RequestException as ex:
        raise SystemExit(ex)

    # If response status below 400
    if res.ok:
        # Guesses correct encoding and encodes and returns the request
        res.encoding = res.apparent_encoding
        return res
    # Else response status 400 or above
    else:
        # Calls for exception with details of the request to figure out what exactly went wrong
        res.raise_for_status()
