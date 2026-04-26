import streamlit as st
import pandas as pd

from core.api import get_matches

# PAGE CONFIG
st.set_page_config(
    page_title="Elite Goal Scanner",
    layout="wide"
)

# HEADER
st.title("⚽ Elite Goal Scanner")

st.write(
    "Low-Odds Over 1.5 Goal Probability Scanner"
)

# FETCH MATCHES
matches = get_matches()

results = []

# PROCESS DATA
for match in matches:

    try:

        home = match["home_team"]
        away = match["away_team"]

        bookmakers = match.get("bookmakers", [])

        for bookmaker in bookmakers:

            markets = bookmaker.get("markets", [])

            for market in markets:

                # ONLY TOTALS MARKET
                if market["key"] != "totals":
                    continue

                outcomes = market.get("outcomes", [])

                for outcome in outcomes:

                    name = outcome.get("name")
                    point = outcome.get("point")
                    price = outcome.get("price")

                    # ONLY OVER 1.5
                    if name != "Over":
                        continue

                    if point != 1.5:
                        continue

                    # IMPLIED PROBABILITY
                    implied_probability = round(
                        (1 / price) * 100,
                        2
                    )

                    # GRADE SIGNALS
                    if price <= 1.20:
                        grade = "A+"

                    elif price <= 1.28:
                        grade = "A"

                    elif price <= 1.35:
                        grade = "B"

                    else:
                        grade = "C"

                    results.append({
                        "Match": f"{home} vs {away}",
                        "Market": "Over 1.5",
                        "Odds": price,
                        "Probability": implied_probability,
                        "Grade": grade
                    })

    except Exception as e:
        st.write("ERROR:", e)

# REMOVE DUPLICATES + FILTER
filtered = []

seen = set()

for x in results:

    match = x["Match"]
    market = x["Market"]
    odds = x["Odds"]
    prob = x["Probability"]

    unique_key = f"{match}-{market}"

    # REMOVE DUPLICATES
    if unique_key in seen:
        continue

    seen.add(unique_key)

    # SAFE ODDS RANGE
    if odds < 1.10 or odds > 1.35:
        continue

    # MINIMUM IMPLIED PROBABILITY
    if prob < 72:
        continue

    filtered.append(x)

# SORT BEST SIGNALS FIRST
filtered = sorted(
    filtered,
    key=lambda x: (
        x["Odds"],
        -x["Probability"]
    )
)

# DATAFRAME
df = pd.DataFrame(filtered)

# DISPLAY
st.subheader("📊 Elite Over 1.5 Signals")

st.metric(
    label="Total Qualified Signals",
    value=len(df)
)

if not df.empty:

    st.dataframe(
        df,
        use_container_width=True
    )

    # CHART
    chart_df = df.set_index("Match")["Probability"]

    st.subheader("📈 Probability Chart")

    st.bar_chart(chart_df)

else:

    st.warning(
        "No qualifying low-odds Over 1.5 signals found today."
    )
