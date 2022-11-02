# correlate team statistics to their SPI ranking
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV, train_test_split

from team import Team

results_data = pd.read_csv(
    "./StatsFinalData.csv")
team_names = results_data["Team"].unique()
team_objects = {}
for i, team_name in enumerate(team_names):
    results = results_data.loc[(
        results_data["Team"] == team_name)].dropna(axis=1, how='all').reset_index()
    opp_results = results_data.loc[(
        results_data["Opponent"] == team_name)].dropna(axis=1, how='all').reset_index()
    team_objects[team_name] = Team(team_name, results, opp_results)

team_spi = {
    "Bournemouth": 54.99,
    "Arsenal": 84.74,
    "Aston Villa": 69.99,
    "Brentford": 66.69,
    "Brighton": 78.69,
    "Chelsea": 82.44,
    "Crystal Palace": 68.18,
    "Everton": 64.01,
    "Fulham": 61.51,
    "Leeds": 65.27,
    "Leicester": 68.4,
    "Liverpool": 86.58,
    "Manchester City": 92.89,
    "Manchester United": 80.54,
    "Newcastle": 79.29,
    "Nottingham": 53.95,
    "Southampton": 62.85,
    "Spurs": 79.86,
    "West Ham": 75.1,
    "Wolves": 64.61
}

x_data = pd.DataFrame()
y_data = []

for i, name in enumerate(team_names):
    attributes = pd.DataFrame([team_objects[name].attributes])
    x_data = pd.concat([x_data, attributes])
    y_data.append(team_spi[name])

x_train, x_test, y_train, y_test = train_test_split(
    x_data, y_data, test_size=0.2, random_state=42)

# base fit
rfr = RandomForestRegressor(bootstrap=False, max_depth=120, max_features=0.5,
                            min_samples_leaf=2, min_samples_split=5, n_estimators=1000)
rfr.fit(x_train, y_train)

# optimization
random_params = {
    'bootstrap': [False],
    'max_depth': [150, 160],
    'max_features': ['sqrt', 'log2', 0.6],
    'min_samples_leaf': [2],
    'min_samples_split': [5],
    'n_estimators': [900, 1000]
}

rf = RandomForestRegressor()
rf_grid = GridSearchCV(estimator=rf, param_grid=random_params,
                       cv=3, verbose=1, n_jobs=-1)
rf_grid.fit(x_train, y_train)
print(rf_grid.best_params_)


def evaluate(model, test_features, test_labels):
    print("True Values: ", test_labels)
    predictions = model.predict(test_features)
    print("Predicted Values", predictions)
    errors = abs(predictions - test_labels)
    mape = 100 * np.mean(errors / test_labels)
    accuracy = 100 - mape
    print('Model Performance')
    print('Average Error: {:0.4f} degrees.'.format(np.mean(errors)))
    print('Accuracy = {:0.2f}%.'.format(accuracy))

    return accuracy


rfr_accuracy = evaluate(rfr, x_test, y_test)
best_random = rf_grid.best_estimator_
random_accuracy = evaluate(best_random, x_test, y_test)

print('Improvement of {:0.2f}%.'.format(
    100 * (random_accuracy - rfr_accuracy) / rfr_accuracy))
