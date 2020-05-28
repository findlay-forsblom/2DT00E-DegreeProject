#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  4 20:49:31 2020

@author: findlayforsblom
"""

import numpy as np
from readFiles2 import ReadFiles
import pandas as pd
from sklearn.model_selection import cross_val_predict
from sklearn.model_selection import cross_val_score

files = ReadFiles(['./Datasets/SnowDepth.csv','./Datasets/Airtemperature.csv', './Datasets/Precipitation.csv', './Datasets/FallAmount.csv', './Datasets/humidity.csv' ])
dataset = files.createDataset()
ind = list(range(3,21))
ind.insert(0, 1)
X = dataset.iloc[:, ind].values
y = dataset.iloc[:, 2].values

# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 1/3, random_state = 101)

from sklearn.tree import DecisionTreeRegressor
dt = DecisionTreeRegressor(random_state=0)

from sklearn.model_selection import GridSearchCV
parameters = {'max_depth':[10, 6, 20],
              'max_features':['sqrt','auto', 'log2', None, 2, 500, 100]}
grid_search = GridSearchCV(estimator = dt,
                           param_grid = parameters,
                           cv = 5,
                           n_jobs = -1,
                           verbose = 1,
                           scoring = 'neg_mean_squared_error' )
grid_search = grid_search.fit(X_train, y_train)
best_accuracy = grid_search.best_score_
best_parameters = grid_search.best_params_

dt = DecisionTreeRegressor(random_state=0, max_features = 'auto', max_depth =6 )
dt.fit(X_train, y_train)
y_pred = dt.predict(X_train)
score = dt.score(X_train, y_train) 

sums = (y_pred - y_train) ** 2
sums = (np.sum(sums)) / len(y_pred)

print(f'Training error {round(sums * (10**3),3) }')
print(f'Traning Score {round(score,3)} \n')

prediction = cross_val_predict(dt, X_train, y_train, cv=5)
sums = (prediction - y_train) ** 2
sums = (np.sum(sums)) / len(prediction)


from sklearn.model_selection import cross_val_score
accuracies = cross_val_score(estimator = dt, X = X_train, y = y_train, cv = 5)

print(f'Validation error {round(sums * (10**3),3) }')
print(f'Validation Score {round(accuracies.mean(),3)} \n')
