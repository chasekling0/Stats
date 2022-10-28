# Chase Kling
# 08-25-2022

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

"""
x = [1,2,3,4] #list
y = np.asarray(x) #array
print(sum(x)/len(x)) #mean list
print(y.mean()) #mean array
print(np.median(y)) #median array
"""

df = pd.read_csv("Data\IrisData.csv")
# print(df)
sepal_length = df["sepal_length"]
sepal_width = df["sepal_width"]
petal_length = df["petal_length"]
petal_width = df["petal_width"]
species = df["species"]

plt.hist(sepal_width, bins=150)
plt.show()
