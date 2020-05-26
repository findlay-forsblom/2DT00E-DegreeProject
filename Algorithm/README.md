# Machine learning algorithms
Here is the folder where all the different machine learning algorithms were tested. Each algorithm was tested
in its own file. In the folder **Old models** previous models and datasets of each machine learning algorithm can be found. 
The folder **Datasets** contains the datasets used for the models which were obtained from SMHI. The hyperparamters used in the models
were obtained using gridsearch CV.

## Data pre-processing
All data preprocessing is done in the *readFiles2* file. That is where all the different datasets are merged into one 
single dataset. The picture below shows the features used and their original datasets. This was a supervised learning 
approach with variable no 2 being the target variable and the rest as predictors.
![features](https://github.com/findlay-forsblom/2DT00E-DegreeProject/blob/master/Algorithm/images/features.PNG?raw=true)