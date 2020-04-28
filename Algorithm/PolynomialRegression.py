#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 08:38:50 2020

@author: findlayforsblom
"""

import numpy as np
from readfiles import ReadFiles
import pandas as pd
from sklearn.model_selection import cross_val_predict
from matplotlib import pyplot as plt

files = ReadFiles(['./Datasets/SnowDepth.csv','./Datasets/Airtemperature.csv', './Datasets/Precipitation.csv', './Datasets/FallAmount.csv', './Datasets/humidity.csv' ])
dataset = files.createDataset()
dataset = dataset[dataset['Temp'] < 10]
X = dataset.iloc[:, [1, 3,4,5,6]].values
y = dataset.iloc[:, 2].values

# Encoding categorical data
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer

# Encoding categorical data
df = pd.DataFrame(data=X, columns=['Snow depth', 'Temp', 'dummy', 'Precipiattion','Humidity'])
just_dummies = pd.get_dummies(df['dummy'])

df = pd.concat([df, just_dummies], axis=1)
df.drop(['dummy'], inplace=True, axis=1) 

X = df.iloc[:,].values

# Avoiding the Dummy Variable Trap
X = X[:, :-1]

"""
columnTransformer = ColumnTransformer([('encoder', OneHotEncoder(), [2])], remainder='passthrough')
X = columnTransformer.fit_transform(X).toarray()

# Avoiding the Dummy Variable Trap
X = X[:, 1:]
"""

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
    
    
    from sklearn.model_selection import cross_val_score
    accuracies = cross_val_score(estimator = lin_reg_2, X = X_poly, y = y_train, cv = 5)
    accuracies.std()
    
    print(f'Validation error {round(sums * (10**3),3) }')
    print(f'Validation Score {round(accuracies.mean(),3)} \n') 
    
validationErrors = np.array(validationErrors)
pos = validationErrors.argmin()

#printing results for tranning error and validation erro
fig, ax = plt.subplots()
ax.plot(list(range(1,4)), traningErrors, '-', label='training data')
ax.plot(list(range(1,4)), validationErrors, '-', label='validation data')
ax.axvline(x=list(range(1,4))[pos], linestyle = '--', label = 'best fit')
ax.set_xlabel('Model Complexity (Degree)')
ax.set_ylabel('Mean Squared Error')
ax.legend()
ax.set_title('The bias variance trade off')
plt.show()


#Using ridge regression in comibination with polynomial regression at degree 2
from sklearn.linear_model import Ridge
poly_reg = PolynomialFeatures(degree=2)
X_poly = poly_reg.fit_transform(X_train)
poly_reg.fit(X_poly, y_train)
ridgeReg = Ridge(fit_intercept = False, normalize = True)

from sklearn.model_selection import GridSearchCV
parameters = [{'alpha': [0.000001, 0.00002, 0.0000003], 
               'max_iter': [1000, 3000, 10000],
              'tol': [1e-5, 1e-6, 1e-7, 1e-4, 1e-3, 1e-2, 1e-1, 1e-8]}]

grid_search = GridSearchCV(estimator = ridgeReg,
                           param_grid = parameters,
                           cv = 5,
                           scoring = 'neg_mean_squared_error',
                           n_jobs = -1)
grid_search = grid_search.fit(X_poly[:,1:], y_train)
best_mse = grid_search.best_score_
best_parameters = grid_search.best_params_

ridgeReg = Ridge(fit_intercept = False, normalize = True, alpha = 0.000001, tol ='1e-5,', max_iter = 1000 )
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


#lin_reg_2.score(poly_reg.fit_transform(X_test), y_test)

"""

y_pred = lin_reg_2.predict(poly_reg.fit_transform(X_test))
y_pred = np.round(y_pred, 2)

sums = (y_pred - y_test) ** 2
sums = round((np.sum(sums)) / len(y_pred), 6)  
print(sums) 

from sklearn.model_selection import cross_val_score
accuracies = cross_val_score(estimator = lin_reg_2, X = X_train, y = y_train, cv = 10)
accuracies.mean()
accuracies.std()

# Applying Grid Search to find the best model and the best parameters
from sklearn.model_selection import GridSearchCV
parameters = [{'fit_intercept': [True, False], 'normalize': [True, False]}]
grid_search = GridSearchCV(estimator = lin_reg_2,
                           param_grid = parameters,
                           cv = 10,
                           n_jobs = -1)
grid_search = grid_search.fit(X_train, y_train)
best_accuracy = grid_search.best_score_
best_parameters = grid_search.best_params_
"""
