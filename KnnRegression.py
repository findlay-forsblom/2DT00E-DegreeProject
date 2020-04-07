#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 09:12:39 2020

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
from sklearn.compose import make_column_transformer

preprocessor = make_column_transformer( (OneHotEncoder(),[2]),remainder="passthrough")
X = preprocessor.fit_transform(X).toarray()

# Avoiding the Dummy Variable Trap
X = X[:, 1:]

# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 1/3, random_state = 101)

from sklearn.neighbors import KNeighborsRegressor
testks = []
mse = []
for k in range(1, 25, 2):
    neigh = KNeighborsRegressor(n_neighbors=k)
    neigh.fit(X_train, y_train)
    
    y_pred = neigh.predict(X_test)
    
    sums = (y_pred - y_test) ** 2
    sums = round((np.sum(sums)) / len(y_pred), 6)    
    testks.append(k)
    mse.append(sums)
    
mse = np.array(mse)      
posmin = mse.argmin()
print(f'{testks[posmin]} with the best k')

neigh = KNeighborsRegressor(n_neighbors=3)
neigh.fit(X_train, y_train)

y_pred = neigh.predict(X_test)
y_pred = np.round(y_pred, 2)