import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from numpy import average
from scipy import interpolate
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.feature_selection import SelectFromModel
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF
from sklearn.model_selection import (GridSearchCV, RandomizedSearchCV,
                                     train_test_split)

# aggregate to nearest 0.5 xG
# go from there?

# classifier model based on difference of SPI and W/D/L
# potentially create a MVP of this and see if there is space to add more detail


results_data = pd.read_csv(
    "./data/StatsFinalData.csv")

results_data.sort_values(by="Team xG")
# xg_data = results_data.drop(
#     ["Team", "Opponent", "Home/Away", "Result", "Allowed", "Red Cards",
#         "Yellow Cards", "Fouls", "Team xG", "Team nsxG", "Opponent xG", "Opponent nsxG"], axis=1)

# results_data = results_data.loc[(results_data["Team"] == "Brighton")]

xg_result = np.array(results_data["On Target"])
goal_result = np.array(results_data["Team xG"])
# xg_result = np.array([round(a/5) * 5 for a in xg_result])
goal_result = np.array([round(a, 2) for a in goal_result])
print(xg_result)
f1 = interpolate.interp1d(xg_result, goal_result)
poly = np.poly1d(np.polyfit(xg_result, goal_result, deg=3))
xg_result = xg_result.reshape(-1, 1)
print(xg_result)


xg_train, xg_test, g_train, g_test = train_test_split(
    xg_result, goal_result, test_size=0.3)
kernel = 1 * RBF(length_scale=1.0, length_scale_bounds=(1e-5, 1e5))
gaussian_process = GaussianProcessRegressor(
    kernel=kernel, n_restarts_optimizer=9)
gaussian_process.fit(xg_train, g_train)

polyline = np.linspace(min(xg_result), max(xg_result))
test_line = np.array([0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5])
test_line = test_line.reshape(-1, 1)
mean_prediction, std_prediction = gaussian_process.predict(
    test_line, return_std=True)

print(std_prediction)


plt.scatter(xg_result, goal_result, color='b')
# plt.scatter(xg_train, g_train, color='r')
# plt.plot(test_line, mean_prediction, color='r', marker='+')
# plt.scatter(xg_result, f1(xg_result))
# plt.fill_between(
#     test_line.ravel(),
#     mean_prediction - 1.96 * std_prediction,
#     mean_prediction + 1.96 * std_prediction,
#     alpha=0.5
# )
plt.title("SPI Difference vs Total xG Generated, All Teams")
plt.xlabel("SPI Difference")
plt.ylabel("Total xG Generated")
plt.plot(polyline, poly(polyline))
plt.show()

# opp_spi = list(arsenal_res["Opponent SPI"])
# team_spi = list(arsenal_res["Team SPI"])

# xGd_train, xGd_test, xGr_train, xGr_test = train_test_split(
#     xg_data, xg_result, test_size=0.2, random_state=42)

# plt.scatter(opp_spi - team_spi, xg_result, lw=0.8, color="r")
# # plt.scatter(nsxg_result, goal_result, lw=0.8, color='g')
# poly = np.poly1d(np.polyfit(opp_spi - team_spi, xg_result, deg=2))
# # poly2 = np.poly1d(np.polyfit(nsxg_result, goal_result, deg=2))
# polyline = np.linspace(0, 5)
# plt.plot(polyline, poly(polyline))
# # plt.plot(polyline, poly2(polyline))
# plt.xlabel("Opponent SPI")
# plt.ylabel("xG")
# plt.show()
# # print(stats.pearsonr(xg_result, goal_result))


# names = xg_data.columns
# # current best but only 80% accuracy
# rfr = RandomForestRegressor(max_depth=100, max_features='sqrt',
#                             min_samples_leaf=3, min_samples_split=2, n_estimators=2000, bootstrap=False)
# rfr.fit(xGd_train, xGr_train)
# print(sorted(zip(map(lambda x: round(x, 4), rfr.feature_importances_), names), reverse=True))


# def evaluate(model, test_features, test_labels):
#     print("True Values: ", test_labels)
#     predictions = model.predict(test_features)
#     print("Pred Values: ", predictions)
#     predictions = [x for x in predictions]
#     test_labels = [y for y in test_labels]
#     errors = abs(np.subtract(predictions, test_labels))
#     mape = 100 * np.mean(errors / (test_labels))
#     accuracy = 100 - mape
#     print('Model Performance')
#     print('Average Error: {:0.4f} degrees.'.format(np.mean(errors)))
#     print('Accuracy = {:0.2f}%.'.format(accuracy))

#     return accuracy


# rfr_accuracy = evaluate(rfr, xGd_test, xGr_test)

# # grouped_place = results_data.groupby("Home/Away")
# # for name, group in grouped_place:
# #     print(name, str(average(group["Goals"])))
# #     print(name, str(average(group["Allowed"])))
# #     print(name, str(average(group["Team nsxG"])))
# #     print(name, str(average(group["Opponent nsxG"])))

# # grouped_teams = results_data.groupby("Team")
# # for name, group in grouped_teams:
# #     home_away = group.groupby("Home/Away")
# #     for place, group2 in home_away:
# #         print(name, place, str(average(group2["Goals"])))
# #         print(name, place, str(average(group2["Allowed"])))
# #         print(name, place, str(average(group2["Team nsxG"])))
# #         print(name, place, str(average(group2["Opponent nsxG"])))
