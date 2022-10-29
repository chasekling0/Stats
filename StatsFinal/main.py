import pandas as pd
from numpy import average

from match_engine import MatchEngine
from team import Team

results_data = pd.read_csv(
    "./StatsFinalData.csv")

team_names = results_data["Team"].unique()

header = ["Team", "Played", "Wins", "Draws", "Losses",
          "Points", "Goals For", "Goals Against", "Goal Difference"]
all_header = ["Rank", *header]
all_standings = pd.DataFrame(columns=all_header)

for i in range(1):
    # set up the seasons
    print("Season #" + str(i+1))
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
    # print(team_objects["Arsenal"].results)
    # print(standings.to_string())

    # add table results to tracker
    standings.insert(0, "Rank", standings.index)
    for index, row in standings.iterrows():
        all_standings.loc[(len(all_standings.index))] = row

avg_table = pd.DataFrame(columns=all_header)
best_table = pd.DataFrame(columns=all_header)
worst_table = pd.DataFrame(columns=all_header)
other_stats = pd.DataFrame(columns=[
                           "Team", "Champions", "CL Qual", "EL Qual", "ECL Qual", "Last In", "Relegated", "Bottom"])

final = open("./ResultData.txt", "w", encoding='UTF-8')
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
    goals_for = round(average(results["Goals For"]), 1)
    goals_conceded = round(average(results["Goals Against"]), 1)
    goal_diff = round(average(results["Goal Difference"]), 1)
    averages = [position, team, played, wins, draws, losses,
                points, goals_for, goals_conceded, goal_diff]

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

print("Average Table")
print(avg_table)
print("Best Table")
print(best_table)
print("Worst Table")
print(worst_table)
print("Other Stats")
print(other_stats)
