import pandas as pd
import matplotlib.pyplot as plt


def filter_data():
    gss_data = pd.read_stata("gss7222_r3.dta", convert_categoricals=False)
    data = gss_data[["year", "age", "sex", "numwomen", "nummen", "wtssps"]]
    data.to_csv('gss_data.csv')


def calculate():
    gss_data = pd.read_csv("gss_data.csv")
    filtered_data = gss_data[
            (gss_data['age'] >= 18) & (gss_data['age'] < 30)
            & gss_data['sex'].isin([1, 2])
        ].dropna(subset=['numwomen', 'nummen'])

    filtered_data['virgin'] = filtered_data.apply(
        lambda row: row['numwomen'] == 0 if row['sex'] == 1 else row['nummen'] == 0,
        axis=1
    )

    grouped_data = filtered_data.groupby(['year', 'sex', 'virgin']).size().reset_index(name='count')

    grouped_data['pct'] = grouped_data.groupby(['year', 'sex'])['count'].transform(lambda x: x / x.sum() * 100)

    virgin_data = grouped_data[grouped_data['virgin'] == True]

    virgin_data['sex'] = virgin_data['sex'].map({1: 'Male', 2: 'Female'})

    plt.figure(figsize=(10, 6))
    for sex in virgin_data['sex'].unique():
        sex_data = virgin_data[virgin_data['sex'] == sex]
        plt.plot(sex_data['year'], sex_data['pct'], marker=None, label=sex, linewidth=3)

    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.yaxis.grid(True)
    ax.xaxis.set_ticks_position('none')

    # plt.xlabel('Year')
    plt.title('Share of individuals under age 30 who report zero opposite sex sexual partners since they turned 18.')
    # plt.suptitle('Source: General Social Survey')
    plt.legend(title='Sex')
    plt.grid(True, axis='y')
    plt.figtext(0.01, 0.01, 'Source: General Social Survey')
    plt.show()


filter_data()
