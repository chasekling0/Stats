# Chase Kling
# 08-25-2022

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

df = pd.read_csv("Data\ActiveLearning.csv")
x = df["x"]
y = df["y"]
z = df["z"]

plt.hist(z)
plt.show()
