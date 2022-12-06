import time

import pandas as pd
from numpy import average, std

from match_engine import MatchEngine
from team import Team

start_time = time.time()
results_data = pd.read_csv(
    "./data/StatsFinalData.csv")
results_data.drop(["Fouls", "Yellow Cards", "Red Cards"], inplace=True, axis=1)

team_names = results_data["Team"].unique()

spi_start = {
    "Manchester City": 91.2,
    "Liverpool": 86.4,
    "Arsenal": 85.9,
    "Chelsea": 81,
    "Manchester United": 80,
    "Newcastle": 79.9,
    "Spurs": 79.4,
    "Brighton": 78.2,
    "West Ham": 73.8,
    "Aston Villa": 72.2,
    "Leicester": 70.2,
    "Crystal Palace": 69.5,
    "Brentford": 68.3,
    "Leeds": 65.1,
    "Southampton": 63.2,
    "Wolves": 62.9,
    "Fulham": 62,
    "Everton": 60.7,
    "Bournemouth": 56.6,
    "Nottingham": 55.3,
}

header = ["Team", "Played", "Wins", "Draws", "Losses",
          "Points", "Goals For", "Goals Against", "Goal Difference"]
all_header = ["Rank", "Team", "Played", "Wins", "Draws", "Losses",
              "Points", "Points SD", "Goals For", "Goals Against", "Goal Difference"]
other_header = ["Rank", *header]
all_standings = pd.DataFrame(columns=all_header)

arsenal_stats = pd.DataFrame(columns=["Team", "Opponent", "Home/Away",
                             "Possession", "Passes", "Shots", "On Target", "Goals", "Allowed", "Result"])

remaining_schedule = pd.read_csv(
    "./data/RemainingSchedule.csv")

team_objects = {}
for i, team_name in enumerate(team_names):
    results = results_data.loc[(
        results_data["Team"] == team_name)].dropna(axis=1, how='all').reset_index()
    opp_results = results_data.loc[(
        results_data["Opponent"] == team_name)].dropna(axis=1, how='all').reset_index()
    team_objects[team_name] = Team(
        team_name, results, opp_results, spi_start[team_name])

match_engine = MatchEngine(team_objects, results_data)

for i in range(1):
    # set up the seasons
    print("Season #" + str(i+1))

    # simulate the seasons
    for row_tuple in remaining_schedule.itertuples():
        match_engine.simulate_match(
            row_tuple[1], row_tuple[2])

    # create the final table
    results = []

    # add results to table
    for key, value in team_objects.items():
        results.append(value.final_standing())

    # create and sort and display
    standings = pd.DataFrame(results, columns=header)
    standings = standings.sort_values(
        by=["Points", "Goal Difference", "Goals For"], ascending=False).reset_index()
    standings.index += 1

    for index, row in team_objects["Arsenal"].results.iterrows():
        arsenal_stats.loc[(len(arsenal_stats.index))
                          ] = row

    # add table results to tracker
    standings.insert(0, "Rank", standings.index)
    for index, row in standings.iterrows():
        all_standings.loc[(len(all_standings.index))] = row

    for i, team in enumerate(team_names):
        team_objects[team].reset_team()

avg_table = pd.DataFrame(columns=all_header)
best_table = pd.DataFrame(columns=other_header)
worst_table = pd.DataFrame(columns=other_header)
other_stats = pd.DataFrame(columns=[
                           "Team", "Champions", "CL Qual", "EL Qual", "ECL Qual", "Last In", "Relegated", "Bottom"])
arsenal_averages = pd.DataFrame(columns=["Team", "Opponent", "Home/Away", "Possession",
                                "Passes", "Shots", "On Target", "Goals", "Allowed", "Win %", "Draw %", "Loss %"])

final = open("./data/ResultData.txt", "w", encoding='UTF-8')
for i, team in enumerate(team_names):
    results = all_standings.loc[(all_standings["Team"] == team)]
    best_result = results.loc[(
        results["Points"] == max(results["Points"]))]
    worst_result = results.loc[(
        results["Points"] == min(results["Points"]))]

    position = round(average(results["Rank"]), 1)
    played = sum(results["Played"])
    wins = round(average(results["Wins"]), 1)
    draws = round(average(results["Draws"]), 1)
    losses = round(average(results["Losses"]), 1)
    points = round(average(results["Points"]), 1)
    point_std = round(std([int(x) for x in results["Points"]]), 2)
    goals_for = round(average(results["Goals For"]), 1)
    goals_conceded = round(average(results["Goals Against"]), 1)
    goal_diff = round(average(results["Goal Difference"]), 1)
    averages = [position, team, played, wins, draws, losses,
                points, point_std, goals_for, goals_conceded, goal_diff]

    champions = len(results.loc[(results["Rank"] == 1)])
    cl_qual = len(results.loc[(results["Rank"] <= 4)])
    el_qual = len(results.loc[(results["Rank"].isin([5, 6]))])
    ecl_qual = len(results.loc[(results["Rank"] == 7)])
    last_in = len(results.loc[(results["Rank"] == 17)])
    relegated = len(results.loc[(results["Rank"] >= 18)])
    bottom = len(results.loc[(results["Rank"] == 20)])
    team_stats = [team, champions, cl_qual, el_qual,
                  ecl_qual, last_in, relegated, bottom]

    avg_table.loc[(len(avg_table.index))] = averages
    other_stats.loc[(len(other_stats.index))] = team_stats
    best_table.loc[(len(best_table.index))] = best_result.iloc[0]
    worst_table.loc[(len(worst_table.index))] = worst_result.iloc[0]
    final.write(team + "\n")
    for k, season in results.iterrows():
        final.write(str(list(season)))
        final.write("\n")

final.close()

opponents = team_names.tolist()
opponents.remove("Arsenal")

for i, team in enumerate(opponents):
    team_results = arsenal_stats.loc[(arsenal_stats["Opponent"] == team)]

    arsenal_home = team_results.loc[(team_results["Home/Away"] == "Home")]
    arsenal_away = team_results.loc[(team_results["Home/Away"] == "Away")]

    headers = ["Possession", "Passes", "Shots",
               "On Target", "Goals", "Allowed"]

    home_row = ["Arsenal", team, "Home"]
    away_row = ["Arsenal", team, "Away"]

    for i, stat in enumerate(headers):

        home_stat = average(arsenal_home[stat])
        home_row.append(home_stat)

        away_stat = average(arsenal_away[stat])
        away_row.append(away_stat)

    home_res = arsenal_home["Result"].value_counts(
        normalize=True)
    away_res = arsenal_away["Result"].value_counts(
        normalize=True)
    try:
        home_row.append(home_res["W"])
    except:
        home_row.append(0.0)

    try:
        away_row.append(away_res["W"])
    except:
        away_row.append(0.0)

    try:
        home_row.append(home_res["D"])
    except:
        home_row.append(0.0)

    try:
        away_row.append(away_res["D"])
    except:
        away_row.append(0.0)

    try:
        home_row.append(home_res["L"])
    except:
        home_row.append(0.0)

    try:
        away_row.append(away_res["L"])
    except:
        away_row.append(0.0)

    arsenal_averages.loc[(len(arsenal_averages.index))] = home_row
    arsenal_averages.loc[(len(arsenal_averages.index))] = away_row


avg_table = avg_table.sort_values(
    by=["Points", "Goal Difference", "Goals For"], ascending=False)
avg_table.reset_index(inplace=True, drop=True)
avg_table.index += 1

best_table = best_table.sort_values(
    by=["Points", "Goal Difference", "Goals For"], ascending=False)
best_table.reset_index(inplace=True, drop=True)
best_table.index += 1

worst_table = worst_table.sort_values(
    by=["Points", "Goal Difference", "Goals For"], ascending=False)
worst_table.reset_index(inplace=True, drop=True)
worst_table.index += 1

other_stats = other_stats.sort_values(
    by=["Champions", "CL Qual", "EL Qual", "ECL Qual", "Last In", "Relegated", "Bottom"], ascending=False)
other_stats.reset_index(inplace=True, drop=True)
other_stats.index += 1

arsenal_averages = arsenal_averages.sort_values(
    by=["Opponent", "Goals", "Allowed"])
arsenal_averages.reset_index(inplace=True, drop=True)
arsenal_averages.index += 1

print("Average Table")
print(avg_table)
print("Best Table")
print(best_table)
print("Worst Table")
print(worst_table)
print("Other Stats")
print(other_stats)
print("Arsenal Data")
print(arsenal_averages)

elapsed = (time.time() - start_time) / 60.0
print("Simulating 1000 seasons took: " + str(elapsed) + "minutes")
