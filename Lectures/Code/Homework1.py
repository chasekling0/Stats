# Chase Kling
# 09-07-2022

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

df = pd.read_csv(
    "C:/Users/chase/OneDrive/Documents/Stats/Lectures/Data/Leaves.csv")

linden = df.loc[(df["Name"] == "Legend American Linden")]
linden_length = linden["Leaf_Length"]
linden_width = linden["Leaf_Width"]

maple = df.loc[(df["Name"] == "Schlesinger Red Maple")]
maple_length = maple["Leaf_Length"]
maple_width = maple["Leaf_Width"]

sweet_gum = df.loc[(df["Name"] == "Moraine Sweet Gum")]
sweet_gum_length = sweet_gum["Leaf_Length"]
sweet_gum_width = sweet_gum["Leaf_Width"]

all_length = df["Leaf_Length"]
all_width = df["Leaf_Width"]

num_bins = 5


def print_stats(sample_list, name):
    sample_array = np.asarray(sample_list)
    print(name, ":")
    print("Mean: ", round(sample_array.mean(), 3))
    print("Median: ", round(np.median(sample_array), 3))
    print("Range: ", round(sample_array.max() - sample_array.min(), 3))
    print("Variance: ", round(sample_array.var(), 3))
    print("Standard Deviation: ", round(np.std(sample_array), 3))
    print()


# length histograms
lhists, ((lhist1, lhist2), (lhist3, lhist4)) = plt.subplots(2, 2)

lhist1.hist(all_length, num_bins)
lhist1.set_xlabel('All Leaves')
lhist1.set_ylabel('Count')

lhist2.hist(linden_length, num_bins)
lhist2.set_xlabel('Legend American Linden')
lhist2.set_ylabel('Count')

lhist3.hist(maple_length, num_bins)
lhist3.set_xlabel("Schlesinger Red Maple")
lhist3.set_ylabel('Count')

lhist4.hist(sweet_gum_length, num_bins)
lhist4.set_xlabel("Moraine Sweet Gum")
lhist4.set_ylabel('Count')

lhists.suptitle("Leaf Length (cm)")
lhists.set_figheight(3.5)
lhists.tight_layout()
plt.show()

# width histograms
whists, ((whist1, whist2), (whist3, whist4)) = plt.subplots(2, 2)

whist1.hist(all_width, num_bins)
whist1.set_xlabel('All Leaves')
whist1.set_ylabel('Count')

whist2.hist(linden_width, num_bins)
whist2.set_xlabel('Legend American Linden')
whist2.set_ylabel('Count')

whist3.hist(maple_width, num_bins)
whist3.set_xlabel("Schlesinger Red Maple")
whist3.set_ylabel('Count')

whist4.hist(sweet_gum_width, num_bins)
whist4.set_xlabel("Moraine Sweet Gum")
whist4.set_ylabel('Count')

whists.suptitle("Leaf Width (cm)")
whists.set_figheight(3.5)
whists.tight_layout()
plt.show()

# length boxplots
species_names = ["All Leaves", "Linden",
                 "Red Maple", "Sweet Gum"]
species_data = [all_length, linden_length, maple_length, sweet_gum_length]
lbpfig, lbpaxis = plt.subplots(figsize=(7, 5))

boxplots = lbpaxis.boxplot(species_data)
lbpaxis.set_xticklabels(species_names)
lbpaxis.set(
    title="Leaf Lengths (cm)",
    xlabel="Tree Species",
    ylabel="Length of Leaf (cm)"
)

plt.tight_layout()
plt.show()

# width boxplots
species_names = ["All Leaves", "Linden",
                 "Red Maple", "Sweet Gum"]
species_data = [all_width, linden_width, maple_width, sweet_gum_width]
wbpfig, wbpaxis = plt.subplots(figsize=(7, 5))

boxplots = wbpaxis.boxplot(species_data)
wbpaxis.set_xticklabels(species_names)
wbpaxis.set(
    title="Leaf Widths (cm)",
    xlabel="Tree Species",
    ylabel="Width of Leaf (cm)"
)

plt.tight_layout()
plt.show()

# scatterplot
linden_scatter = plt.scatter(linden_width, linden_length, c='g',
                             label="Legend American Linden")
maple_scatter = plt.scatter(
    maple_width, maple_length, c='r', label="Schlesinger Red Maple")
moraine_scatter = plt.scatter(sweet_gum_width, sweet_gum_length,
                              c='b', label="Moraine Sweet Gum")

plt.xlabel("Leaf Width (cm)")
plt.ylabel("Leaf Length (cm)")
plt.title("Leaf Width by Length")
plt.legend(loc="lower right")

plt.show()

# Leaf Stats
# print_stats(linden_length, "Linden Length")
# print_stats(linden_width, "Linden Width")
# print_stats(maple_length, "Maple Length")
# print_stats(maple_width, "Maple Width")
# print_stats(sweet_gum_length, "Sweet Gum Width")
# print_stats(sweet_gum_width, "Sweet Gum Length")
print_stats(all_length, "All Length")
print_stats(all_width, "All Width")

# Book Problem
sample = [542, 542, 543, 538, 539, 545, 535, 540]
print_stats(sample, "Book Problem")
