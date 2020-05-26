#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  4 20:23:52 2020

@author: findlayforsblom
"""

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

# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 1/3, random_state = 101)

from sklearn.neighbors import KNeighborsRegressor
neigh = KNeighborsRegressor()

from sklearn.model_selection import GridSearchCV
parameters = [{'n_neighbors': [10, 60, 70]}]

grid_search = GridSearchCV(estimator = neigh,
                           param_grid = parameters,
                           cv = 5,
                           n_jobs = -1,
                           verbose = 1)
grid_search = grid_search.fit(X_train, y_train)
best_accuracy = grid_search.best_score_
best_parameters = grid_search.best_params_


neigh = KNeighborsRegressor(n_neighbors = 60)
neigh.fit(X_train, y_train)
score = neigh.score(X_train, y_train)