import requests

API_KEY = "YOUR_API_KEY"

SPORT = "soccer"

REGIONS = "eu"

MARKETS = "totals"

ODDS_FORMAT = "decimal"


def get_matches():

    url = f"https://api.the-odds-api.com/v4/sports/{SPORT}/odds"

    params = {
        "apiKey": API_KEY,
        "regions": REGIONS,
        "markets": MARKETS,
        "oddsFormat": ODDS_FORMAT
    }

    response = requests.get(url, params=params)

    return response.json()
