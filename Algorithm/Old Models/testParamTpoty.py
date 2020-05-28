#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 16:13:36 2020

@author: findlayforsblom
"""
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline, make_union
from sklearn.preprocessing import StandardScaler
from sklearn.svm import LinearSVR
from tpot.builtins import StackingEstimator
from tpot.export_utils import set_param_recursive
from readfiles import ReadFiles

# NOTE: Make sure that the outcome column is labeled 'target' in the data file
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
pd.DataFrame(X).to_csv("./Datasets/X.csv")
pd.DataFrame(y).to_csv("./Datasets/y.csv")
Y = pd.read_csv('./Datasets/y.csv')
Y.drop('Unnamed: 0', axis = 1, inplace = True)

tpot_data = pd.read_csv('./Datasets/X.csv', sep=',', dtype=np.float64)
#features = tpot_data.drop('target', axis=1)
training_features, testing_features, training_target, testing_target = \
            train_test_split(X, Y, random_state=42)

# Average CV score on the training set was: -0.00021627142164234252
exported_pipeline = make_pipeline(
    StackingEstimator(estimator=LinearSVR(C=0.5, dual=False, epsilon=0.1, loss="squared_epsilon_insensitive", tol=0.1)),
    StandardScaler(),
    StackingEstimator(estimator=RandomForestRegressor(bootstrap=False, max_features=0.6500000000000001, min_samples_leaf=1, min_samples_split=2, n_estimators=100)),
    RandomForestRegressor(bootstrap=False, max_features=0.8, min_samples_leaf=2, min_samples_split=10, n_estimators=410)
)
# Fix random state for all the steps in exported pipeline
set_param_recursive(exported_pipeline.steps, 'random_state', 42)

exported_pipeline.fit(training_features, training_target)
results = exported_pipeline.predict(testing_features)

ypred = pd.DataFrame(results).reset_index()
ypred.drop('index', axis = 1, inplace = True)
ypred = ypred.iloc[:].values
ypred =np.round(ypred, 2)

y_test = pd.DataFrame(testing_target).reset_index()
y_test.drop('index', axis = 1, inplace = True)
y_test = y_test.iloc[:].values
y_test =np.round(y_test, 2)


from sklearn.model_selection import cross_val_score
accuracies = cross_val_score(estimator = exported_pipeline, X = training_features, y = training_target, cv = 10)
accuracies.mean()
accuracies.std()



