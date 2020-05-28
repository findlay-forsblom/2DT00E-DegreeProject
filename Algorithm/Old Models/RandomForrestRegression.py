#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 09:23:42 2020

@author: findlayforsblom
"""


import numpy as np
from readfiles import ReadFiles
from matplotlib import pyplot as plt

files = ReadFiles(['./Datasets/SnowDepth.csv','./Datasets/Airtemperature.csv', './Datasets/Precipitation.csv', './Datasets/FallAmount.csv', './Datasets/humidity.csv' ])
dataset = files.createDataset()
dataset = dataset[dataset['Temp'] < 10]
X = dataset.iloc[:, [1, 3,4,5,6]].values
y = dataset.iloc[:, 2].values


# Encoding categorical data
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import make_column_transformer

preprocessor = make_column_transformer( (OneHotEncoder(),[2]),remainder="passthrough")
X = preprocessor.fit_transform(X).toarray()

# Avoiding the Dummy Variable Trap
X = X[:, 1:]

# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 1/3, random_state = 101)

from sklearn.ensemble import RandomForestRegressor
"""
trees = []
mse = []
for k in range(10, 500, 10):
    regressor = RandomForestRegressor(n_estimators = k, random_state = 0)
    regressor.fit(X_train, y_train)
    
    y_pred = regressor.predict(X_test)
    
    sums = (y_pred - y_test) ** 2
    sums = round((np.sum(sums)) / len(y_pred), 6) 
    trees.append(k)
    mse.append(sums)
    
mse = np.array(mse)      
posmin = mse.argmin()
print(f'{trees[posmin]} has least MSE')
"""

estimators = list(range(10,500, 10))



regressor = RandomForestRegressor(n_estimators = 410, random_state = 0)
regressor.fit(X_train, y_train)

y_pred = regressor.predict(X_test)
y_pred = np.round(y_pred, 2)

sums = (y_pred - y_test) ** 2
sums = round((np.sum(sums)) / len(y_pred), 6) 
print(sums)

from sklearn.model_selection import cross_val_score
accuracies = cross_val_score(estimator = regressor, X = X_train, y = y_train, cv = 10, n_jobs = -1)
accuracies.mean()
accuracies.std()

from sklearn.model_selection import GridSearchCV
parameters = {'n_estimators': estimators, 'max_features': ['auto', 'sqrt', 'log2']}
grid_search = GridSearchCV(estimator = regressor,
                           param_grid = parameters,
                           cv = 10,
                           n_jobs = -1)
grid_search = grid_search.fit(X_train, y_train)
best_accuracy = grid_search.best_score_
best_parameters = grid_search.best_params_


"""
fig3, ax3 = plt.subplots()
err = ax3.plot(trees, mse, label= 'MSE values ')
best = ax3.plot(trees[posmin], mse[posmin], '-o',color = 'red', label= 'Optimal number of Trees')
ax3.legend()
ax3.set_xlabel('No of Trees')
ax3.set_ylabel('MSE value')
ax3.set_title('MSE test error with different Tree values')
"""