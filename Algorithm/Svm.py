#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  3 09:28:56 2020

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

# Feature Scaling
from sklearn.preprocessing import StandardScaler
sc_X = StandardScaler()
sc_y = StandardScaler()
X = sc_X.fit_transform(X)
y = sc_y.fit_transform(np.reshape(y, (-1,1))).ravel()

# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 1/3, random_state = 101)

from sklearn.svm import SVR
# Applying Grid Search to find the best model and the best parameters
svr = SVR()
from sklearn.model_selection import GridSearchCV
parameters = [{'kernel': ['poly'], 'C': [0.005, 0.05, 1], 
               'epsilon':[0.2, 0.09, 0.1],
               'coef0': [0, 0.05, 1 ],
               'tol':[1e-3, 1e-5, 1e-1],
               'gamma': ['scale', 'auto', 0.05, 0.5], 
               'degree': [1,2,3]}]

grid_search = GridSearchCV(estimator = svr,
                           param_grid = parameters,
                           cv = 5,
                           n_jobs = -1)
grid_search = grid_search.fit(X_train, y_train)
best_accuracy = grid_search.best_score_
best_parameters = grid_search.best_params_

#Fitting best linear parameters 
svr = SVR(kernel = 'linear', C = 0.005, epsilon = 0.1 )
svr.fit(X_train, y_train)
score = svr.score(X_train, y_train)
prediction = cross_val_predict(svr, X_train, y_train, cv=5)
accuracies = cross_val_score(estimator = svr, X = X_train, y = y_train, cv = 5)
y_pred = svr.predict(X_train)
y_pred = sc_y.inverse_transform(y_pred)
y_train = sc_y.inverse_transform(y_train)
sums = (y_pred - y_train) ** 2
sums = (np.sum(sums)) / len(y_pred)
print(f'Training error {round(sums * (10**3),3) }')
print(f'Traning Score {round(score,3)} \n')

prediction = sc_y.inverse_transform(prediction)
sums = (prediction - y_train) ** 2
sums = (np.sum(sums)) / len(prediction)
print(f'Validation error {round(sums * (10**3),3) }')
print(f'Validation Score {round(accuracies.mean(),3)} \n') 


