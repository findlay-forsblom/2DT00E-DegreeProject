#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 11:46:55 2020

@author: findlayforsblom
"""

import numpy as np
from readFiles2 import ReadFiles
import pandas as pd
from sklearn.model_selection import cross_val_predict

files = ReadFiles(['./Datasets/SnowDepth.csv','./Datasets/Airtemperature.csv', './Datasets/Precipitation.csv', './Datasets/FallAmount.csv', './Datasets/humidity.csv' ])
dataset = files.createDataset()
ind = list(range(3,21))
ind.insert(0, 1)
X = dataset.iloc[:, ind].values
y = dataset.iloc[:, 2].values

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


lol2= np.array([[0.07, 2, 0.5, 80, 0, 0,0,0,0,0,0,1,0,0,0,0,0,0,0]])
regressor.predict(lol2)
regressor.coef_

columns = np.array(list(dataset))
columns = columns[ind].tolist()

import json
with open('app.json', 'w', encoding='utf-8') as f:
    json.dump(columns, f, ensure_ascii=False, indent=4)