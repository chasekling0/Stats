import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.tree import plot_tree

results_data = pd.read_csv(
    "./data/StatsFinalData.csv")

feature = results_data.drop(
    ["Team", "Opponent", "Home/Away", "Result", "Goals", "Allowed"], axis=1)
response = results_data["Goals"]
f_train, f_test, r_train, r_test = train_test_split(
    feature, response, test_size=0.1)

rfr = RandomForestRegressor()
rfr.fit(f_train, r_train)
score = rfr.score(f_train, r_train)
print("R-Squared:", score)

r_pred = rfr.predict(f_test)
mse = mean_squared_error(r_test, r_pred)
print("MSE: ", mse)
print("RMSE: ", mse*(1/2.0))

x_ax = range(len(r_test))
plt.plot(x_ax, r_test, linewidth=1, label="Original")
plt.plot(x_ax, r_pred, linewidth=1.1, label="Predicted")
plt.title("Real Goals v Predicted Goals")
plt.xlabel("Test")
plt.ylabel("Goals")
plt.legend(loc='best', fancybox=True, shadow=True)
plt.grid(True)
plt.show()
