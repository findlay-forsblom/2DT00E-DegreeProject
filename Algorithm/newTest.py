# -*- coding: utf-8 -*-
"""
Created on Sat May 16 16:34:42 2020

@author: findl
"""


import numpy as np
from readFiles2 import ReadFiles
from matplotlib import pyplot as plt
import pandas as pd
from sklearn.model_selection import cross_val_predict
from sklearn.model_selection import train_test_split as tts
from yellowbrick.regressor import ResidualsPlot
from yellowbrick.regressor import PredictionError

files = ReadFiles(['./Datasets/SnowDepth.csv','./Datasets/Airtemperature.csv', './Datasets/Precipitation.csv', './Datasets/FallAmount.csv', './Datasets/humidity.csv' ])
dataset = files.createDataset()
ind = list(range(3,21))
ind.insert(0, 1)
X = dataset.iloc[:, ind].values
y = dataset.iloc[:, 2].values

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 1/3, random_state = 101)

from sklearn.ensemble import RandomForestRegressor
regressor = RandomForestRegressor(random_state = 0, warm_start = True, n_estimators = 300,
                                  max_features = 15, max_depth = 12, max_leaf_nodes = 250,
                                  max_samples = 0.5,
                                  min_impurity_split = 4e-06)

visualizer = ResidualsPlot(regressor)
visualizer.fit(X_train, y_train)  # Fit the training data to the visualizer
visualizer.score(X_test, y_test)  # Evaluate the model on the test data
visualizer.show()   

visualizer = PredictionError(regressor) 
visualizer.fit(X_train, y_train)  # Fit the training data to the visualizer
visualizer.score(X_test, y_test)  # Evaluate the model on the test data
visualizer.show()  
