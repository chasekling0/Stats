import math
import random

import numpy as np
import pandas as pd

from match_engine import MatchEngine
from team import Team

results_data = pd.read_csv(
    "./StatsFinalData.csv")

team_names = results_data["Team"].unique()

team_objects = {}
for i, team_name in enumerate(team_names):
    results = results_data.loc[(
        results_data["Team"] == team_name)].dropna(axis=1, how='all')
    opp_results = results_data.loc[(
        results_data["Opponent"] == team_name)].dropna(axis=1, how='all')

    team_objects[team_name] = Team(team_name, results, opp_results)

match_engine = MatchEngine(team_objects)
match_engine.simulate_match("Bournemouth", "Wolves")
match_engine.simulate_match("Arsenal", "West Ham")
match_engine.simulate_match("Aston Villa", "Spurs")
match_engine.simulate_match("Brentford", "Southampton")
match_engine.simulate_match("Brighton", "Nottingham")
match_engine.simulate_match("Chelsea", "Newcastle")
match_engine.simulate_match("Crystal Palace", "Manchester United")
match_engine.simulate_match("Everton", "Manchester City")
match_engine.simulate_match("Fulham", "Liverpool")
match_engine.simulate_match("Leeds", "Leicester")


# TODO - create team objects for every team in the data set
# TODO - match engine to simulate match between two teams that saves the match to results
# TODO - run match engine for remaining results and save to standings
# TODO - way to run match engine 100-1000 times and save stat results
