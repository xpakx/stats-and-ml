import pandas as pd
import matplotlib.pyplot as plt


def prefilter_data():
    gss_data = pd.read_stata("gss7222_r3.dta", convert_categoricals=False)
    data = gss_data[["year", "age", "sex", "numwomen", "nummen", "wtssps"]]
    data.to_csv('gss_data.csv')


def filter_data(data):
    return data[
            (data['age'] >= 18) & (data['age'] < 30)
            & (data['sex'].isin([1, 2]))
        ].dropna(subset=['numwomen', 'nummen'])


def calculate(data):
    data['virgin'] = data.apply(
        lambda row: row['numwomen'] == 0 if row['sex'] == 1 else row['nummen'] == 0,
        axis=1
    )

    grouped_data = data.groupby(['year', 'sex', 'virgin']).apply(
        lambda x: pd.Series({
            'count': x['wtssps'].sum()
        }), include_groups=False
    ).reset_index()

    grouped_data['pct'] = grouped_data.groupby(['year', 'sex'])['count'].transform(lambda x: x / x.sum() * 100)

    virgin_data = grouped_data[grouped_data['virgin']]
    virgin_data['sex'] = virgin_data['sex'].map({1: 'Male', 2: 'Female'})
    return virgin_data


def plot(virgin_data, exclude=None):
    plt.figure(figsize=(10, 6))
    for sex in virgin_data['sex'].unique():
        if sex == exclude:
            continue
        sex_data = virgin_data[virgin_data['sex'] == sex]
        plt.plot(sex_data['year'], sex_data['pct'], marker=None, label=sex, linewidth=3)

    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.yaxis.grid(True)
    ax.xaxis.set_ticks_position('none')
    plt.ylim(0, 30)

    plt.title('Share of individuals under age 30 who report zero opposite sex sexual partners since they turned 18.')
    if not exclude:
        plt.legend(title='Sex')
    plt.grid(True, axis='y')
    plt.figtext(0.01, 0.01, 'Source: General Social Survey')
    plt.show()


raw_data = pd.read_csv("gss_data.csv")
filtered_data = filter_data(raw_data)
data = calculate(filtered_data)
plot(data)
