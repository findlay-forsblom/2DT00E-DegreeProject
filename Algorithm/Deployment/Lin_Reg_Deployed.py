#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 10:18:46 2020

@author: findlayforsblom
"""
import numpy as np

from joblib import dump, load
lol = X_test[30]
lol = np.reshape(lol, (1,-1))
regressor = load('../Models/multipleLinearRegV2')