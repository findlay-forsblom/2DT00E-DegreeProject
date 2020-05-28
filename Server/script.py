import sys
import numpy as np
import numpy as np
from joblib import dump, load

# Script for predicting snowlevels.
# Author: Findlay Forsblom, Linnaeus University.

Xtest = sys.argv[1]
Xtest = Xtest.split(',')
Xtest = np.array(Xtest, dtype=float)
Xtest = np.reshape(Xtest, (1,-1))

regressor = load('./models/randomForrest')
pred = regressor.predict(Xtest)
print(pred[0])