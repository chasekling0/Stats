# Chase Kling
# Homework 3
# 10-05-2022

import csv
import math

import matplotlib.pyplot as plt
import pandas as pd


# aggregating data
def aggregate_data(data_list: pd.Series):
    '''creates ranges and values for bins, then returns newly aggregated data'''

    num_bins = 10
    min_val = data_list.min()
    data_range = data_list.max() - min_val
    bin_size = data_range / num_bins

    bin_ranges = [round(min_val + bin_size, 2)]
    bin_values = [round(min_val + (bin_size / 2), 2)]
    for i in range(1, num_bins):
        bin_ranges.append(round(bin_ranges[i - 1] + bin_size, 2))
        bin_values.append(round(bin_values[i - 1] + bin_size, 2))

    new_data = []
    for i, data in enumerate(data_list):
        range_index = 0
        while data > bin_ranges[range_index]:
            range_index += 1
        new_data.append(round(bin_values[range_index], 1))

    return new_data


df = pd.read_csv("Lectures\\Data\\IrisData.csv", sep=",")
sepal_length = df["sepal_length"]
sepal_width = df["sepal_width"]
petal_length = df["petal_length"]
petal_width = df["petal_width"]
species = df["species"]

new_sl = aggregate_data(sepal_length)
new_sw = aggregate_data(sepal_width)
new_pl = aggregate_data(petal_length)
new_pw = aggregate_data(petal_width)

agg_data = open("Lectures\\Data\\NewIrisData.csv",
                'w', encoding="UTF-8", newline='')
writer = csv.writer(agg_data)

headers = ["sepal_length", "sepal_width",
           "petal_length", "petal_width", "species"]
writer.writerow(headers)
for i in range(len(species)):
    new_row = [new_sl[i], new_sw[i], new_pl[i], new_pw[i], species[i]]
    writer.writerow(new_row)

agg_data.close()

# creating PDF and CDF


def get_counts(data: list):
    '''gets counts of values in the data'''
    unique_vals = list(set(data))
    unique_vals.sort()
    counts = []

    for i, uniq in enumerate(unique_vals):
        counts.append(data.count(uniq))

    return [unique_vals, counts]


def create_pdf_cdf(data: list, data_name: str):
    '''creates pdf and cdf to display for the given list of data'''
    pdf_label = "PDF of " + data_name + " data"
    cdf_label = "CDF of " + data_name + " data"
    x_label = data_name + " Bins"

    values, counts = get_counts(data)
    prob = [round(a/len(data), 3) for a in counts]

    plt.bar(values, prob)
    plt.title(pdf_label)
    plt.xlabel(x_label)
    plt.ylabel("P(x)")
    plt.show()

    # adding '0' probability value to start the cdf
    values.insert(0, 0)
    prob.insert(0, 0)
    cum_prob = create_cumsum(values, prob)

    plt.plot(values, cum_prob, '-o')
    plt.title(cdf_label)
    plt.xlabel(x_label)
    plt.ylabel("P(x)")
    plt.show()


def create_cumsum(bin_vals: list, prob: list):
    '''generates array of cumulative probability'''
    new_prob = [0] * len(bin_vals)

    for i, val_prob in enumerate(prob):
        new_prob[i] = val_prob + sum(prob[:i])

    return new_prob


create_pdf_cdf(new_pl, "Petal Length")
create_pdf_cdf(new_pw, "Petal Width")
create_pdf_cdf(new_sl, "Sepal Length")
create_pdf_cdf(new_sw, "Sepal Width")

# Question 3 Probabilities

# P(petal width(x) <= 0.46 units)
count = 0
for i, val in enumerate(new_pw):
    if val <= 0.46:
        count += 1

print("Q3.1: P(x) =", round(count/len(new_pw), 3))

# P(0.46 units <= petal width(x) <= 1.42 units)
count = 0
for i, val in enumerate(new_pw):
    if val >= 0.46 and val <= 1.42:
        count += 1

print("Q3.2: P(x) =", round(count/len(new_pw), 3))

# P(0.5 units <= petal length(x) <= 2.5 units)
count = 0
for i, val in enumerate(new_pl):
    if val >= 0.5 and val <= 3.5:
        count += 1

print("Q3.3: P(x) =", round(count/len(new_pl), 3))
