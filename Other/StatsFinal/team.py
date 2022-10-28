import math
from operator import truediv

import pandas as pd
from numpy import average, std


class Team:
    '''class to hold and update team attributes'''

    def __init__(self, name, results) -> None:
        '''initialize and generate attributes based on results'''
        self.name = name
        self.results: pd.DataFrame = results
        self.attributes = {}
        self.generate_attributes()

    def __str__(self):
        '''basic string representation of the class'''
        return str(self.name) + "\n" + str(self.results)

    def generate_attributes(self):
        '''generate attributes from given results'''
        self.home_games = self.results.loc[(
            self.results["Home/Away"] == "Home")].dropna(axis=0)
        self.away_games = self.results.loc[(
            self.results["Home/Away"] == "Away")].dropna(axis=0)

        self.generate_possession_stats()
        self.generate_pass_stats()
        self.generate_all_shot_stats()
        self.generate_goal_stats()
        self.generate_defensive_stats()

    def generate_possession_stats(self):
        # home possession attributes
        self.attributes["AvgHomePoss"] = average(self.home_games["Possession"])
        self.attributes["HomePossVar"] = self.home_games["Possession"].var()
        self.attributes["HomePlayed"] = len(self.home_games)

        # away possession attributes
        self.attributes["AvgAwayPoss"] = average(self.away_games["Possession"])
        self.attributes["AwayPossVar"] = self.away_games["Possession"].var()
        self.attributes["AwayPlayed"] = len(self.away_games)

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
            map(truediv, list(self.home_games["On Target"]), list(self.home_games["Shots"])))
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
            map(truediv, list(self.away_games["On Target"]), list(self.away_games["Shots"])))
        self.attributes["AvgAwayShotOnTarget"] = average(
            away_shots_on_target_ratio)
        self.attributes["AwayOnTargetStd"] = std(away_shots_on_target_ratio)

    def generate_goal_stats(self):
        # home goals attributes
        home_goals_ratio = list(
            map(truediv, list(self.home_games["Goals"]), list(self.home_games["On Target"])))
        self.attributes["AvgHomeGoalsPerTarget"] = average(
            home_goals_ratio)
        self.attributes["HomeGoalsPerTargetStd"] = std(home_goals_ratio)

        # away goals attributes
        away_goals_ratio = list(
            map(truediv, list(self.away_games["Goals"]), list(self.away_games["On Target"].replace(0, 1))))
        self.attributes["AvgAwayGoalsPerTarget"] = average(
            away_goals_ratio)
        self.attributes["AwayGoalsPerTargetStd"] = std(away_goals_ratio)

    def generate_defensive_stats(self):
        # home defensive attributes
        self.attributes["AvgHomeGoalsConceded"] = average(
            self.home_games["Allowed"])
        self.attributes["HomeGoalsConcededVar"] = self.home_games["Allowed"].var()

        # away defensive attributes
        self.attributes["AvgAwayGoalsConceded"] = average(
            self.away_games["Allowed"])
        self.attributes["AwayGoalsConcededVar"] = self.away_games["Allowed"].var()

    # TODO - way to save results to the results field
    # TODO - update attributes based on generated games
