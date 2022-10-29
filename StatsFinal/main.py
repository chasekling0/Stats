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
        results_data["Team"] == team_name)].dropna(axis=1, how='all').reset_index()
    opp_results = results_data.loc[(
        results_data["Opponent"] == team_name)].dropna(axis=1, how='all').reset_index()

    team_objects[team_name] = Team(team_name, results, opp_results)

match_engine = MatchEngine(team_objects)

remaining_schedule = pd.read_csv(
    "./RemainingSchedule.csv")

for row_tuple in remaining_schedule.itertuples():
    match_engine.simulate_match(
        row_tuple[1], row_tuple[2])

header = ["Team", "Played", "Wins", "Draws", "Losses",
          "Points", "Goals For", "Goals Against", "Goal Difference"]
results = []

for key, value in team_objects.items():
    results.append(value.final_standing())

standings = pd.DataFrame(results, columns=header)
standings = standings.sort_values(
    by=["Points", "Goal Difference", "Goals For"], ascending=False)

print(team_objects["Arsenal"].results)
print(standings.to_string())

# TODO - create team objects for every team in the data set
# TODO - match engine to simulate match between two teams that saves the match to results
# TODO - run match engine for remaining results and save to standings
# TODO - way to run match engine 100-1000 times and save stat results
