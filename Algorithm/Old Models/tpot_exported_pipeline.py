import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
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

# Average CV score on the training set was: -0.00023314697906995398
exported_pipeline = XGBRegressor(learning_rate=0.1, max_depth=10, min_child_weight=1, n_estimators=100, nthread=1, objective="reg:squarederror", subsample=1.0)
# Fix random state in exported estimator
if hasattr(exported_pipeline, 'random_state'):
    setattr(exported_pipeline, 'random_state', 42)

exported_pipeline.fit(training_features, training_target)
results = exported_pipeline.predict(testing_features)
