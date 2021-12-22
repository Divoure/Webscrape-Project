import requests


def get_response(url):
    try:
        res = requests.get(url)
        res.encoding = res.apparent_encoding
    except requests.exceptions.Timeout as ex:
        raise SystemExit(ex)
    except requests.exceptions.TooManyRedirects as ex:
        raise SystemExit(ex)
    except requests.exceptions.RequestException as ex:
        raise SystemExit(ex)
    if res.ok:
        return res
    else:
        res.raise_for_status()
