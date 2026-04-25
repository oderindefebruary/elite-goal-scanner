import requests
from bs4 import BeautifulSoup

def get_fixtures():

    url = "https://www.espn.com/soccer/fixtures"
    headers = {"User-Agent": "Mozilla/5.0"}

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    fixtures = []

    for row in soup.find_all("tr"):

        text = row.get_text(" ", strip=True)

        if "vs" in text:

            try:
                home, away = text.split("vs")
                fixtures.append((home.strip(), away.strip()))
            except:
                continue

    return fixtures
