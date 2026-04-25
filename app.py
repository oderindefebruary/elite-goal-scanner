import streamlit as st
import pandas as pd

from core.scraper import get_fixtures
from core.model import load_team_strength, calculate_probability

st.set_page_config(page_title="Elite Goal Scanner", layout="wide")

st.title("⚽ Elite Goal Scanner")

st.write("Over 0.5 Goal Probability Engine (No API Version)")

# LOAD DATA
team_df = load_team_strength()

# GET FIXTURES
fixtures = get_fixtures()

results = []

for home, away in fixtures:

    try:
        prob = calculate_probability(home, away, team_df)

        if prob >= 90:

            results.append({
                "Match": f"{home} vs {away}",
                "Probability": prob
            })

    except:
        continue

# SORT RESULTS
results = sorted(results, key=lambda x: x["Probability"], reverse=True)

df = pd.DataFrame(results)

st.subheader("Top Goal Signals")

st.dataframe(df, use_container_width=True)

st.subheader("Probability Chart")

if not df.empty:
    st.bar_chart(df.set_index("Match"))
else:
    st.warning("No high probability matches found today.")
