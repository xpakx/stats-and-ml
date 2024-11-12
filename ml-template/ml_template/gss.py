import pandas as pd


def filter_data():
    gss_data = pd.read_stata("gss7222_r3.dta", convert_categoricals=False)
    data = gss_data[["year", "age", "sex", "numwomen", "nummen", "wtssps"]]
    data.to_csv('gss_data.csv')

filter_data()
