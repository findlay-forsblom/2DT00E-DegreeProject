#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 14:34:37 2020

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


# Fitting Multiple Linear Regression to the Training set
from sklearn.linear_model import LinearRegression
regressor = LinearRegression(fit_intercept= True,normalize= True)
regressor.fit(X_train, y_train)

# Predicting the Test set results
y_pred = regressor.predict(X_test)
y_pred = np.round(y_pred, 2)


from sklearn.model_selection import cross_val_score
accuracies = cross_val_score(estimator = regressor, X = X_train, y = y_train, cv = 10)
accuracies.mean()
accuracies.std()

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
sums = (y_pred - y_test) ** 2
sums = round((np.sum(sums)) / len(y_pred), 6)  
print(sums)
"""










