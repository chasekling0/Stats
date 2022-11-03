import numpy as np
import pandas as pd
from keras.layers import Dense
from keras.models import Sequential
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

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
        "Yellow Cards", "Fouls", "Team xG", "Team nsxG", "Opponent xG", "Opponent nsxG", "Passes", "Team", "Opponent"], axis=1)
xG_features = xG_features.values
xG_results = np.asarray(results_data["Team xG"])
xG_results = xG_results.reshape(-1, 1)

predictor_scaler = StandardScaler()
result_scaler = StandardScaler()

ps_fit = predictor_scaler.fit(xG_features)
rs_fit = result_scaler.fit(xG_results)

xG_features = ps_fit.transform(xG_features)
xG_results = rs_fit.transform(xG_results)

x_train, x_test, y_train, y_test = train_test_split(
    xG_features, xG_results, test_size=0.2)

model = Sequential()
model.add(Dense(units=6, input_dim=6, kernel_initializer='normal',
          activation='relu'))
model.add(Dense(units=6, kernel_initializer='normal', activation='tanh'))
model.add(Dense(1, kernel_initializer='normal'))
model.compile(loss='mean_squared_error', optimizer='adam')
model.fit(x_train, y_train, batch_size=30, epochs=1000, verbose=1)

predictions = model.predict(x_test)
predictions = rs_fit.inverse_transform(predictions)
y_test_orig = rs_fit.inverse_transform(y_test)
ape = 100*(abs(y_test_orig - predictions)/y_test_orig)
mape = 100 - np.mean(ape)

print("Real Values: ", y_test_orig)
print("Predicted Values: ", predictions)
print("Accuracy: ", mape)
