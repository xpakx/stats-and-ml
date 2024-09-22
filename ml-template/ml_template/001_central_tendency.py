import pandas as pd
from pandas.core.frame import DataFrame
from numpy import ndarray
import numpy as np
from scipy import stats

teams: DataFrame = pd.read_csv('teams.csv')
sorted_teams: DataFrame = teams.sort_values(by='age')
age: DataFrame = sorted_teams[["age"]]

print("Mean")
print(age.mean())
print("Mean (5 youngest)")
print(age[0:5].mean())

print("Median")
print(age.median())

print("Mode")
print(age.mode())


dataset: ndarray = np.array([-15, 2, 3, 4, 5, 6, 7, 8, 9, 12])
print(dataset.mean())
print(stats.trim_mean(dataset, 0.1))


print("10% trimmed mean")
print(stats.trim_mean(age, .1))

print(sorted_teams.head(5))
print(age.value_counts().head(10))
print(age.value_counts().max())
