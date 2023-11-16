import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from scipy.stats import pearsonr
from sklearn.metrics import mean_absolute_error
import mplcatppuccin
import matplotlib as mpl

teams = pd.read_csv('teams.csv')
teams = teams[["team", "year", "age", "athletes", "prev_medals", "prev_3_medals", "medals"]]
teams['age_d25'] = (teams['age'] - 25.0).abs()
teams = teams.dropna()
print(teams.corr(numeric_only=True)['medals'])

sns.set_theme()
mpl.style.use("mocha")
color = mplcatppuccin.palette.load_color("mocha", "flamingo")

plot = sns.lmplot(x='athletes', y='medals', line_kws={"color": color}, data=teams, fit_reg=True, ci=95)
plot.set(xlabel='Athletes', ylabel='Current medals')
plot = sns.lmplot(x='prev_medals', y='medals',  line_kws={"color": color}, data=teams, fit_reg=True, ci=95)
plot.set(xlabel='Athletes', ylabel='Medals in last event')
plot = sns.lmplot(x='prev_3_medals', y='medals', line_kws={"color": color},  data=teams, fit_reg=True, ci=95)
plot.set(xlabel='Athletes', ylabel='Medals two events ago')
sns.despine()

teams.plot.hist(y="medals")
# sns.histplot(x='medals', data=teams)
plt.show()

print(pearsonr(teams['medals'], teams['athletes']))
print(pearsonr(teams['medals'], teams['prev_medals']))
print(pearsonr(teams['medals'], teams['prev_3_medals']))
print(pearsonr(teams['medals'], teams['age']))
print(pearsonr(teams['medals'], teams['age_d25']))

train = teams[teams["year"] < 2012].copy()
test = teams[teams["year"] >= 2012].copy()
print(train.shape)
print(test.shape)

reg = LinearRegression()
predictors = ['athletes', 'prev_medals', 'prev_3_medals', 'age_d25']
target = 'medals'

reg.fit(train[predictors], train[target])
predictions = reg.predict(test[predictors])
test["predictions"] = predictions
test.loc[test["predictions"] < 0, "predictions"] = 0
test["predictions"] = test["predictions"].round()

print(test[test["team"] == "USA"])
print(test[test["team"] == "IND"])
print(test[test["team"] == "POL"])

error = mean_absolute_error(test["medals"], test["predictions"])
print(error)
