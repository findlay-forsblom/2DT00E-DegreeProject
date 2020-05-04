#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 14:34:37 2020

@author: findlayforsblom
"""

import numpy as np
from readfiles import ReadFiles
import pandas as pd
from sklearn.model_selection import cross_val_predict

files = ReadFiles(['./Datasets/SnowDepth.csv','./Datasets/Airtemperature.csv', './Datasets/Precipitation.csv', './Datasets/FallAmount.csv', './Datasets/humidity.csv' ])
dataset = files.createDataset()
dataset = dataset[dataset['Temp'] < 10]
X = dataset.iloc[:, [1, 3,4,6,5]].values
y = dataset.iloc[:, 2].values


# Encoding categorical data
df = pd.DataFrame(data=X, columns=['Snow depth', 'Temp', 'dummy', 'Humidity','Precipiattion'])
just_dummies = pd.get_dummies(df['dummy'])

df = pd.concat([df, just_dummies], axis=1)
df.drop(['dummy'], inplace=True, axis=1) 

X = df.iloc[:,].values

# Avoiding the Dummy Variable Trap
X = X[:, :-1]

"""
# Encoding categorical data
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import make_column_transformer

preprocessor = make_column_transformer( (OneHotEncoder(),[2]),remainder="passthrough")
X = preprocessor.fit_transform(X).toarray()
X.get_feature_names()

# Avoiding the Dummy Variable Trap
X = X[:, :-1]
"""
# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 1/3, random_state = 101)


# Fitting Multiple Linear Regression to the Training set
from sklearn.linear_model import LinearRegression
regressor = LinearRegression(fit_intercept= True,normalize= True)
regressor.fit(X_train, y_train)

y_pred = regressor.predict(X_train)
sums = (y_pred - y_train) ** 2
sums = (np.sum(sums)) / len(y_pred)
score = regressor.score(X_train, y_train)
print(f'Training error {round(sums * (10**3),3) }')
print(f'Traning Score {round(score,3)} \n')

prediction = cross_val_predict(regressor, X_train, y_train, cv=5)
sums = (prediction - y_train) ** 2
sums = (np.sum(sums)) / len(prediction)


from sklearn.model_selection import cross_val_score
accuracies = cross_val_score(estimator = regressor, X = X_train, y = y_train, cv = 5)
accuracies.std()

print(f'Validation error {round(sums * (10**3),3) }')
print(f'Validation Score {round(accuracies.mean(),3)}')

from sklearn.externals import joblib
joblib.dump(regressor,'./Models/multipleLinearRegV2' )

import statsmodels.api as sm
X = np.append(arr = np.ones((X.shape[0],1), dtype=np.float).astype(int), values = X, axis=1)
X_opt = X[:,]
X_opt = X_opt.astype(float)
regressor_OLS = sm.OLS(endog = y, exog = X_opt).fit()
regressor_OLS.summary()

X_opt = X[:, [0, 1,2,3,4,10,11,13,15,17,18]]
X_opt = X_opt.astype(float)
regressor_OLS = sm.OLS(endog = y, exog = X_opt).fit()
regressor_OLS.summary()

filtered = df.iloc[:, [0, 1,2,3,4,10,11,13,15,17,18]]

# Predicting the Test set results
y_pred = regressor.predict(X_test)
y_pred = np.round(y_pred, 2)


# Applying Grid Search to find the best model and the best parameters
from sklearn.model_selection import GridSearchCV
parameters = [{'fit_intercept': [True, False], 'normalize': [True, False]}]
grid_search = GridSearchCV(estimator = regressor,
                           param_grid = parameters,
                           cv = 10,
                           n_jobs = -1)
grid_search = grid_search.fit(X_train, y_train)
best_accuracy = grid_search.best_score_
best_parameters = grid_search.best_params_


"""
import pickle 
with open('./Models/multipleLinearReg', 'wb') as f:
    pickle.dump(regressor, f)
"""


"""
sums = (y_pred - y_test) ** 2
sums = round((np.sum(sums)) / len(y_pred), 6)  
print(sums)
"""










