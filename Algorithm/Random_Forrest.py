#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  5 09:28:38 2020

@author: findlayforsblom
"""

import numpy as np
from readFiles2 import ReadFiles
from matplotlib import pyplot as plt
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

from sklearn.ensemble import RandomForestRegressor
regressor = RandomForestRegressor(random_state = 0, criterion = 'mse', warm_start = True )

from sklearn.model_selection import GridSearchCV
parameters = {'n_estimators': [280, 270, 290], 
              'max_features': ['auto', 13,14, 16],
              'max_depth':[None, 10, 12,15],
              'max_leaf_nodes': [None, 2, 5, 12]}
grid_search = GridSearchCV(estimator = regressor,
                           param_grid = parameters,
                           cv = 5,
                           n_jobs = -1,
                           verbose = 1)
grid_search = grid_search.fit(X_train, y_train)
best_accuracy = grid_search.best_score_
best_parameters = grid_search.best_params_

regressor = RandomForestRegressor(random_state = 0, warm_start = True, n_estimators = 270, max_features = 14, max_depth = 12 )
regressor.fit(X_train, y_train)
y_pred = regressor.predict(X_train)
score = regressor.score(X_train, y_train) 

sums = (y_pred - y_train) ** 2
sums = (np.sum(sums)) / len(y_pred)

print(f'Training error {round(sums * (10**3),3) }')
print(f'Traning Score {round(score,3)} \n')

prediction = cross_val_predict(regressor, X_train, y_train, cv=5)
sums = (prediction - y_train) ** 2
sums = (np.sum(sums)) / len(prediction)


from sklearn.model_selection import cross_val_score
accuracies = cross_val_score(estimator = regressor, X = X_train, y = y_train, cv = 5)

print(f'Validation error {round(sums * (10**3),3) }')
print(f'Validation Score {round(accuracies.mean(),3)} \n')

regressor.feature_importances_

columns = dataset.columns
columns = list(columns[ind])
columns[3] ='Humidity'
columns[14] ='Snow fall'
columns[11]= 'Rain'

feat_importances = pd.Series(regressor.feature_importances_, index=columns)
fig = feat_importances.nlargest(7).plot(kind='barh', title = 'Feature Importance').get_figure()
plt.xlabel('Relative importance')
plt.ylabel('features')
fig.savefig("./images/feature.pdf")
fig.show()
