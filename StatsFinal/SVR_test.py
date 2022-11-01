import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.svm import SVR

results_data = pd.read_csv(
    "./StatsFinalData.csv")

x_data = results_data.drop(["Team", "Opponent", "Home/Away", "Result"], axis=1)
y_data = results_data["Goals"]

svr_rbf = SVR(kernel='rbf', C=100, gamma=0.1, epsilon=0.1)
svr_lin = SVR(kernel='linear', C=100, gamma='auto')
svr_poly = SVR(kernel='poly', C=100, gamma='auto',
               degree=3, epsilon=0.1, coef0=1)

lw = 2
svrs = [svr_rbf, svr_lin, svr_poly]
kernel_label = ["RBF", "Linear", "Polynomial"]
model_color = ['m', 'c', 'g']

fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(15, 10), sharey=True)
for ix, svr in enumerate(svrs):
    axes[ix].plot(
        x_data,
        svr.fit(x_data, y_data).predict(x_data),
        color=model_color[ix],
        lw=lw,
        label="{} model".format(kernel_label[ix]),
    )
    axes[ix].legend(
        loc='upper center',
        bbox_to_anchor=(0.5, 1.1),
        ncol=1,
        fancybox=True,
        shadow=True,
    )
fig.text(0.5, 0.04, 'data', ha='center', va='center')
fig.text(0.06, 0.5, 'target', ha='center', va='center', rotation='vertical')
fig.suptitle("Support Vector Regression", fontsize=14)
plt.show()
