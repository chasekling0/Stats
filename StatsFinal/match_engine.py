import math

from numpy import average, random, std
from scipy.stats import poisson as poisson

import team


class MatchEngine:
    '''simulation engine for matches'''

    def __init__(self, team_list):
        '''initialize with team information for simulation'''

        self.team_information = team_list

    def simulate_match(self, home_name, away_name):
        '''pass in two team names, return result'''
        self.home_team = self.team_information[home_name]
        self.away_team = self.team_information[away_name]

        # TODO - fouls should utilize red and yellow cards, do not for now
        home_fouls, away_fouls = self.get_fouls()
        home_poss, away_poss = self.get_possession()
        home_passes, away_passes = self.get_passes(home_poss, away_poss)
        home_shots, away_shots = self.get_shots(home_passes, away_passes)
        home_on_target, away_on_target = self.get_shots_on_target(
            home_shots, away_shots)
        home_goals, away_goals = self.get_goals(
            home_on_target, away_on_target)

        if home_goals + away_goals >= 7:
            print(home_name + " " + str(home_goals) +
                  "-" + str(away_goals) + " " + away_name)

        score = home_goals - away_goals
        home_result, away_result = self.determine_winner(score)

        home_output = [0, home_name, away_name, "Home", home_poss, home_fouls, 0, 0,
                       home_passes, home_shots, home_on_target, home_goals, away_goals, home_result]
        away_output = [0, away_name, home_name, "Away", away_poss, away_fouls, 0, 0,
                       away_passes, away_shots, away_on_target, away_goals, home_goals, away_result]

        self.home_team.update_results(home_output, away_output)
        self.away_team.update_results(away_output, home_output)

    def determine_winner(self, score):
        if score > 0:
            return 'W', 'L'
        elif score == 0:
            return 'D', 'D'
        elif score < 0:
            return 'L', 'W'

    def get_fouls(self):
        home_foul_avg, home_foul_std = self.home_team.attributes[
            "AvgHomeFouls"], self.home_team.attributes["HomeFoulsStd"]

        away_foul_avg, away_foul_std = self.away_team.attributes[
            "AvgAwayFouls"], self.away_team.attributes["AwayFoulsStd"]

        random_std = random.normal(0, 0.5)

        home_fouls = round(home_foul_avg + (home_foul_std * random_std))
        away_fouls = round(away_foul_avg + (away_foul_std * random_std))

        return home_fouls, away_fouls

    def get_goals(self, home_on_target, away_on_target):
        '''generates total number of shots a team makes in a game'''

        home_avg_goals, home_goals_std, home_goals_def, home_goals_def_std, home_played = self.home_team.attributes[
            "AvgHomeGoalsPerTarget"], self.home_team.attributes["HomeGoalsPerTargetStd"], self.home_team.attributes[
                "AvgHomeGoalConc"], self.home_team.attributes["HomeGoalConcStd"], self.home_team.attributes["HomePlayed"]

        away_avg_goals, away_goals_std, away_goals_def, away_goals_def_std, away_played = self.away_team.attributes[
            "AvgAwayGoalsPerTarget"], self.away_team.attributes["AwayGoalsPerTargetStd"], self.away_team.attributes[
            "AvgAwayGoalConc"], self.away_team.attributes["AwayGoalConcStd"], self.away_team.attributes["AwayPlayed"]

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

        home_xGoals = home_goal_per_target * home_on_target
        away_xGoals = away_goal_per_target * away_on_target

        goal_values = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        home_prob = []
        away_prob = []

        for i, val in enumerate(goal_values):
            home_val = poisson.pmf(k=val, mu=home_xGoals) * 1000
            away_val = poisson.pmf(k=val, mu=away_xGoals) * 1000
            if not math.isnan(home_val):
                home_prob.append(round(home_val))
            else:
                home_prob.append(0)
            if not math.isnan(away_val):
                away_prob.append(round(away_val))
            else:
                away_prob.append(0)

        random_home = random.normal(500, 100)
        random_away = random.normal(500, 100)

        total = 0
        home_goals, away_goals = 0, 0
        for i, prob in enumerate(home_prob):
            total += prob
            if random_home <= total:
                home_goals = goal_values[i]
                break

        total = 0
        for i, prob in enumerate(away_prob):
            total += prob
            if random_away <= total:
                away_goals = goal_values[i]
                break

        return home_goals, away_goals

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
