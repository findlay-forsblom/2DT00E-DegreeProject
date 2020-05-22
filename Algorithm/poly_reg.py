#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  3 09:17:57 2020

@author: findlayforsblom
"""

import numpy as np
from readFiles2 import ReadFiles
import pandas as pd
from sklearn.model_selection import cross_val_predict
from matplotlib import pyplot as plt
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

# Fitting Polynomial Regression to the dataset
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

traningErrors = []
validationErrors = []

for degree in range(1,4):
    print(f'Degree {degree}')
    poly_reg = PolynomialFeatures(degree = degree)
    X_poly = poly_reg.fit_transform(X_train)
    #poly_reg.fit(X_poly, y)
    
    lin_reg_2 = LinearRegression(n_jobs= -1,fit_intercept= False, normalize= True)
    lin_reg_2.fit(X_poly, y_train)
    
    y_pred = lin_reg_2.predict(X_poly)
    sums = (y_pred - y_train) ** 2
    sums = (np.sum(sums)) / len(y_pred)
    score = lin_reg_2.score(X_poly, y_train)
    print(f'Training error {round(sums * (10**3),3) }')
    print(f'Traning Score {round(score,3)} \n')
    
    traningErrors.append(sums)
    
    prediction = cross_val_predict(lin_reg_2, X_poly, y_train, cv=5)
    sums = (prediction - y_train) ** 2
    sums = (np.sum(sums)) / len(prediction)
    
    validationErrors.append(sums)
    
    accuracies = cross_val_score(estimator = lin_reg_2, X = X_poly, y = y_train, cv = 5)
    accuracies.std()
    
    print(f'Validation error {round(sums * (10**3),3) }')
    print(f'Validation Score {round(accuracies.mean(),3)} \n') 
    
validationErrors = np.array(validationErrors)
pos = validationErrors.argmin()

#printing results for tranning error and validation erro
fig, ax = plt.subplots(figsize=(4, 5), dpi=80)
ax.plot(list(range(1,4)), traningErrors, '-', label='training data')
ax.plot(list(range(1,4)), validationErrors, '-', label='validation data')
ax.axvline(x=list(range(1,4))[pos], linestyle = '--', label = 'best fit')
ax.set_xlabel('Model Complexity (Degree)')
ax.set_ylabel('Mean Squared Error')
ax.legend()
ax.set_title('The bias variance trade off')
plt.savefig('./images/bias3.pdf')


from sklearn.linear_model import Ridge
poly_reg = PolynomialFeatures(degree=2)
X_poly = poly_reg.fit_transform(X_train)
poly_reg.fit(X_poly, y_train)

ridgeReg = Ridge(fit_intercept = False, normalize = True)
from sklearn.model_selection import GridSearchCV
parameters = [{'alpha': [0.01, 0.03, 0.009], 
               'max_iter': [1000, 5000, 10000],
              'tol': [1e-5, 1e-8, 2e-8]}]

grid_search = GridSearchCV(estimator = ridgeReg,
                           param_grid = parameters,
                           cv = 5,
                           scoring = 'neg_mean_squared_error',
                           n_jobs = -1,
                           verbose = 1)
grid_search = grid_search.fit(X_poly[:,1:], y_train)
best_mse = grid_search.best_score_
best_parameters = grid_search.best_params_

ridgeReg = Ridge(fit_intercept = False, normalize = True, alpha = 0.01, tol =1e-5,
                 max_iter = 13000, solver = 'auto' )
ridgeReg.fit(X_poly, y_train)
y_pred = ridgeReg.predict(X_poly)
sums = (y_pred - y_train) ** 2
sums = (np.sum(sums)) / len(y_pred)
score = ridgeReg.score(X_poly, y_train)
print(f'Training error {round(sums * (10**3),3) }')
print(f'Traning Score {round(score,3)} \n')

prediction = cross_val_predict(ridgeReg, X_poly, y_train, cv=5)
sums = (prediction - y_train) ** 2
sums = (np.sum(sums)) / len(prediction)
accuracies = cross_val_score(estimator = ridgeReg, X = X_poly, y = y_train, cv = 5)

print(f'Validation error {round(sums * (10**3),3) }')
print(f'Validation Score {round(accuracies.mean(),3)} \n') 
