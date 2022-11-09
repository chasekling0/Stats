import math
from operator import truediv

import pandas as pd
from numpy import average, std


class Team:
    '''class to hold and update team attributes'''

    def __init__(self, name, results, opposition_results) -> None:
        '''initialize and generate attributes based on results'''
        self.name = name
        self.results: pd.DataFrame = results
        self.opp: pd.DataFrame = opposition_results
        # print(name)
        # print(str(opposition_results))
        self.attributes = {}
        self.generate_attributes()

    def __str__(self):
        '''basic string representation of the class'''
        return str(self.name) + "\n" + str(self.results)

    def final_standing(self):
        games_played = len(self.results)
        match_results = self.results["Result"].value_counts()
        wins = match_results._get_value("W")
        draws = match_results._get_value("D")
        losses = match_results._get_value("L")
        points = (3 * wins) + draws
        goals_for = self.results["Goals"].sum()
        goals_conceded = self.results["Allowed"].sum()
        goal_difference = goals_for - goals_conceded

        return [self.name, games_played, wins, draws, losses, points, goals_for, goals_conceded, goal_difference]

    def update_results(self, team_result, opp_result):
        self.results.loc[len(self.results.index)] = team_result
        self.opp.loc[len(self.opp.index)] = opp_result

        self.attributes.clear()
        self.generate_attributes()

    def generate_attributes(self):
        '''generate attributes from given results'''

        # offensive stats for games at home
        self.home_games = self.results.loc[(
            self.results["Home/Away"] == "Home")].dropna(axis=0)

        # offensive stats for games away from home
        self.away_games = self.results.loc[(
            self.results["Home/Away"] == "Away")].dropna(axis=0)

        # defensive stats for games at home
        self.home_opp = self.opp.loc[(
            self.opp["Home/Away"] == "Away")].dropna(axis=0)

        # defensive stats for games away from home
        self.away_opp = self.opp.loc[(
            self.opp["Home/Away"] == "Home")].dropna(axis=0)

        self.generate_possession_stats()
        self.generate_pass_stats()
        self.generate_all_shot_stats()
        self.generate_goal_stats()
        self.generate_defensive_stats()
        # self.generate_efficiency()

    def generate_efficiency(self):
        self.home_oe = self.attributes["AvgScoredHome"] / \
            self.attributes["AvgHomensxG"]
        self.away_oe = self.attributes["AvgScoredAway"] / \
            self.attributes["AvgAwaynsxG"]

        self.home_de = self.attributes["AvgHomeGoalsConc"] / \
            self.attributes["AvgHomensxGConc"]
        self.away_de = self.attributes["AvgAwayGoalsConc"] / \
            self.attributes["AvgAwaynsxGConc"]

        self.home_overall = round(self.home_oe / self.home_de, 3)
        self.away_overall = round(self.away_oe / self.away_de, 3)

        print(self.home_oe)
        print(self.away_oe)
        print(self.home_de)
        print(self.away_de)
        print(self.home_overall)
        print(self.away_overall)

    def generate_possession_stats(self):
        # home possession attributes
        self.attributes["AvgHomePoss"] = average(self.home_games["Possession"])
        self.attributes["HomePossVar"] = self.home_games["Possession"].var()
        self.attributes["HomePlayed"] = len(self.home_games)

        # away possession attributes
        self.attributes["AvgAwayPoss"] = average(self.away_games["Possession"])
        self.attributes["AwayPossVar"] = self.away_games["Possession"].var()
        self.attributes["AwayPlayed"] = len(self.away_games)

        # home fouls attributes
        self.attributes["AvgHomeFouls"] = average(self.home_games["Fouls"])
        self.attributes["HomeFoulsStd"] = self.home_games["Fouls"].std()

        home_yellow_per_foul = list(map(truediv, list(
            self.home_games["Yellow Cards"]), list(self.home_games["Fouls"].replace(0, 1))))
        self.attributes["AvgHomeYellow"] = average(home_yellow_per_foul)
        self.attributes["HomeYellowStd"] = std(home_yellow_per_foul)

        home_red_per_foul = list(map(truediv, list(
            self.home_games["Red Cards"]), list(self.home_games["Fouls"].replace(0, 1))))
        self.attributes["AvgHomeRed"] = average(home_red_per_foul)
        self.attributes["HomeRedStd"] = std(home_red_per_foul)

        # away fouls attributes
        self.attributes["AvgAwayFouls"] = average(self.away_games["Fouls"])
        self.attributes["AwayFoulsStd"] = self.away_games["Fouls"].std()

        away_yellow_per_foul = list(map(truediv, list(
            self.away_games["Yellow Cards"]), list(self.away_games["Fouls"].replace(0, 1))))
        self.attributes["AvgAwayYellow"] = average(away_yellow_per_foul)
        self.attributes["AwayYellowStd"] = std(away_yellow_per_foul)

        away_red_per_foul = list(map(truediv, list(
            self.away_games["Red Cards"]), list(self.away_games["Fouls"].replace(0, 1))))
        self.attributes["AvgAwayRed"] = average(away_red_per_foul)
        self.attributes["AwayRedStd"] = std(away_red_per_foul)

    def generate_pass_stats(self):
        # home pass attributes
        home_pass_per_possession = list(
            map(truediv, list(self.home_games["Passes"]), list(self.home_games["Possession"])))
        self.attributes["AvgHomePassPerPoss"] = average(
            home_pass_per_possession)
        self.attributes["HomePassPerPossStd"] = std(home_pass_per_possession)

        # away pass attributes
        away_pass_per_possession = list(
            map(truediv, list(self.away_games["Passes"]), list(self.away_games["Possession"])))
        self.attributes["AvgAwayPassPerPoss"] = average(
            away_pass_per_possession)
        self.attributes["AwayPassPerPossStd"] = std(away_pass_per_possession)

    def generate_all_shot_stats(self):
        # home shots attributes
        home_shots_per_pass = list(
            map(truediv, list(self.home_games["Shots"]), list(self.home_games["Passes"])))
        self.attributes["AvgHomeShotPerPass"] = average(home_shots_per_pass)
        self.attributes["HomeShotPerPassStd"] = std(home_shots_per_pass)

        # home shot on target attributes
        home_shots_on_target_ratio = list(
            map(truediv, list(self.home_games["On Target"]), list(self.home_games["Shots"].replace(0, 1))))
        self.attributes["AvgHomeShotOnTarget"] = average(
            home_shots_on_target_ratio)
        self.attributes["HomeOnTargetStd"] = std(home_shots_on_target_ratio)

        # away shots attributes
        away_shots_per_pass = list(
            map(truediv, list(self.away_games["Shots"]), list(self.away_games["Passes"])))
        self.attributes["AvgAwayShotPerPass"] = average(away_shots_per_pass)
        self.attributes["AwayShotPerPassStd"] = std(away_shots_per_pass)

        # away shot on target attributes
        away_shots_on_target_ratio = list(
            map(truediv, list(self.away_games["On Target"]), list(self.away_games["Shots"].replace(0, 1))))
        self.attributes["AvgAwayShotOnTarget"] = average(
            away_shots_on_target_ratio)
        self.attributes["AwayOnTargetStd"] = std(away_shots_on_target_ratio)

        # # home xG
        # self.attributes["AvgHomexG"] = average(self.home_games["Team xG"])

        # # home nsxG
        # self.attributes["AvgHomensxG"] = average(self.home_games["Team nsxG"])

        # # away xG
        # self.attributes["AvgAwayxG"] = average(self.away_games["Team xG"])

        # # away nsxG
        # self.attributes["AvgAwaynsxG"] = average(self.away_games["Team nsxG"])

    def generate_goal_stats(self):
        # home goals attributes
        home_goals_ratio = list(
            map(truediv, list(self.home_games["Goals"]), list(self.home_games["On Target"].replace(0, 1))))
        self.attributes["AvgHomeGoalsPerTarget"] = average(
            home_goals_ratio)
        self.attributes["HomeGoalsPerTargetStd"] = std(home_goals_ratio)

        # away goals attributes
        away_goals_ratio = list(
            map(truediv, list(self.away_games["Goals"]), list(self.away_games["On Target"].replace(0, 1))))
        self.attributes["AvgAwayGoalsPerTarget"] = average(
            away_goals_ratio)
        self.attributes["AwayGoalsPerTargetStd"] = std(away_goals_ratio)

        # avg home scored
        self.attributes["AvgScoredHome"] = average(self.home_games["Goals"])

        # avg away scored
        self.attributes["AvgScoredAway"] = average(self.away_games["Goals"])

    def generate_defensive_stats(self):

        # home passes to shots conceded
        home_shots_per_pass_conc = list(
            map(truediv, list(self.home_opp["Shots"]), list(self.home_opp["Passes"])))
        self.attributes["AvgHomeShotPassConc"] = average(
            home_shots_per_pass_conc)
        self.attributes["HomeShotPassConcStd"] = std(
            home_shots_per_pass_conc)

        # home shots to shots on target conceded
        home_shots_on_target_conc = list(
            map(truediv, list(self.home_opp["On Target"]), list(self.home_opp["Shots"].replace(0, 1))))
        self.attributes["AvgHomeOnTargetConc"] = average(
            home_shots_on_target_conc)
        self.attributes["HomeOnTargetConcStd"] = std(
            home_shots_on_target_conc)

        # home shots on target to goals conceded
        home_target_goals_conc = list(
            map(truediv, list(self.home_opp["Goals"]), list(self.home_opp["On Target"].replace(0, 1))))
        self.attributes["AvgHomeGoalConc"] = average(
            home_target_goals_conc)
        self.attributes["HomeGoalConcStd"] = std(
            home_target_goals_conc)

        # away passes to shots conceded
        away_shots_per_pass_conc = list(
            map(truediv, list(self.away_opp["Shots"]), list(self.away_opp["Passes"])))
        self.attributes["AvgAwayShotPassConc"] = average(
            away_shots_per_pass_conc)
        self.attributes["AwayShotPassConcStd"] = std(
            away_shots_per_pass_conc)

        # away shots to shots on target conceded
        away_shots_on_target_conc = list(
            map(truediv, list(self.away_opp["On Target"]), list(self.away_opp["Shots"].replace(0, 1))))
        self.attributes["AvgAwayOnTargetConc"] = average(
            away_shots_on_target_conc)
        self.attributes["AwayOnTargetConcStd"] = std(
            away_shots_on_target_conc)

        # away shots on target to goals conceded
        away_target_goals_conc = list(
            map(truediv, list(self.away_opp["Goals"]), list(self.away_opp["On Target"].replace(0, 1))))
        self.attributes["AvgAwayGoalConc"] = average(
            away_target_goals_conc)
        self.attributes["AwayGoalConcStd"] = std(
            away_target_goals_conc)

        # # home conceded
        # self.attributes["AvgHomeGoalsConc"] = average(
        #     self.home_games["Allowed"])

        # # away conceded
        # self.attributes["AvgAwayGoalsConc"] = average(
        #     self.away_games["Allowed"])

        # # home xG conceded
        # self.attributes["AvgHomexGConc"] = average(
        #     self.home_games["Opponent xG"])

        # # home nsxG conceded
        # self.attributes["AvgHomensxGConc"] = average(
        #     self.home_games["Opponent nsxG"])

        # # away xG conceded
        # self.attributes["AvgAwayxGConc"] = average(
        #     self.away_games["Opponent xG"])

        # # away nsxG conceded
        # self.attributes["AvgAwaynsxGConc"] = average(
        #     self.away_games["Opponent nsxG"])
