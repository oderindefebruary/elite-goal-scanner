import streamlit as st
import pandas as pd

from core.api import get_matches

st.set_page_config(page_title="Elite Goal Scanner", layout="wide")

st.title("⚽ Elite Goal Scanner")

st.write("Live Over 0.5 Probability Scanner")

matches = get_matches()

results = []

for match in matches:

    try:

        home = match["home_team"]
        away = match["away_team"]

        bookmakers = match["bookmakers"]

        for bookmaker in bookmakers:

            markets = bookmaker["markets"]

            for market in markets:

                if market["key"] == "totals":

                    outcomes = market["outcomes"]

                    for outcome in outcomes:

                        name = outcome["name"]

                        point = outcome.get("point", 0)

                        price = outcome["price"]

                        # LOOK FOR OVER 0.5

                       if name == "Over":

    implied_probability = round((1 / price) * 100, 2)

    results.append({
        "Match": f"{home} vs {away}",
        "Market": f"Over {point}",
        "Odds": price,
        "Probability": implied_probability
    })

    except:
        continue

# FILTER
filtered = [x for x in results if x["Probability"] >= 80]

# SORT
filtered = sorted(filtered, key=lambda x: x["Probability"], reverse=True)

df = pd.DataFrame(filtered)

st.subheader("Top Goal Signals")

st.dataframe(df, use_container_width=True)

if not df.empty:
    st.bar_chart(df.set_index("Match")["Probability"])
else:
    st.warning("No qualifying matches found.")
