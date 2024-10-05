import pandas as pd
from pandas.core.frame import DataFrame
import numpy as np

dat: DataFrame = pd.read_excel('ferguson2024.xlsx', sheet_name="Results")
dat = dat[dat['d'].notna()]
print(dat[["Citation", "n", "d"]].head())


# TODO use exact formula
def correct_d_bias(d, n):
    """
    Corrects Cohen's d using the Borenstein approximation
    for small sample bias.

    :param d: Cohen's d value.
    :param n: Total sample size.
    :return:  Bias-corrected Cohen's d value.
    """
    if n <= 2:
        return d
    correction_factor = 1 - (3 / (4 * (n - 2) - 1))
    return d * correction_factor


# https://cran.r-project.org/web/packages/psychmeta/psychmeta.pdf
def var_error_d(d, n1, n2=np.nan, correct_bias=True):
    """
    Estimates the error variance of standardized mean
    differences (Cohen’s d values).

    :param d:            Vector of Cohen’s d values.
    :param n1:           Vector of sample sizes from group 1.
                         (or the total sample size with the assumption
                         that groups are of equal size)
    :param n2:           Vector of sample sizes from group 2. Defaults to NaN.
    :param correct_bias: If True, corrects for small-sample bias.
                         Defaults to True.
    :return:             Estimated error variance of Cohen’s d.
    """
    if np.isnan(n2):  # TODO: for diff n
        n = n1
    else:
        raise NotImplementedError("Not implemented!")
    if correct_bias:
        d = correct_d_bias(d, n)
    factor = (n-1)/(n-3)

    variance = (4/n) * (1 + (d ** 2)/8)

    return factor*variance


dat['v'] = dat.apply(lambda row: var_error_d(d=row['d'], n1=row['n']), axis=1)
print(dat[["Citation", "n", "d", "v"]].head())
