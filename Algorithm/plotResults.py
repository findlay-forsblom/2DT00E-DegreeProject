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







import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm
from sklearn.datasets import make_blobs


# we create 40 separable points
X, y = make_blobs(n_samples=40, centers=2, random_state=6)

# fit the model, don't regularize for illustration purposes
clf = svm.SVC(kernel='linear', C=1000)
clf.fit(X, y)

classes = ['Class A', 'Class B']






fig, ax = plt.subplots()
cdict = {0: '#ADD8E6', 1: '#b5651d'}
type = {0: 'Class A', 1:'Class B'}
for g in np.unique(y):
    ix = np.where(y == g)
    ax.scatter(X[ix,0], X[ix,1], c = cdict[g], label = type[g] )
ax.legend()





#plt.scatter(X[:, 0], X[:, 1], c=y, s=30, cmap=plt.cm.Paired, label = classes)
#plt.legend()

# plot the decision function
ax = plt.gca()
xlim = ax.get_xlim()
ylim = ax.get_ylim()

# create grid to evaluate model
xx = np.linspace(xlim[0], xlim[1], 30)
yy = np.linspace(ylim[0], ylim[1], 30)
YY, XX = np.meshgrid(yy, xx)
xy = np.vstack([XX.ravel(), YY.ravel()]).T
Z = clf.decision_function(xy).reshape(XX.shape)

# plot decision boundary and margins
ax.contour(XX, YY, Z, colors='k', levels=[-1, 0, 1], alpha=0.5,
           linestyles=['--', '-', '--'])
# plot support vectors
ax.scatter(clf.support_vectors_[:, 0], clf.support_vectors_[:, 1], s=100,
           linewidth=1, facecolors='none', edgecolors='k')

plt.axis('off')
plt.savefig("./images/SVMClassifier.pdf") 

clf.support_vectors_
