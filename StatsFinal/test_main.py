import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from numpy import average
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.feature_selection import SelectFromModel
from sklearn.model_selection import (GridSearchCV, RandomizedSearchCV,
                                     train_test_split)

results_data = pd.read_csv(
    "./data/StatsFinalData.csv")

arsenal_res = results_data.loc[(results_data["Team"] == "Arsenal")]

xg_data = arsenal_res.drop(
    ["Team", "Opponent", "Home/Away", "Result", "Goals", "Allowed", "Red Cards",
        "Yellow Cards", "Fouls", "Team xG", "Team nsxG", "Opponent xG", "Opponent nsxG"], axis=1)
xg_result = list(arsenal_res["Team nsxG"])
opp_spi = list(arsenal_res["Opponent SPI"])
team_spi = list(arsenal_res["Team SPI"])

xGd_train, xGd_test, xGr_train, xGr_test = train_test_split(
    xg_data, xg_result, test_size=0.2, random_state=42)

plt.scatter(opp_spi - team_spi, xg_result, lw=0.8, color="r")
# plt.scatter(nsxg_result, goal_result, lw=0.8, color='g')
poly = np.poly1d(np.polyfit(opp_spi - team_spi, xg_result, deg=2))
# poly2 = np.poly1d(np.polyfit(nsxg_result, goal_result, deg=2))
polyline = np.linspace(0, 5)
plt.plot(polyline, poly(polyline))
# plt.plot(polyline, poly2(polyline))
plt.xlabel("Opponent SPI")
plt.ylabel("xG")
plt.show()
# print(stats.pearsonr(xg_result, goal_result))


names = xg_data.columns
# current best but only 80% accuracy
rfr = RandomForestRegressor(max_depth=100, max_features='sqrt',
                            min_samples_leaf=3, min_samples_split=2, n_estimators=2000, bootstrap=False)
rfr.fit(xGd_train, xGr_train)
print(sorted(zip(map(lambda x: round(x, 4), rfr.feature_importances_), names), reverse=True))


def evaluate(model, test_features, test_labels):
    print("True Values: ", test_labels)
    predictions = model.predict(test_features)
    print("Pred Values: ", predictions)
    predictions = [x for x in predictions]
    test_labels = [y for y in test_labels]
    errors = abs(np.subtract(predictions, test_labels))
    mape = 100 * np.mean(errors / (test_labels))
    accuracy = 100 - mape
    print('Model Performance')
    print('Average Error: {:0.4f} degrees.'.format(np.mean(errors)))
    print('Accuracy = {:0.2f}%.'.format(accuracy))

    return accuracy


rfr_accuracy = evaluate(rfr, xGd_test, xGr_test)

# grouped_place = results_data.groupby("Home/Away")
# for name, group in grouped_place:
#     print(name, str(average(group["Goals"])))
#     print(name, str(average(group["Allowed"])))
#     print(name, str(average(group["Team nsxG"])))
#     print(name, str(average(group["Opponent nsxG"])))

# grouped_teams = results_data.groupby("Team")
# for name, group in grouped_teams:
#     home_away = group.groupby("Home/Away")
#     for place, group2 in home_away:
#         print(name, place, str(average(group2["Goals"])))
#         print(name, place, str(average(group2["Allowed"])))
#         print(name, place, str(average(group2["Team nsxG"])))
#         print(name, place, str(average(group2["Opponent nsxG"])))
