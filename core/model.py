import pandas as pd

def load_team_strength():

    return pd.read_csv("data/team_strength.csv")


def get_team_strength(team, df):

    row = df[df["team"] == team]

    if len(row) == 0:
        return 0.50, 0.50

    return float(row["attack"]), float(row["defense"])


def calculate_probability(home, away, df):

    home_attack, home_def = get_team_strength(home, df)
    away_attack, away_def = get_team_strength(away, df)

    # OVER 0.5 GOAL LOGIC (simple but effective MVP model)

    probability = (
        (home_attack * 0.6) +
        ((1 - away_def) * 0.4)
    ) * 100

    return round(probability, 2)
