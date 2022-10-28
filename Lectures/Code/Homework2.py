# Chase Kling
# Homework 2
# 09-13-2022

import random
import matplotlib.pyplot as plt


def DiceRollSimulator(numDice, numSides, numRolls):
    dice_roll_total = []

    rolls = 0
    dice = 0

    while rolls < numRolls:
        total = 0
        while dice < numDice:
            total += random.randint(1, numSides)
            dice += 1
        dice_roll_total.append(total)
        rolls += 1
        dice = 0

    return (dice_roll_total)


numD = int(input("Enter the number of dice you wish to roll:"))
numS = int(input("Enter the number of sides each dice has:"))
numR = int(input("Enter the number of rolls you wish to simulate:"))

x = DiceRollSimulator(numD, numS, numR)

plt.hist(x, bins=numS)
plt.ylabel("Count")
plt.xlabel("Sum of the Rolls")
plt.title(f"Histogram of {numD}d{numS} Rolled {numR} Times")
plt.tight_layout()
plt.show()
