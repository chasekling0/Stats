import math
import random

import numpy as np
import pandas as pd

from match_engine import MatchEngine
from team import Team

results_data = pd.read_csv(
    "C:/Users/chase/OneDrive/Documents/Fall2022Classes/Stats/Other/StatsFinal/StatsFinalData.csv")

team_names = results_data["Team"].unique()

team_objects = {}
for i, team_name in enumerate(team_names):
    results = results_data.loc[(
        results_data["Team"] == team_name)].dropna(axis=1, how='all')
    team_objects[team_name] = Team(team_name, results)

match_engine = MatchEngine(team_objects)
match_engine.simulate_match("Arsenal", "Aston Villa")
match_engine.simulate_match("Arsenal", "Manchester City")
match_engine.simulate_match("Arsenal", "Nottingham")
match_engine.simulate_match("Wolves", "Bournemouth")
match_engine.simulate_match("Manchester United", "Leicester")
match_engine.simulate_match("Brentford", "West Ham")
match_engine.simulate_match("Newcastle", "Manchester United")
match_engine.simulate_match("Nottingham", "Leeds")
match_engine.simulate_match("Manchester City", "Spurs")

# TODO - create team objects for every team in the data set
# TODO - match engine to simulate match between two teams that saves the match to results
# TODO - run match engine for remaining results and save to standings
# TODO - way to run match engine 100-1000 times and save stat results

# standings = pd.read_csv(
#     "C:/Users/chase/OneDrive/Documents/Fall2022Classes/Stats/Other/StatsFinal/StatsPremStandings.xlsx")
