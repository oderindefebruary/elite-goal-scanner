import streamlit as st
import pandas as pd

from core.api import get_matches

st.set_page_config(page_title="Elite Goal Scanner", layout="wide")

st.title("⚽ Elite Goal Scanner")

st.write("Live Odds Goal Scanner")

matches = get_matches()

results = []

for match in matches:

    try:

        home = match["home_team"]
        away = match["away_team"]

        bookmakers = match.get("bookmakers", [])

        for bookmaker in bookmakers:

            markets = bookmaker.get("markets", [])

            for market in markets:

                if market["key"] == "totals":

                    outcomes = market.get("outcomes", [])

                    for outcome in outcomes:

                        name = outcome.get("name")
                        point = outcome.get("point")
                        price = outcome.get("price")

                        # ALL OVER MARKETS
                        if name == "Over":

                            implied_probability = round((1 / price) * 100, 2)

                            results.append({
                                "Match": f"{home} vs {away}",
                                "Market": f"Over {point}",
                                "Odds": price,
                                "Probability": implied_probability
                            })

    except Exception as e:
        st.write("ERROR:", e)

# DEBUG
st.write("TOTAL SIGNALS FOUND:", len(results))

# LOWER FILTER
filtered = [
    x for x in results
    if x["Probability"] >= 85
]

# SORT
filtered = sorted(
    filtered,
    key=lambda x: x["Probability"],
    reverse=True
)

df = pd.DataFrame(filtered)

st.subheader("Signals")

if not df.empty:

    st.dataframe(df, use_container_width=True)

    st.bar_chart(df.set_index("Match")["Probability"])

else:

    st.warning("No qualifying matches found.")
