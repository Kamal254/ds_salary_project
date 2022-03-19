import pandas as pd 
import matplotlib.pyplot as plt 
import numpy as np 
from sklearn.model_selection import train_test_split

dataframe = pd.read_csv('EDA_data.csv')
print(dataframe.columns)
#steps

#Choose relevent column
df_model = dataframe.drop(['Job Description','index', 'Job_country'], axis=1)

#get dummy variable
df_dummy = pd.get_dummies(df_model)
#train test split
x = df_dummy.drop('Salary Estimate', axis=1)
y = df_dummy['Salary Estimate'].values
X_train, X_test, Y_train, Y_test = train_test_split(x, y, test_size=0.2, random_state=42)
#multiple linear regression
import statsmodels.api as sm

X_sm = x = sm.add_constant(x)
model = sm.OLS(y,X_sm)
model.fit().summary()

from sklearn.linear_model import LinearRegression, Lasso
from sklearn.model_selection import cross_val_score


#Here is our linear Regression model
lm = LinearRegression()
lm.fit(X_train, Y_train)
lm_score = np.mean(cross_val_score(lm,X_test,Y_test, cv= 3))
'''score is 66.50'''


#lasso regression

lm_l = Lasso(alpha=.1)
lm_l.fit(X_train,Y_train)
lm_l_score = np.mean(cross_val_score(lm_l,X_train,Y_train,cv= 3))
'''Our lasso model gives 87 score at alpha=.13'''
#lets run our lasso model in .1 to 10 value of alpha
alpha = []
score = []
for i in range(1,100):
    alpha.append(i/10)
    lml = Lasso(alpha=(i/10))
    score.append(np.mean(cross_val_score(lml,X_train,Y_train,cv= 3)))
'''so we are getting 87 score at alpha=.1'''
plt.plot(alpha,score)
scr = tuple(zip(alpha,score))
df_scr = pd.DataFrame(scr, columns = ['alpha','score'])
df_scr[df_scr.score== max(df_scr.score)]


#random forest

from sklearn.ensemble import RandomForestRegressor
rf = RandomForestRegressor()
rf.fit(X_train, Y_train)
rf_score = rf.score(X_test, Y_test)
'''As we can see our score is approx 94'''

#print(np.mean(cross_val_score(rf, X_train,Y_train,cv=3)))
#print(np.mean(cross_val_score(rf, X_test,Y_test,cv=3)))

#tunning models GridsearchCV
from sklearn.model_selection import GridSearchCV
parameters = {'n_estimators':range(10,300,10), 'criterion':('mse','mae'), 'max_features':('auto','sqrt','log2')}
gs = GridSearchCV(rf,parameters,cv=3)
gs.fit(X_train,Y_train)
gs.best_score_
gs.best_estimator_

#test ensembles

tpred_lm = lm.predict(X_test)
tpred_lml = lm_l.predict(X_test)
tpred_rf = gs.best_estimator_.predict(X_test)

from sklearn.metrics import mean_absolute_error
mean_absolute_error(Y_test,tpred_lm)
mean_absolute_error(Y_test,tpred_lml)
mean_absolute_error(Y_test,tpred_rf)

mean_absolute_error(Y_test,(tpred_lm+tpred_rf)/2)

import pickle
pickl = {'model' : gs.best_estimator_}
pickle.dump(pickl, open('model_file'+".p","wb"))

file_name = "model_file.p"
with open(file_name, 'rb') as pickled:
    data = pickle.load(pickled)
    model = data['model']

print(model.predict(np.array(list(X_test.iloc[1,:])).reshape(1,-1))[0])

list(X_test.iloc[1,:])
