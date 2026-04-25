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

            parts = text.split("vs")

            if len(parts) == 2:

                home = parts[0].strip()
                away = parts[1].strip()

                # filter junk rows
                if len(home) > 2 and len(away) > 2:
                    fixtures.append((home, away))

    return fixtures
