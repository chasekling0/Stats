# predict matches using models based on SPI and statistics
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.feature_selection import SelectFromModel
from sklearn.model_selection import (GridSearchCV, RandomizedSearchCV,
                                     train_test_split)

from team import Team

# one model for xG from game stats
# one model for nsxG from game stats
# one model for goals from xG, nsxG, SPIs

results_data = pd.read_csv(
    "./StatsFinalData.csv")

results_data = results_data.dropna(axis=1, how='all')

xG_data = results_data.drop(
    ["Team", "Opponent", "Home/Away", "Result", "Goals", "Allowed", "Red Cards",
        "Yellow Cards", "Fouls", "Team xG", "Team nsxG", "Opponent xG", "Opponent nsxG", "Passes"], axis=1)
goal_data = list(results_data["Team xG"])
allowed_data = list(results_data["Allowed"])

x_train, x_test, g_train, g_test = train_test_split(
    xG_data, goal_data, test_size=0.2, random_state=42)

names = xG_data.columns
rfr = RandomForestRegressor()
rfr.fit(x_train, g_train)
print(sorted(zip(map(lambda x: round(x, 4), rfr.feature_importances_), names), reverse=True))

random_params = {
    'bootstrap': [True, False],
    'max_depth': [60, 80, 100, 120, 140, 160, 180, 200],
    'max_features': ['sqrt', 'log2', 0.4, 0.5, 0.6],
    'min_samples_leaf': [1, 2, 3, 5],
    'min_samples_split': [2, 5, 10],
    'n_estimators': [200, 400, 600, 800, 1000, 1200, 1500, 1800, 2000]
}

rf = RandomForestRegressor()
rf_grid = RandomizedSearchCV(estimator=rf, param_distributions=random_params, n_iter=20,
                             scoring='neg_mean_absolute_error', cv=3, verbose=1, n_jobs=-1, return_train_score=True)
rf_grid.fit(x_train, g_train)
print(rf_grid.best_params_)


def evaluate(model, test_features, test_labels):
    print("True Values: ", test_labels)
    predictions = model.predict(test_features)
    print("Predicted Values", predictions)
    predictions = [x + 1 for x in predictions]
    test_labels = [y + 1 for y in test_labels]
    errors = abs(np.subtract(predictions, test_labels))
    mape = 100 * np.mean(errors / (test_labels))
    accuracy = 100 - mape
    print('Model Performance')
    print('Average Error: {:0.4f} degrees.'.format(np.mean(errors)))
    print('Accuracy = {:0.2f}%.'.format(accuracy))

    return accuracy


rfr_accuracy = evaluate(rfr, x_test, g_test)
best_random = rf_grid.best_estimator_
random_accuracy = evaluate(best_random, x_test, g_test)
print(sorted(zip(map(lambda x: round(x, 4),
      best_random.feature_importances_), names), reverse=True))


print('Improvement of {:0.2f}%.'.format(
    100 * (random_accuracy - rfr_accuracy) / rfr_accuracy))
