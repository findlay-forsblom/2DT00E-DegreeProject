#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 11 15:48:58 2020

@author: findlayforsblom
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

trainingError = np.array([0.288, 0.208, 0.140, 0.208, 0.312, 0.226, 0.225, 0.927, 0.171, 0.077]) * 10 **(-3)
validationError = np.array([0.291, 0.240, 0.430, 0.239, 0.313, 0.249, 0.265, 0.769, 0.297, 0.191]) * 10 **(-3)
index = ['linear Reg', 'poly-reg Deg 2', 'poly-reg Deg 3','poly-reg Deg 2 ridge',
         'SVR(linear kernel)', 'SVR(Poly kernel)','SVR(rbf kernel)', 'SVR(Sig kernel)', 'DT', 'RF']
df = pd.DataFrame({'traning error': trainingError,
                   'validation error': validationError}, index=index)
ax = df.plot.bar(rot=0)
plt.xticks(fontsize=6.1, rotation=60)
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