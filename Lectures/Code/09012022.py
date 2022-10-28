# Chase Kling
# 09-01-2022

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

df = pd.read_csv(
    "C:/Users/chase/OneDrive/Documents/Stats/Lectures/Data/DiceActivity.csv")

d_twelve = df["D12"]
d_six = df["D6"]

dtwelve_array = np.asarray(d_twelve)
print(dtwelve_array.mean())
print(np.median(dtwelve_array))

dsix_array = np.asarray(d_six)
print(dsix_array.mean())
print(np.median(dsix_array))
