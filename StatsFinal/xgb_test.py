import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn.datasets import load_boston
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import KFold, cross_val_score, train_test_split

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

xG_features = results_data.drop(
    ["Result", "Goals", "Allowed", "Red Cards",
        "Yellow Cards", "Fouls", "Team xG", "Team nsxG", "Opponent xG", "Opponent nsxG"], axis=1)
xG_results = results_data["Team xG"]

x_train, x_test, y_train, y_test = train_test_split(
    xG_features, xG_results, test_size=0.20)

model = xgb.XGBRegressor(verbosity=0, objective='reg:squarederror',
                         max_depth=20, learning_rate=0.1, n_estimators=1000, subsamble=0.6)
print(model)


model.fit(x_train, y_train)
score = model.score(x_train, y_train)
names = xG_features.columns
print(sorted(zip(map(lambda x: round(x, 4), model.feature_importances_), names), reverse=True))

print("Training score: ", score)

# - cross validataion
scores = cross_val_score(model, x_train, y_train, cv=5)
print("Mean cross-validation score: %.2f" % scores.mean())

kfold = KFold(n_splits=10, shuffle=True)
kf_cv_scores = cross_val_score(model, x_train, y_train, cv=kfold)
print("K-fold CV average score: %.2f" % kf_cv_scores.mean())

ypred = model.predict(x_test)
mse = mean_squared_error(y_test, ypred)
print("MSE: %.2f" % mse)
print("RMSE: %.2f" % (mse**(1/2.0)))

x_ax = range(len(y_test))
plt.plot(x_ax, y_test, lw=0.9, color="blue", label="original")
plt.plot(x_ax, ypred, lw=0.8, color="red", label="predicted")
plt.legend()
plt.show()
