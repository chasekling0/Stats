import math

import numpy as np
from numpy import average, random


class MatchEngine:
    '''simulation engine for matches'''

    def __init__(self, team_list, results_data):
        '''initialize with team information for simulation'''

        self.team_information = team_list
        self.results_data = results_data.reset_index()

    def simulate_match(self, home_name, away_name):
        '''pass in two team names, return result'''
        self.home_team = self.team_information[home_name]
        self.away_team = self.team_information[away_name]

        spi_diff = np.array(self.results_data["SPI Difference"])
        xg_gen = np.array(self.results_data["Team xG"])
        nsxg_gen = np.array(self.results_data["Team nsxG"])

        self.xg_gen_model = np.poly1d(
            np.polyfit(spi_diff, xg_gen, deg=3))
        self.nsxg_gen_model = np.poly1d(
            np.polyfit(spi_diff, nsxg_gen, deg=3))

        home_poss, away_poss = self.get_possession()
        home_passes, away_passes = self.get_passes(home_poss, away_poss)
        home_shots, away_shots = self.get_shots(home_passes, away_passes)
        home_on_target, away_on_target = self.get_shots_on_target(
            home_shots, away_shots)
        home_xG, home_nsxG, away_xG, away_nsxG = self.get_xgs()
        home_goals, away_goals = self.get_goals(
            home_on_target, away_on_target, home_xG, home_nsxG, away_xG, away_nsxG)

        # if home_goals + away_goals > 4:
        print(home_name + " " + str(home_goals) +
              "-" + str(away_goals) + " " + away_name)

        score = home_goals - away_goals
        home_result, away_result = self.determine_winner(score)

        home_output = [0, home_name, away_name, "Home", home_poss, home_passes, home_shots, home_on_target, home_goals, away_goals, home_result, self.home_team.spi,
                       self.away_team.spi, self.home_team.spi - self.away_team.spi, home_xG, away_xG, home_nsxG, away_nsxG, home_xG + home_nsxG, away_xG + away_nsxG]
        away_output = [0, away_name, home_name, "Away", away_poss, away_passes, away_shots, away_on_target, away_goals, home_goals, away_result, self.away_team.spi,
                       self.home_team.spi, self.away_team.spi - self.home_team.spi, away_xG, home_xG, away_nsxG, home_nsxG, away_xG + away_nsxG, home_xG + home_nsxG]

        self.home_team.update_results(home_output, away_output)
        self.away_team.update_results(away_output, home_output)

        self.results_data.loc[len(self.results_data.index)] = home_output
        self.results_data.loc[len(self.results_data.index)] = away_output

    def determine_winner(self, score):
        home_spi = self.home_team.spi
        away_spi = self.away_team.spi
        home_adj = home_spi / 100.00
        away_adj = away_spi / 100.00

        if score > 0:
            self.home_team.spi += away_adj
            self.away_team.spi -= home_adj
            return 'W', 'L'
        elif score == 0:
            self.home_team.spi += away_adj / 2.0
            self.away_team.spi += home_adj / 2.0
            return 'D', 'D'
        elif score < 0:
            self.home_team.spi -= away_adj
            self.away_team.spi += home_adj
            return 'L', 'W'

    def get_goals(self, home_on_target, away_on_target, home_xg, home_nsxg, away_xg, away_nsxg):
        '''generates total number of shots a team makes in a game'''

        home_avg_goals, home_goals_std, home_goals_def, home_goals_def_std, home_played = self.home_team.attributes[
            "AvgHomeGoalsPerTarget"], self.home_team.attributes["HomeGoalsPerTargetStd"], self.home_team.attributes[
                "AvgHomeGoalConc"], self.home_team.attributes["HomeGoalConcStd"], self.home_team.attributes["HomePlayed"]

        away_avg_goals, away_goals_std, away_goals_def, away_goals_def_std, away_played = self.away_team.attributes[
            "AvgAwayGoalsPerTarget"], self.away_team.attributes["AwayGoalsPerTargetStd"], self.away_team.attributes[
            "AvgAwayGoalConc"], self.away_team.attributes["AwayGoalConcStd"], self.away_team.attributes["AwayPlayed"]

        home_conversion = self.home_team.home_oe + \
            (random.normal(-0.1, 0.05) * self.home_team.home_oe)
        away_conversion = self.away_team.away_oe + \
            (random.normal(-0.1, 0.05) * self.away_team.away_oe)

        home_defense = self.home_team.home_de + \
            (random.normal(-0.1, 0.05) * self.home_team.home_de)
        away_defense = self.away_team.away_de + \
            (random.normal(-0.1, 0.05) * self.away_team.away_de)

        home_extra_goal_avg = home_avg_goals - away_goals_def
        home_extra_goal_std = math.sqrt((math.pow(home_goals_std, 2) / (home_played - 1)) +
                                        (math.pow(away_goals_def_std, 2) / (away_played - 1)))

        away_extra_goal_avg = away_avg_goals - home_goals_def
        away_extra_goal_std = math.sqrt((math.pow(away_goals_std, 2) / (away_played - 1)) +
                                        (math.pow(home_goals_def_std, 2) / (home_played - 1)))

        home_goal_per_target = home_avg_goals - \
            random.normal(home_extra_goal_avg, home_extra_goal_std)

        away_goal_per_target = away_avg_goals - \
            random.normal(away_extra_goal_avg, away_extra_goal_std)

        # goals based on conversion of shots
        home_xGoals = home_goal_per_target * home_on_target
        away_xGoals = away_goal_per_target * away_on_target

        # goals based on conversion of xG
        home_x_goals = home_conversion * (home_xg + home_nsxg)
        home_x_allowed = home_defense * (away_xg + away_nsxg)

        away_x_goals = away_conversion * (away_xg + away_nsxg)
        away_x_allowed = away_defense * (home_xg + home_nsxg)

        home_xGoals = average(
            [(home_xGoals * 1.25) + (home_x_goals * 0.25), away_x_allowed])
        away_xGoals = average(
            [(away_xGoals * 1.25) + (away_x_goals * 0.25), home_x_allowed])

        xG_dependency = 0.25 * math.sqrt(math.fabs(home_xGoals*away_xGoals))
        home_xGoals -= xG_dependency
        away_xGoals -= xG_dependency

        def get_goals(home_xGoals, away_xGoals, xG_dependency):
            home_xGoals = -0.5 * home_xGoals if home_xGoals < 0 else home_xGoals
            away_xGoals = -0.5 * away_xGoals if away_xGoals < 0 else away_xGoals

            home_goals = average(np.random.poisson(home_xGoals, 100))
            away_goals = average(np.random.poisson(away_xGoals, 100))
            shared = average(np.random.poisson(xG_dependency, 100))

            home_goals = int(home_goals + shared)
            away_goals = int(away_goals + shared)
            return home_goals, away_goals

        home_goals, away_goals = get_goals(
            home_xGoals, away_xGoals, xG_dependency)
        if home_goals == away_goals:
            home_goals, away_goals = get_goals(
                home_xGoals, away_xGoals, xG_dependency)

        return home_goals, away_goals

    def get_xgs(self):
        home_spi = self.home_team.spi
        away_spi = self.away_team.spi
        home_diff = home_spi - away_spi
        away_diff = away_spi - home_spi

        home_xg = self.xg_gen_model(home_diff)
        home_nsxg = self.nsxg_gen_model(home_diff)
        away_xg = self.xg_gen_model(away_diff)
        away_nsxg = self.nsxg_gen_model(away_diff)

        home_avg_xg = self.home_team.attributes["AvgHomexG"]
        home_xg_std = self.home_team.attributes["HomexGStd"]
        home_avg_nsxg = self.home_team.attributes["AvgHomensxG"]
        home_nsxg_std = self.home_team.attributes["HomensxGStd"]
        home_avg_xg_conc = self.home_team.attributes["AvgHomexGConc"]
        home_xg_conc_std = self.home_team.attributes["HomeXgConcStd"]
        home_avg_nsxg_conc = self.home_team.attributes["AvgHomensxGConc"]
        home_nsxg_conc_std = self.home_team.attributes["HomensXgConcStd"]

        away_avg_xg = self.away_team.attributes["AvgAwayxG"]
        away_xg_std = self.away_team.attributes["AwayxGStd"]
        away_avg_nsxg = self.away_team.attributes["AvgAwaynsxG"]
        away_nsxg_std = self.away_team.attributes["AwaynsxGStd"]
        away_avg_xg_conc = self.away_team.attributes["AvgAwayxGConc"]
        away_xg_conc_std = self.away_team.attributes["AwayXgConcStd"]
        away_avg_nsxg_conc = self.away_team.attributes["AvgAwaynsxGConc"]
        away_nsxg_conc_std = self.away_team.attributes["AwaynsXgConcStd"]

        home_xg_final = average(
            [home_xg, random.normal(home_avg_xg, home_xg_std), random.normal(away_avg_xg_conc, away_xg_conc_std)])
        home_nsxg_final = average(
            [home_nsxg, random.normal(home_avg_nsxg, home_nsxg_std), random.normal(away_avg_nsxg_conc, away_nsxg_conc_std)])
        away_xg_final = average([away_xg, random.normal(
            away_avg_xg, away_xg_std), random.normal(home_avg_xg_conc, home_xg_conc_std)])
        away_nsxg_final = average(
            [away_nsxg, random.normal(away_avg_nsxg, away_nsxg_std), random.normal(home_avg_nsxg_conc, home_nsxg_conc_std)])

        return home_xg_final, home_nsxg_final, away_xg_final, away_nsxg_final

    def get_shots_on_target(self, home_shots, away_shots):
        '''generates total number of shots a team makes in a game'''

        home_avg_target, home_target_std, home_target_def, home_target_def_std, home_played = self.home_team.attributes[
            "AvgHomeShotOnTarget"], self.home_team.attributes["HomeOnTargetStd"], self.home_team.attributes[
                "AvgHomeOnTargetConc"], self.home_team.attributes["HomeOnTargetConcStd"], self.home_team.attributes["HomePlayed"]

        away_avg_target, away_target_std, away_target_def, away_target_def_std, away_played = self.away_team.attributes[
            "AvgAwayShotOnTarget"], self.away_team.attributes["AwayOnTargetStd"], self.away_team.attributes[
            "AvgAwayOnTargetConc"], self.away_team.attributes["AwayOnTargetConcStd"], self.away_team.attributes["AwayPlayed"]

        home_extra_target_avg = home_avg_target - away_target_def
        home_extra_target_std = math.sqrt((math.pow(home_target_std, 2) / (home_played - 1)) +
                                          (math.pow(away_target_def_std, 2) / (away_played - 1)))

        away_extra_target_avg = away_avg_target - home_target_def
        away_extra_target_std = math.sqrt((math.pow(away_target_std, 2) / (away_played - 1)) +
                                          (math.pow(home_target_def_std, 2) / (home_played - 1)))

        home_target_per_shot = home_avg_target - \
            random.normal(home_extra_target_avg, home_extra_target_std)

        away_target_per_shot = away_avg_target - \
            random.normal(away_extra_target_avg, away_extra_target_std)

        home_target = round(home_target_per_shot * home_shots)
        away_target = round(away_target_per_shot * away_shots)

        return home_target, away_target

    def get_shots(self, home_passes, away_passes):
        '''generates total number of shots a team makes in a game'''

        home_avg_shots, home_shot_std, home_shot_def, home_def_std, home_played = self.home_team.attributes[
            "AvgHomeShotPerPass"], self.home_team.attributes["HomeShotPerPassStd"], self.home_team.attributes[
                "AvgHomeShotPassConc"], self.home_team.attributes["HomeShotPassConcStd"], self.home_team.attributes["HomePlayed"]

        away_avg_shots, away_shot_std, away_shot_def, away_def_std, away_played = self.away_team.attributes[
            "AvgAwayShotPerPass"], self.away_team.attributes["AwayShotPerPassStd"], self.away_team.attributes[
            "AvgAwayShotPassConc"], self.away_team.attributes["AwayShotPassConcStd"], self.away_team.attributes["AwayPlayed"]

        home_extra_shot_avg = home_avg_shots - away_shot_def
        home_extra_shot_std = math.sqrt((math.pow(home_shot_std, 2) / (home_played - 1)) +
                                        (math.pow(away_def_std, 2) / (away_played - 1)))

        away_extra_shot_avg = away_avg_shots - home_shot_def
        away_extra_shot_std = math.sqrt((math.pow(away_shot_std, 2) / (away_played - 1)) +
                                        (math.pow(home_def_std, 2) / (home_played - 1)))

        home_shot_per_pass = home_avg_shots - \
            random.normal(home_extra_shot_avg, home_extra_shot_std)

        away_shot_per_pass = away_avg_shots - \
            random.normal(away_extra_shot_avg, away_extra_shot_std)

        home_shots = round(home_shot_per_pass * home_passes)
        away_shots = round(away_shot_per_pass * away_passes)

        return home_shots, away_shots

    def get_passes(self, home_poss, away_poss):
        '''generates total number of passes teams make in a game'''

        home_avg_pass, home_pass_std = self.home_team.attributes[
            "AvgHomePassPerPoss"], self.home_team.attributes["HomePassPerPossStd"]

        away_avg_pass, away_pass_std = self.away_team.attributes[
            "AvgAwayPassPerPoss"], self.away_team.attributes["AwayPassPerPossStd"]

        home_pass_per_poss = random.normal(home_avg_pass, home_pass_std)
        away_pass_per_poss = random.normal(away_avg_pass, away_pass_std)

        home_passes = round(home_poss * home_pass_per_poss)
        away_passes = round(away_poss * away_pass_per_poss)

        return home_passes, away_passes

    def get_possession(self):
        '''generate possession, return difference in possession for home team'''

        # need average possession, variance, and the number of games played for both teams
        home_avg, home_var, home_played = self.home_team.attributes[
            "AvgHomePoss"], self.home_team.attributes["HomePossVar"], self.home_team.attributes["HomePlayed"]
        away_avg, away_var, away_played = self.away_team.attributes[
            "AvgAwayPoss"], self.away_team.attributes["AwayPossVar"], self.away_team.attributes["AwayPlayed"]

        # currently treating a difference of 2 distributions
        diff_avg = home_avg - away_avg
        diff_std = math.sqrt((home_var / (home_played - 1)) +
                             (away_var / (away_played - 1)))

        # assuming 50% is baseline, average possession for home team is 50% plus the random adjustment
        home_poss = 50 + random.normal(diff_avg, diff_std)
        return round(home_poss, 2), round(100 - home_poss, 2)
