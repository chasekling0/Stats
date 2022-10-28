import math

from numpy import random

import team


class MatchEngine:
    '''simulation engine for matches'''

    def __init__(self, team_list):
        '''initialize with team information for simulation'''

        self.team_information = team_list

    def simulate_match(self, home_name, away_name):
        '''pass in two team names, return result'''
        home_team = self.team_information[home_name]
        away_team = self.team_information[away_name]

        # TODO - fouls here? a red card would change ALL game outcomes

        home_poss = self.get_possession(home_team, away_team)
        away_poss = round(100 - home_poss, 2)

        # TODO - either after possession or passes, team's defenses need to be factored in
        home_passes = self.get_passes(home_team, home_poss, True)
        away_passes = self.get_passes(away_team, away_poss, False)

        home_shots = self.get_shots(home_team, home_passes, True)
        away_shots = self.get_shots(away_team, away_passes, False)

        home_on_target = self.get_shots_on_target(home_team, home_shots, True)
        away_on_target = self.get_shots_on_target(away_team, away_shots, False)

        home_xG, home_xG_std = self.get_expected_goals(
            home_team, home_on_target, True)
        away_xG, away_xG_std = self.get_expected_goals(
            away_team, away_on_target, False)

        # defense currently only factored in here
        home_goals = self.get_goals(
            home_team, home_xG, home_xG_std, away_team, True)
        away_goals = self.get_goals(
            away_team, away_xG, away_xG_std, home_team, False)

        print(home_name + " " + str(home_goals) +
              "-" + str(away_goals) + " " + away_name)

        # TODO - better concept of this function

    def get_goals(self, team, xG, xG_std, defense_team, home):
        '''generates total goals scored in a game'''
        key_mod = 'Away' if home else 'Home'
        avg_key = "Avg" + key_mod + "GoalsConceded"
        var_key = key_mod + "GoalsConcededVar"
        def_play_key = key_mod + "Played"
        off_play_key = ('Home' if home else "Away") + "Played"

        def_played = defense_team.attributes[def_play_key]
        off_played = team.attributes[off_play_key]

        avg_conc = defense_team.attributes[avg_key]
        conc_var = defense_team.attributes[var_key]
        xG_var = math.pow(xG_std, 2)

        diff_avg = xG - avg_conc
        diff_std = math.sqrt((xG_var / (off_played - 1)) +
                             (conc_var / (def_played - 1)))

        random_std = random.normal(0, 1)
        goals = round(diff_avg + (diff_std * random_std))

        return goals if goals > 0 else 0

    def get_expected_goals(self, team, on_target, home):
        '''generates total number of goals expected to be scored in a game'''

        # set up keys so function may work for either team
        key_mod = 'Home' if home else 'Away'
        avg_key = "Avg" + key_mod + "GoalsPerTarget"
        std_key = key_mod + "GoalsPerTargetStd"

        # get attributes + random performance factor
        avg_goals = team.attributes[avg_key]
        goals_std = team.attributes[std_key]
        random_std = random.normal(0, 0.5)

        # return total number of shots the team makes
        goals_per_target = avg_goals + (random_std * goals_std)
        return on_target * goals_per_target, goals_std * goals_per_target

    def get_shots_on_target(self, team, shots, home):
        '''generates total number of shots on target a team makes in a game'''

        # set up keys so function may work for either team
        key_mod = 'Home' if home else 'Away'
        avg_key = "Avg" + key_mod + "ShotOnTarget"
        std_key = key_mod + "OnTargetStd"

        # get attributes + random performance factor
        avg_on_target = team.attributes[avg_key]
        on_target_std = team.attributes[std_key]
        random_std = random.normal(0, 0.5)

        # return total number of shots the team makes
        on_target_per_shot = avg_on_target + (random_std * on_target_std)
        return round(shots * on_target_per_shot)

    def get_shots(self, team, passes, home):
        '''generates total number of shots a team makes in a game'''

        # set up keys so function may work for either team
        key_mod = 'Home' if home else 'Away'
        avg_key = "Avg" + key_mod + "ShotPerPass"
        std_key = key_mod + "ShotPerPassStd"

        # get attributes + random performance factor
        avg_shots = team.attributes[avg_key]
        shot_std = team.attributes[std_key]
        random_std = random.normal(0, 0.5)

        # return total number of shots the team makes
        shots_per_pass = avg_shots + (random_std * shot_std)
        return round(passes * shots_per_pass)

    def get_passes(self, team, poss, home):
        '''generates total number of passes a team makes in a game'''

        # set up keys so function may work for either team
        key_mod = 'Home' if home else 'Away'
        avg_key = "Avg" + key_mod + "PassPerPoss"
        std_key = key_mod + "PassPerPossStd"

        # get attributes + random performance factor
        avg_pass = team.attributes[avg_key]
        pass_std = team.attributes[std_key]
        random_std = random.normal(0, 0.5)

        # return total number of passes the team makes
        pass_per_poss = avg_pass + (random_std * pass_std)
        return round(poss * pass_per_poss)

    def get_possession(self, home_team, away_team):
        '''generate possession, return difference in possession for home team'''

        # need average possession, variance, and the number of games played for both teams
        home_avg, home_var, home_played = home_team.attributes[
            "AvgHomePoss"], home_team.attributes["HomePossVar"], home_team.attributes["HomePlayed"]
        away_avg, away_var, away_played = away_team.attributes[
            "AvgAwayPoss"], away_team.attributes["AwayPossVar"], away_team.attributes["AwayPlayed"]

        # currently treating a difference of 2 distributions
        diff_avg = home_avg - away_avg
        diff_std = math.sqrt((home_var / (home_played - 1)) +
                             (away_var / (away_played - 1)))

        # generate random number to determine 'how much' possession
        # generating with std of 0.5 to balance randomness
        random_std = random.normal(0, 0.5)

        # assuming 50% is baseline, average possession for home team is 50% plus the difference in averages, plus the positive/negative performance adjustment
        home_poss = 50 + diff_avg + (random_std * diff_std)
        return round(home_poss, 2)
