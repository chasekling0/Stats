# predict matches using models based on SPI and statistics
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats as stats
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.feature_selection import SelectFromModel
from sklearn.model_selection import (GridSearchCV, RandomizedSearchCV,
                                     train_test_split)

# one model for xG from game stats
# one model for nsxG from game stats
# one model for goals from xG, nsxG, SPIs

results_data = pd.read_csv(
    "./data/StatsFinalData.csv")

team_map = {
    "Bournemouth": 1,
    "Arsenal": 2,
    "Aston Villa": 3,
    "Brentford": 4,
    "Brighton": 5,
    "Chelsea": 6,
    "Crystal Palace": 7,
    "Everton": 8,
    "Fulham": 9,
    "Leeds": 10,
    "Leicester": 11,
    "Liverpool": 12,
    "Manchester City": 13,
    "Manchester United": 14,
    "Newcastle": 15,
    "Nottingham": 16,
    "Southampton": 17,
    "Spurs": 18,
    "West Ham": 19,
    "Wolves": 20
}

home_away_map = {
    "Home": 0,
    "Away": 1
}

results_data["Team"] = results_data["Team"].map(team_map)
results_data["Opponent"] = results_data["Opponent"].map(team_map)
results_data["Home/Away"] = results_data["Home/Away"].map(home_away_map)

results_data = results_data.dropna(axis=1, how='all')

xG_data = results_data.drop(
    ["Result", "Goals", "Allowed", "Red Cards",
        "Yellow Cards", "Fouls", "Team xG", "Team nsxG", "Opponent xG", "Opponent nsxG", "Passes"], axis=1)
xg_result = list(results_data["Team xG"])
nsxg_result = list(results_data["Team nsxG"])

goal_data = results_data.drop(
    ["Result", "Goals", "Allowed", "Red Cards",
        "Yellow Cards", "Fouls", "Home/Away", "Opponent", "Opponent xG", "Opponent nsxG", "On Target", "Passes", "Possession", "Shots"], axis=1)
goal_result = list(results_data["Goals"])
allowed_data = list(results_data["Allowed"])


plt.scatter(xg_result, goal_result, lw=0.8, color="r")
plt.scatter(nsxg_result, goal_result, lw=0.8, color='g')
poly = np.poly1d(np.polyfit(xg_result, goal_result, deg=2))
poly2 = np.poly1d(np.polyfit(nsxg_result, goal_result, deg=2))
polyline = np.linspace(0, 5)
plt.plot(polyline, poly(polyline))
plt.plot(polyline, poly2(polyline))
plt.xlabel("xG")
plt.ylabel("Scored")
plt.show()
print(stats.pearsonr(xg_result, goal_result))

print(goal_data)

xGd_train, xGd_test, xGr_train, xGr_test = train_test_split(
    xG_data, nsxg_result, test_size=0.2, random_state=42)

g_train, g_test, gr_train, gr_test = train_test_split(
    goal_data, goal_result, test_size=0.2, random_state=42)

names = xG_data.columns
# current best but only 80% accuracy
rfr = RandomForestRegressor(max_depth=100, max_features='sqrt',
                            min_samples_leaf=3, min_samples_split=2, n_estimators=2000, bootstrap=False)
rfr.fit(xGd_train, xGr_train)
print(sorted(zip(map(lambda x: round(x, 4), rfr.feature_importances_), names), reverse=True))

names = goal_data.columns
gfr = RandomForestClassifier(max_depth=100, max_features='sqrt',
                             min_samples_leaf=3, min_samples_split=2, n_estimators=2000, bootstrap=False)
gfr.fit(g_train, gr_train)
print(sorted(zip(map(lambda x: round(x, 4), gfr.feature_importances_), names), reverse=True))

# random_params = {
#     'bootstrap': [True, False],
#     'max_depth': [60, 80, 100, 120, 140, 160, 180, 200],
#     'max_features': ['sqrt', 'log2', 0.4, 0.5, 0.6],
#     'min_samples_leaf': [1, 2, 3, 5],
#     'min_samples_split': [2, 5, 10],
#     'n_estimators': [200, 400, 600, 800, 1000, 1200, 1500, 1800, 2000]
# }

# grid_params = {
#     'n_estimators': [800, 1800, 2000],
#     'min_samples_split': [2, 10],
#     'min_samples_leaf': [1, 3, 5],
#     'max_features': ['sqrt', 'log2'],
#     'max_depth': [100, 160, 180, 200],
#     'bootstrap': [False]
# }

# rf = RandomForestRegressor()
# rf_grid = RandomizedSearchCV(estimator=rf, param_distributions=random_params, n_iter=20,
#                              scoring='neg_mean_absolute_error', cv=3, verbose=1, n_jobs=-1, return_train_score=True)
# rf_grid.fit(x_train, g_train)
# print(rf_grid.best_params_)

# rf = RandomForestRegressor()
# rf_grid = GridSearchCV(estimator=rf, param_grid=grid_params,
#                        cv=2, verbose=1, n_jobs=-1)
# rf_grid.fit(x_train, g_train)
# print(rf_grid.best_params_)


def evaluate(model, test_features, test_labels):
    print("True Values: ", test_labels)
    predictions = model.predict(test_features)
    print("Pred Values: ", predictions)
    predictions = [x + 1 for x in predictions]
    test_labels = [y + 1 for y in test_labels]
    errors = abs(np.subtract(predictions, test_labels))
    mape = 100 * np.mean(errors / (test_labels))
    accuracy = 100 - mape
    print('Model Performance')
    print('Average Error: {:0.4f} degrees.'.format(np.mean(errors)))
    print('Accuracy = {:0.2f}%.'.format(accuracy))

    return accuracy


rfr_accuracy = evaluate(rfr, xGd_test, xGr_test)
gfr_accuracy = evaluate(gfr, g_test, gr_test)
# best_random = rf_grid.best_estimator_
# random_accuracy = evaluate(best_random, x_test, g_test)
# print(sorted(zip(map(lambda x: round(x, 4),
#       best_random.feature_importances_), names), reverse=True))


# print('Improvement of {:0.2f}%.'.format(
#     100 * (random_accuracy - rfr_accuracy) / rfr_accuracy))
