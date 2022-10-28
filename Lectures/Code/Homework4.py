# Chase Kling
# 11-02-2022
# Homework 4

import random

import matplotlib.pyplot as plt

# defining functions to do simulation and creating the histogram


def grab_bag(list_bag, num_samples, num_data_points):
    '''function to simulate the averages when selecting from a bag of values'''
    means = []

    # runs number for number of data points, calculates means of numSamples from the bag
    for time in range(num_data_points):
        current = 0
        for sample in range(num_samples):
            current += list_bag[random.randint(0, len(list_bag) - 1)]
        means.append(current / num_samples)

    return means


def plot_histogram(meansList, numSamples):
    '''function to plot the histogram of a resulting sample'''
    plt.hist(meansList, bins=13)
    plt.xlabel("Means")
    plt.ylabel("Counts")
    plt.title("CLT Simulation (" + str(numSamples) + " samples)")
    plt.show()


# initializing the constant values needed for the simulation

values = [1, 2, 2, 2, 3, 5, 6, 6, 6, 7]
num_s = 40
num_dp = 5000

# running simulation and plotting results

x = grab_bag(values, num_s, num_dp)
plot_histogram(x, num_s)
