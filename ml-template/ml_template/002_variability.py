import pandas as pd
from pandas.core.frame import DataFrame
import numpy as np
from scipy import stats
from statsmodels import robust
import statistics
import math

teams: DataFrame = pd.read_csv('teams.csv')
height: DataFrame = teams[["height"]]

print("Max")
print(height.max())
print("Min")
print(height.min())

# quantiles
print(np.quantile(height, .5))
print(np.quantile(height, .9))
print(np.quantile(height, [.25, .75]))

# interquantile range
quantiles = np.quantile(height, [.25, .75])
print(quantiles[1] - quantiles[0])
print(stats.iqr(height))


# mean absolute deviation
def aad(data: DataFrame):
    data_mean = data.mean().item()
    abs_deviations = []
    for i in data.values.flatten():
        abs_deviations.append(abs(i - data_mean))
    return sum(abs_deviations) / len(abs_deviations)


print(aad(height))
print(abs(height - height.mean()).mean())


# median absolute deviation
def mad(data: DataFrame):
    data_mean = data.median().item()
    abs_deviations = []
    for i in data.values.flatten():
        abs_deviations.append(abs(i - data_mean))
    return sum(abs_deviations) / len(abs_deviations)


print(mad(height))
print(abs(height - height.median()).mean())
robust.mad(height, c=1)


# variance (s²)
def variance(data: DataFrame):
    data_mean = data.mean().item()
    sum = 0
    for i in data.values.flatten():
        sum += (i - data_mean)**2
    return sum / data.size


def variance2(data: DataFrame):
    data_mean = data.mean().item()
    sum = 0
    for i in data.values.flatten():
        sum += (i - data_mean)**2
    return sum / (data.size - 1)


print(variance(height))
print(statistics.variance(height['height']))
print(variance2(height))
print(statistics.pvariance(height['height']))

# standard deviation (s)
print(math.sqrt(variance(height)))
print(statistics.pstdev(height['height']))
print(math.sqrt(variance2(height)))
print(statistics.stdev(height['height']))
