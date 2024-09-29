import pandas as pd
from pandas.core.frame import DataFrame, Series
import statistics
from scipy import stats
import numpy as np

teams: DataFrame = pd.read_csv('teams.csv')
height: DataFrame = teams[["height"]]


# skew
def skewness(data: Series):
    data_mean = data.mean().item()
    stdev = statistics.stdev(data)
    sum = 0
    for i in data.values.flatten():
        sum += (i - data_mean)**3
    return sum / (data.size * (stdev**3))


print(skewness(height['height']))
print(height.skew(axis=0))


# kurtosis
def kurtosis(data: Series):
    data_mean = data.mean().item()
    stdev = statistics.stdev(data)
    sum = 0
    for i in data.values.flatten():
        sum += (i - data_mean)**4
    return sum / (data.size * (stdev**4)) - 3


print(kurtosis(height['height']))
print(height.kurtosis(axis=0))
print("Pandas: ", height.kurtosis())
print("Fischer: ", stats.kurtosis(height, fisher=True))
print("Pearson: ", stats.kurtosis(height, fisher=False))


# describe
print(height.describe())
print(height['height'].describe())
print(teams.describe(include='all'))

teams['tall'] = np.where(teams['height'] > 185, True, False)
print(teams['tall'].describe())
