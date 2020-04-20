import sys
import numpy as np
import numpy as np

from joblib import dump, load
Xtest = sys.argv[1]
Xtest = Xtest.split(',')
Xtest = np.array(Xtest, dtype=float)
Xtest = np.reshape(Xtest, (1,-1))
print(Xtest)
regressor = load('./models/Mlmodel')
pred = regressor.predict(Xtest)
print(pred)