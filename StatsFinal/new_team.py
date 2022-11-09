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
        self.attributes = {}
        # self.generate_attributes()
