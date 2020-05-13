#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 11 15:48:58 2020

@author: findlayforsblom
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

trainingError = np.array([0.400, 0.264, 0.149, 0.412, 0.247, 0.228, 0.437, 0.074, 0.045]) * 10 **(-3)
validationError = np.array([0.488, 0.351, 7.786, 0.415, 0.290, 0.340, 0.433, 0.400, 0.269]) * 10 **(-3)
index = ['linear Reg', 'poly-reg Deg 2', 'poly-reg Deg 3',
         'SVR(linear kernel)', 'SVR(Poly kernel)','SVR(rbf kernel)', 'SVR(Sigmoid kernel)', 'DT', 'RF']
df = pd.DataFrame({'traning error': trainingError,
                   'validation error': validationError}, index=index)
ax = df.plot.bar(rot=0)
plt.xticks(fontsize=7, rotation=40)
plt.xlabel('Machine Learning algorithms')
plt.ylabel('MSE')
plt.tight_layout()
plt.savefig('./images/errors.pdf')

trainingScore = [0.945, 0.964, 0.971, 0.943, 0.966, 0.969, 0.940, 0.990, 0.994]
validationScore = [0.944, 0.952, -0.026, 0.943, 0.960, 0.954, 0.941, 0.945, 0.963]
df = pd.DataFrame({'traningError': trainingScore,
                   'validationError': validationScore}, index=index)
ax = df.plot.bar(rot=0)
plt.xticks(fontsize=7, rotation=40)
plt.tight_layout()