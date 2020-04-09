#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 13:25:18 2020

@author: findlayforsblom
"""

import numpy as np
from readfiles import ReadFiles

files = ReadFiles(['./Datasets/SnowDepth.csv','./Datasets/Airtemperature.csv', './Datasets/Precipitation.csv', './Datasets/FallAmount.csv', './Datasets/humidity.csv' ])
dataset = files.createDataset()
dataset = dataset[dataset['Temp'] < 10]
X = dataset.iloc[:, [1, 3,4,5,6]].values
y = dataset.iloc[:, 2].values

# Encoding categorical data
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer

columnTransformer = ColumnTransformer([('encoder', OneHotEncoder(), [2])], remainder='passthrough')
X = columnTransformer.fit_transform(X).toarray()

# Avoiding the Dummy Variable Trap
X = X[:, 1:]


# Feature Scaling
from sklearn.preprocessing import StandardScaler
sc_X = StandardScaler()
sc_y = StandardScaler()
X = sc_X.fit_transform(X)
y = sc_y.fit_transform(np.reshape(y, (-1,1)))

# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 1/3, random_state = 101)

from sklearn.svm import SVR
polys= []
mse = []
y_test = sc_y.inverse_transform(y_test)
y_test = y_test.flatten()
y_train = y_train.flatten()
regressor = SVR(kernel = 'poly', degree = 10)
regressor.fit(X_train, y_train)

y_pred = regressor.predict(X_test)
y_pred = sc_y.inverse_transform(y_pred)

polys = list(range(1,4))
Cs = np.arange(1,1000, 300)
epsilons = np.arange(0,0.5,0.02)
# Applying Grid Search to find the best model and the best parameters
from sklearn.model_selection import GridSearchCV
parameters = [{'kernel': ['poly', 'linear', 'rbf'], 'degree': polys, 'C': Cs, 'epsilon':epsilons, 'gamma': epsilons }]
grid_search = GridSearchCV(estimator = regressor,
                           param_grid = parameters,
                           cv = 10,
                           n_jobs = -1)
grid_search = grid_search.fit(X_train, y_train)
best_accuracy = grid_search.best_score_
best_parameters = grid_search.best_params_





for k in range(1, 10):
    regressor = SVR(kernel = 'poly', degree = k)
    regressor.fit(X_train, y_train.flatten())
    
    y_pred = regressor.predict(X_test)
    y_pred = sc_y.inverse_transform(y_pred)
      
    sums = (y_pred - y_test) ** 2
    sums = round((np.sum(sums)) / len(y_pred), 6)   
    polys.append(k)
    mse.append(sums)

mse = np.array(mse)      
posmin = mse.argmin()
print(f'{polys[posmin]} with the best k')


regressor = SVR(kernel = 'poly', degree = 7, epsilon = 0.2, gamma = 0.5)
regressor.fit(X_train, y_train.flatten())

y_pred = regressor.predict(X_test)
y_pred = sc_y.inverse_transform(y_pred)
y_pred = np.round(y_pred, 2)
sums = (y_pred - y_test) ** 2
sums = round((np.sum(sums)) / len(y_pred), 6)  
print(sums)

regressor = SVR(kernel = 'rbf', epsilon = 1, gamma = 0.08)
regressor.fit(X_train, y_train.flatten())

y_pred = regressor.predict(X_test)
y_pred = sc_y.inverse_transform(y_pred)
y_pred = np.round(y_pred, 2)
sums = (y_pred - y_test) ** 2
sums = round((np.sum(sums)) / len(y_pred), 6)  
print(sums)

regressor = SVR(kernel = 'linear', epsilon = 0.02, gamma = 0.1)
regressor.fit(X_train, y_train.flatten())

y_pred = regressor.predict(X_test)
y_pred = sc_y.inverse_transform(y_pred)
y_pred = np.round(y_pred, 2)
sums = (y_pred - y_test) ** 2
sums = round((np.sum(sums)) / len(y_pred), 6)  
print(sums)
