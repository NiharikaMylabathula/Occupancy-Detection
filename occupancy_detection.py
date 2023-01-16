# -*- coding: utf-8 -*-
"""Occupancy Detection.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1nIZDt48EGXsubpFMXl-bNGZ7cq88i_Y8

# **OCCUPANCY DETECTION BY DEPLOYMENT OF VARIOUS SENSORS**

In this project we are going to classify occupancy status. We are using sensor data of a corporate office. There are three datasets. One for training and two for testing.

# **Importing Required Python Libraries**
"""

import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
import matplotlib.pyplot as plt
from datetime import datetime
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report, confusion_matrix

import seaborn as sns; sns.set() 
import matplotlib.pyplot as plt  
import plotly.express as px 
import plotly.graph_objects as go

from sklearn.preprocessing import MinMaxScaler 
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier 
from sklearn.svm import SVC 
from sklearn.metrics import confusion_matrix

from keras.models import Sequential 
from keras.layers import Dense, Activation, Dropout 
from keras.regularizers import l2, l1 
from keras.metrics import BinaryAccuracy

"""**Three Datasets which are used are loaded below:**

1.Testing

2.Training

3.Validation   

**The Validation dataset was collected in
an open door situation and the testing dataset was gathered in a closed-door
situation.**

The Validation Dataset is named as "test2".

## **Loading the data using pandas dataframe**
"""

#uploading the dataset
from google.colab import files
data = files.upload()

train = pd.read_csv("datatraining.txt") 
test1 = pd.read_csv("datatest.txt") 
test2 = pd.read_csv("datatest2.txt")

"""**Looking at first five rows of "Training", "Testing", and "Validation" datasets to understand a bit about the data we are using.**"""

print('Training Set')
print(train.head())
print()
print('Test Set 1')
print(test1.head())
print()
print('Test Set 2')
print(test2.head())

"""**To get a rough idea about the datasets as in if there are any null values and the type of data being used.**

**Information regarding Testing dataset**
"""

print(test1.info()) 
test1.head()

"""**Information regarding Validation dataset.**"""

print(test2.info()) 
test2.head()

"""**Information regarding Training Dataset.**"""

print(train.info()) 
train.head()

"""**After having looked upon the basic information regarding Training, Testing, and Validation datasets we made few inferences:**

**All three datasets consists of seven features namely, "date", "Temperature", "Humidity", "Light", "CO2", "HumidityRatio", and "Occupancy".**

**Each of the features of Testing Dataset comprises of 2665  values.**

**Each of the features of Validation Dataset comprises of 9752  values.**

**Each of the features of Training Dataset comprises of 8143  values.**

**Printing the size of Datasets being used.**
"""

print(train.shape)
print(test1.shape)
print(test2.shape)

"""**As expected there should have been 6 columns corresponding to the 6 features as we saw earlier but after looking at the shape and information of the datasets we observed that there is an extra 
column named ‘column 1’ which mismatches with the ‘date’
column. We need to delete it so that it does not cause problem 
later.**

##**Statistical Analysis**

**Statistical Analysis of the Datasets are done in order to get an idea about the mean , median, count, minimum, and maximum values of the data of each dataset.**
"""

#some analytical attributes of train set
train.describe()

#some analytical attributes of test set 1
test1.describe()

#some analytical attributes of test set 2
test2.describe()

"""**As mentioned earlier, The data set has an unnamed id column which mismatches with date. So,we deleted it for making header and the data fitting each other. Also, the second test set seems to lack quotation marks around the dates, so that has been added.**"""

# For training data set:
lines = []
with open('datatraining.txt', 'r') as f:
    lines = f.readlines()
    
new_lines = []
new_lines.append(lines[0].replace('date', 'Date'))

for line in lines[1:]:
    new_lines.append(','.join(l for l in line.split(',')[1:]))

with open('train.csv', 'w') as f:
    f.writelines(new_lines)
    
# For test1 data set:
lines = []
with open('datatest.txt', 'r') as f:
    lines = f.readlines()
    new_lines = []
new_lines.append(lines[0].replace('date', 'Date'))

for line in lines[1:]:
    new_lines.append(','.join(l for l in line.split(',')[1:]))

with open('test1.csv', 'w') as f:
    f.writelines(new_lines)
    
# For test2 data set:
lines = []
with open('datatest2.txt', 'r') as f:
    lines = f.readlines()
    
new_lines = []
new_lines.append(lines[0].replace('date', 'Date'))

for line in lines[1:]:
    i = line.index(',') + 1
    ii = line[i:].index(',')
    line = line[:i] + '"' + line[i:i+ii] + '"' + line[i+ii:]
    new_lines.append(','.join(l for l in line.split(',')[1:]))

with open('test2.csv', 'w') as f:
    f.writelines(new_lines)

"""**Now very importantly check if there are any null values 
present because if there is any NaN value present then it will have to be replaced with some significant values.**
"""

# Check NaNs for train:
print(train.isnull().sum())
print()
# Check NaNs for test1:
print(test1.isnull().sum())
print()
# Check NaNs for test2:
print()
print(test2.isnull().sum())

"""**From the above result we got to know that there are no NaN values present.**

# **Data Visualization**

A scatter plot matrix is a grid (or matrix) of scatter plots used to visualize bivariate relationships between combinations of variables. Each scatter plot in the matrix visualizes the relationship between a pair of variables, allowing many relationships to be explored in one chart.

Plotting the scatter matrix with respect to occupancy column:
"""

pd.plotting.scatter_matrix(train, c=train['Occupancy'], figsize=[10, 10])
plt.show()

"""From here we can see that Humidity ratio and humidity are highly correlated, so humidity ratio can be dropped.

**Time Series Analysis**

To see time series of every feature. we converted date strings to Python datetime objects.
"""

def dateOrNotToDate(date_str):
    return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')

"""**Converting Date for each Dataset**"""

def convert_dates(df):
    for i, date in enumerate(df['date']):
        df.iloc[i, df.columns.get_loc('date')] = dateOrNotToDate(date)
convert_dates(train)
convert_dates(test1)
convert_dates(test2)

"""**ggplot —a general scheme for data visualization which breaks up graphs into semantic components such as scales and layers.**

Plotting every feature in time series:
"""

#plt.style.use('ggplot')
for i, col in enumerate(train.columns.values[1:]):
    plt.subplot(3, 2, i+1)
    plt.plot(train['date'].values.tolist(), train[col].values.tolist(), label=col)
    plt.title(col)
    fig, ax = plt.gcf(), plt.gca()
    ax.xaxis_date()
    fig.autofmt_xdate()
    fig.set_size_inches(10, 10)
    plt.tight_layout()
    plt.grid(True)
plt.show()

"""**Normalizing the data:** Since we have low values like humidity_ratio and high values like light and CO2, we should normalize the data to simplify the learning process.

"""

scaler = MinMaxScaler()
columns = ['Temperature', 'Humidity', 'Light', 'CO2', 'HumidityRatio']
scaler.fit(np.array(train[columns]))
test1[columns] = scaler.transform(np.array(test1[columns]))
test2[columns] = scaler.transform(np.array(test2[columns]))
train[columns] = scaler.transform(np.array(train[columns])
)

"""# **Box Plot of the features**"""

plt.figure(figsize=(10,10))
plt.title('Box Plot for Features', fontdict={'fontsize':18})
ax = sns.boxplot(data=train.drop(['date', 'Occupancy'],axis=1), orient="h", palette="Set2")
print(train.drop(['date', 'Occupancy'],axis=1).describe())

"""# **Correlation table for the features**"""

plt.figure(figsize=(10,8))
plt.title('Correlation Table for Features', fontdict={'fontsize':18})
ax = sns.heatmap(train.corr(), annot=True, linewidths=.2)

"""# **4-D plot for occupancy**"""

from plotly.offline import init_notebook_mode, iplot, plot
init_notebook_mode(connected=True)

data = train.copy()
data.Occupancy = data.Occupancy.astype(str)
fig = px.scatter_3d(data, x='Temperature', y='Humidity', z='CO2', size='Light', color='Occupancy', color_discrete_map={'1':'red', '0':'blue'})
fig.update_layout(scene_zaxis_type="log", title={'text': "Features and Occupancy",
'y':0.9,
'x':0.5,
'xanchor': 'center',
'yanchor': 'top'})
iplot(fig)

"""Occupancy status: 1 indicates "occupied" status, 0 indicated "unoccupied" status"""

sns.set(style="darkgrid")
plt.title("Occupancy Distribution", fontdict={'fontsize':18})
ax = sns.countplot(x="Occupancy", data=train)

"""There's a wide gap between 07-09.02.2015, so checking for the day of those dates"""

days = [
    'Monday',
    'Tuesday', 
    'Wednesday',
    'Thursday',
    'Friday',
    'Saturday',
    'Sunday'
]
seventh_of_feb = datetime.strptime('2015-02-07', '%Y-%m-%d')
print(days[seventh_of_feb.weekday()])

"""So, its saturday-Weekend! So the employees don't go to the office on weekends.

If we can get the start indices of every day in the dates, we can iterate through days and for every day we can plot occupancy in time series.

To do so, we stored the Date column in a list, and day start indices in another. Iterating through 5 to 10, we will get those dates' start index in the dataset:
"""

date_list = train.date.values.tolist()
day_start_indices = []
for i in range(5, 11):
    day_start_indices.append(
        date_list.index(
            datetime.strptime(
                '2015-02-' + str(i) + ' 00:00:00',
                '%Y-%m-%d %H:%M:%S'
            )
        )
    )
day_start_indices = [0] + day_start_indices
print(day_start_indices)

"""So, first 369 rows are from 4th of Feb. Subsequent rows, from 370 to 1808 are from 5th of Feb. etc.

Now, we plot the occupancy in time series:
"""

for i in range(len(day_start_indices)):    
    plt.subplot(4, 2, i + 1)
    if i != len(day_start_indices) - 1:
        plt.plot(
            date_list[day_start_indices[i]:day_start_indices[i+1]],
            train['Occupancy'].values.tolist()[
                day_start_indices[i]:day_start_indices[i+1]])
    else:
        plt.plot(
            date_list[day_start_indices[i]:],
            train['Occupancy'].values.tolist()[day_start_indices[i]:])
    plt.title(str(i + 4) + 'th of Feb.')
    plt.grid(True)
    plt.xticks(rotation=90)
    fig, ax = plt.gcf(), plt.gca()
    ax.xaxis_date()
    fig.set_size_inches(10, 10)
    fig.tight_layout()
plt.show()

"""Printing every first and last occurence of occupancy in every days, To get an idea of the working hours for these officers:"""

print('Daily Work Hours')
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
print()
for i in range(len(day_start_indices)-1):
    try:
        print('Start:\t', 
              train.loc[(train.date > date_list[day_start_indices[i]]) &
                        (train.date < date_list[day_start_indices[i+1]]) &
                        (train.Occupancy == 1), 'date'].iloc[0])
        print('End:\t',
              train.loc[(train.date > date_list[day_start_indices[i]]) &
                        (train.date < date_list[day_start_indices[i+1]]) &
                        (train.Occupancy == 1), 'date'].iloc[-1])
    except:
        print('No Occupancy')
    print('########################################')
    print()

"""It appears to be that, employees do not come to office before 07:30 and they depart after 18:00.

**Analysing Light:** Light seems to be less than 400lx at the weekend. Day light must be illuminating the room atmost 370lx or so. Light follows the same pattern with occupancy. Interesting enough, there is a sudden increase in the lighting at the weekend, possibly on 7th of Feb. Those spots may be outliers.
"""

lighting = train.loc[
    (train.date > date_list[day_start_indices[3]]) &
    (train.date < date_list[day_start_indices[4]]) &
    (train.Light > 850),
    ('date', 'Light')
]
print(lighting)

"""After exploratory analyses, we decided to add Weekend and WorkingHours as features. To do this, we  will, again, write a function to apply the addition to all three of the data sets. For Weekend, as might be expected, we will check if the date is "Saturday or Sunday" or not. If so, then Weekend = 1, else Weekend = 0.

For WorkingHours, if time of the day is between 07:30 and 18:00, then WorkingHours = 1, else WorkingHours = 0.

Firstly we will fill these new columns with 0s. Those which fit the condition will later take their corresponding values.

"""

def add_features(df):
    df.loc[:, 'Weekend'] = 0
    df.loc[:, 'WorkingHour'] = 0

    for i, date in enumerate(df['date']):
        if (days[date.weekday()] == 'Saturday') or\
            (days[date.weekday()] == 'Sunday'):
            df.iloc[i, df.columns.get_loc('Weekend')] = 1

        if date.time() >= datetime.strptime('07:30', '%H:%M').time() and\
            date.time() <= datetime.strptime('18:00', '%H:%M').time():
            df.iloc[i, df.columns.get_loc('WorkingHour')] = 1

add_features(train)
add_features(test1)
add_features(test2)

""" Plotting the scatter matrix again, after the addition of these two new features"""

pd.plotting.scatter_matrix(train, c=train['Occupancy'], figsize=[15, 15])
plt.show()

"""As the results show, Weekend clearly distinguishes the occupancy. So does the WorkingHour.

Also Weekend and Light together seems to be seperable while Weekend with Humidity seems less helpful. Likewise, WorkingHour with CO2 seems very neat and separable.

# **Modeling, Training and Testing**
After data analyses, now, we shall extract source and target domains for modeling.

X_train includes all columns except Occupancy of train DataFrame. X_test1 includes all columns except Occupancy of test1 DataFrame. Xtest2 includes all columns except Occupancy of test2 DataFrame. And y* variables are the corresponding target Series.

We have also defined a list of tuples for features. We will use them in testing the models with different feature combinations.

The Models that we are going to use:



* Linear Regression
*   Logistic Regression
* Kernelized Support Vector Machine
* Decision Tree
* Random Forest
*   Naïve Bayes
* K-Nearest Neighbors


The general convention we followed for every model is,

Import necessary modules.

Define hyper parameters space.

For every feature combinations in the list mentioned above (and coded below):

Make grid search cross-validation.

Fit the model and predict against train, test1, and test2 sets.

Print classification report.

After every model, we presented classification as a table and my conclusions.
"""

X_train = train.drop('Occupancy', axis=1)
X_train1 = X_train.drop('date', axis=1)
y_train = train['Occupancy']

X_test1 = test1.drop('Occupancy', axis=1)
X_test11 = X_test1.drop('date', axis=1)
y_test1 = test1['Occupancy']

X_test2 = test2.drop('Occupancy', axis=1)
X_test21 = X_test2.drop('date', axis=1)
y_test2 = test2['Occupancy']

features_combs_list = [
    ('Weekend', 'WorkingHour'),
    ('Light', 'CO2'),
    ('WorkingHour', 'CO2'),
    ('CO2', 'Temperature'),
    ('Weekend', 'WorkingHour', 'Light', 'CO2'),
    ('Weekend', 'HumidityRatio'),
]

"""# **Linear Regression**"""

from sklearn.linear_model import LinearRegression
linear_regressor = LinearRegression()
linear_regressor.fit(X_train1,y_train)
prediction = linear_regressor.predict(X_test21)

# Commented out IPython magic to ensure Python compatibility.
from sklearn.metrics import mean_squared_error, r2_score

 #The mean squared error
print('Mean squared error: %.2f'
#         % mean_squared_error(y_test2, prediction))
 # the coefficient of determination: 1 is perfect prediction
print('\nCoefficient of determination: %.2f'
#        % r2_score(y_test2, prediction))

"""# **Logistic Regression**"""

from sklearn.linear_model import LogisticRegression

hyper_params_space = [
    {
        'penalty': ['l1', 'l2'],
        'C': [1, 1.2, 1.5],
        'random_state': [0]
    },
]

for features in features_combs_list:
    print(features)
    print('===================================')
    X = X_train.loc[:, features]
    X_t1 = X_test1.loc[:, features]
    X_t2 = X_test2.loc[:, features]
    
    logit = GridSearchCV(LogisticRegression(), hyper_params_space,
                        scoring='accuracy')
    logit.fit(X, y_train)

    print('Best parameters set:')
    print(logit.best_params_)
    print()
    
    preds = [
        (logit.predict(X), y_train, 'Train'),
        (logit.predict(X_t1), y_test1, 'Test1'),
        (logit.predict(X_t2), y_test2, 'Test2')
    ]
    for pred in preds:
        print(pred[2] + ' Classification Report:')
        print()
        print(classification_report(pred[1], pred[0]))
        print()
        print(pred[2] + ' Confusion Matrix:')
        print(confusion_matrix(pred[1], pred[0]))
        print()

"""# **Kernalized Support Vector Machine**"""

from sklearn.svm import SVC

hyper_params_space = [
    {
        'kernel': ['linear'],
        'random_state': [0]
    },
    {
        'kernel': ['rbf'],
        'gamma': np.arange(2, 5),
        'random_state': [0]
    },
]

for features in features_combs_list:
    print(features)
    print('===================================')
    X = X_train.loc[:, features]
    X_t1 = X_test1.loc[:, features]
    X_t2 = X_test2.loc[:, features]

    svc = GridSearchCV(SVC(), hyper_params_space,
                       scoring='accuracy')
    svc.fit(X, y_train)
    
    print('Best parameters set:')
    print(svc.best_params_)
    print()
    
    preds = [
        (svc.predict(X), y_train, 'Train'),
        (svc.predict(X_t1), y_test1, 'Test1'),
        (svc.predict(X_t2), y_test2, 'Test2')
    ]
    
    for pred in preds:
        print(pred[2] + ' Classification Report:')
        print()
        print(classification_report(pred[1], pred[0]))
        print()
        print(pred[2] + ' Confusion Matrix:')
        print(confusion_matrix(pred[1], pred[0]))
        print()

"""# **Decision Tree**"""

from sklearn.tree import DecisionTreeClassifier

hyper_params_space = [
    {
        'max_depth': np.arange(1, 100),
        'min_samples_split': np.arange(2, 5),
        'random_state': [0]
    },
]

for features in features_combs_list:
    print(features)
    print('===================================')
    X = X_train.loc[:, features]
    X_t1 = X_test1.loc[:, features]
    X_t2 = X_test2.loc[:, features]

    tree = GridSearchCV(DecisionTreeClassifier(), hyper_params_space,
                       scoring='accuracy')
    tree.fit(X, y_train)
    
    print('Best parameters set:')
    print(tree.best_params_)
    print()
    
    preds = [
        (tree.predict(X), y_train, 'Train'),
        (tree.predict(X_t1), y_test1, 'Test1'),
        (tree.predict(X_t2), y_test2, 'Test2')
    ]
    
    for pred in preds:
        print(pred[2] + ' Classification Report:')
        print()
        print(classification_report(pred[1], pred[0]))
        print()
        print(pred[2] + ' Confusion Matrix:')
        print(confusion_matrix(pred[1], pred[0]))
        print()

"""# **Random Forest**"""

from sklearn.ensemble import RandomForestClassifier

hyper_params_space = [
    {
        'max_depth': np.arange(1, 100),
        'min_samples_split': np.arange(2, 5),
        'random_state': [0],
        'n_estimators': np.arange(10, 20)
    },
]

for features in features_combs_list:
    print(features)
    print('===================================')
    X = X_train.loc[:, features]
    X_t1 = X_test1.loc[:, features]
    X_t2 = X_test2.loc[:, features]

    tree = GridSearchCV(RandomForestClassifier(), hyper_params_space,
                       scoring='accuracy')
    tree.fit(X, y_train)
    
    print('Best parameters set:')
    print(tree.best_params_)
    print()
    
    preds = [
        (tree.predict(X), y_train, 'Train'),
        (tree.predict(X_t1), y_test1, 'Test1'),
        (tree.predict(X_t2), y_test2, 'Test2')
    ]
    
    for pred in preds:
        print(pred[2] + ' Classification Report:')
        print()
        print(classification_report(pred[1], pred[0]))
        print()
        print(pred[2] + ' Confusion Matrix:')
        print(confusion_matrix(pred[1], pred[0]))
        print()

"""# **Naive Bayes**"""

from sklearn.naive_bayes import GaussianNB

for features in features_combs_list:
    print(features)
    print('===================================')
    X = X_train.loc[:, features]
    X_t1 = X_test1.loc[:, features]
    X_t2 = X_test2.loc[:, features]
    
    nb = GaussianNB()
    nb.fit(X, y_train)
    
    preds = [
        (nb.predict(X), y_train, 'Train'),
        (nb.predict(X_t1), y_test1, 'Test1'),
        (nb.predict(X_t2), y_test2, 'Test2')
    ]
    
    for pred in preds:
        print(pred[2], ':', end=' ')
        print(str((X.shape[0] - (pred[0] != pred[1]).sum()) / X.shape[0]))
    print()

"""# **K Nearest Neighbors**"""

from sklearn.neighbors import KNeighborsClassifier

hyper_params_space = [
    {
        'n_neighbors': np.arange(1, 50),
    },
]

for features in features_combs_list:
    print(features)
    print('===================================')
    X = X_train.loc[:, features]
    X_t1 = X_test1.loc[:, features]
    X_t2 = X_test2.loc[:, features]

    knn = GridSearchCV(KNeighborsClassifier(), hyper_params_space,
                       scoring='accuracy')
    knn.fit(X, y_train)
    
    print('Best parameters set:')
    print(knn.best_params_)
    print()
    
    preds = [
        (knn.predict(X), y_train, 'Train'),
        (knn.predict(X_t1), y_test1, 'Test1'),
        (knn.predict(X_t2), y_test2, 'Test2')
    ]
    
    for pred in preds:
        print(pred[2] + ' Classification Report:')
        print()
        print(classification_report(pred[1], pred[0]))
        print()
        print(pred[2] + ' Confusion Matrix:')
        print(confusion_matrix(pred[1], pred[0]))
        print()

from sklearn.decomposition import PCA

from sklearn import metrics

def Regression(model,X_train,y_train,X_test1,y_test1):
 model.fit(X_train,y_train)
 prediction = model.predict(X_test1)
 print(model.fit(X_train,y_train))
 A=[]
 A.append(metrics.mean_absolute_error(y_test1,prediction))
 A.append(metrics.mean_squared_error(y_test1,prediction))
 A.append(np.sqrt(metrics.mean_squared_error(y_test1,prediction)))
 A.append(model.score(X_train,y_train))
 return A

pca = PCA()
X_pca = pca.fit_transform(X_train1)
print(X_pca.shape)
X_t_pca = pca.transform(X_test11)
print(pca.explained_variance_ratio_)
print(np.cumsum(np.round(pca.explained_variance_ratio_, decimals=4)*100))
PCR_result = []
PCR_result.append(Regression(LinearRegression(), X_pca, y_train, X_t_pca, y_test1))
PCR_result.append(Regression(LogisticRegression(solver="liblinear",random_state=47), X_pca, y_train, X_t_pca, y_test1))
PCR_result.append(Regression(SVC(), X_pca, y_train, X_t_pca, y_test1))
PCR_result.append(Regression(DecisionTreeClassifier(max_depth=1), X_pca, y_train, X_t_pca, y_test1))
PCR_result.append(Regression(RandomForestClassifier(n_estimators=80), X_pca, y_train, X_t_pca, y_test1))
#print PCR Result
PCR_Result = pd.DataFrame(PCR_result, columns=["MAE","MSE","RMSE","R^2 Score"])
PCR_Result.insert(0, "Model",["Linear Regression", "Logistic Regression", "Support Vector Regression", "Decision Trees", "Random Forest"], True)
print(PCR_Result)

def Regression(model,X_train,y_train,X_test2,y_test2):
 model.fit(X_train,y_train)
 prediction = model.predict(X_test2)
 print(model.fit(X_train,y_train))
 A=[]
 A.append(metrics.mean_absolute_error(y_test2,prediction))
 A.append(metrics.mean_squared_error(y_test2,prediction))
 A.append(np.sqrt(metrics.mean_squared_error(y_test2,prediction)))
 A.append(model.score(X_train,y_train))
 return A

pca = PCA()
X_pca = pca.fit_transform(X_train1)
print(X_pca.shape)
X_t_pca = pca.transform(X_test21)
print(pca.explained_variance_ratio_)
print(np.cumsum(np.round(pca.explained_variance_ratio_, decimals=4)*100))
PCR_result = []
PCR_result.append(Regression(LinearRegression(), X_pca, y_train, X_t_pca, y_test2))
PCR_result.append(Regression(LogisticRegression(solver="liblinear",random_state=47), X_pca, y_train, X_t_pca, y_test2))
PCR_result.append(Regression(SVC(), X_pca, y_train, X_t_pca, y_test2))
PCR_result.append(Regression(DecisionTreeClassifier(max_depth=1), X_pca, y_train, X_t_pca, y_test2))
PCR_result.append(Regression(RandomForestClassifier(n_estimators=80), X_pca, y_train, X_t_pca, y_test2))
#print PCR Result
PCR_Result = pd.DataFrame(PCR_result, columns=["MAE","MSE","RMSE","R^2 Score"])
PCR_Result.insert(0, "Model",["Linear Regression", "Logistic Regression", "Support Vector Regression", "Decision Trees", "Random Forest"], True)
print(PCR_Result)

"""# **Artificial Neural Networks**

Now, we are going to use ANNs to predict occupancy
"""

X_train = train.drop(columns=['date', 'Occupancy'], axis=1)
y_train = train['Occupancy']
X_validation = test1.drop(columns=['date', 'Occupancy'], axis=1)
y_validation = test1['Occupancy']
X_test = test2.drop(columns=['date', 'Occupancy'], axis=1)
y_test = test2['Occupancy']

# NN without regularization
model1 = Sequential()
model1.add(Dense(32, activation='relu', input_dim=7))
model1.add(Dense(16, activation='relu'))
model1.add(Dense(1, activation='sigmoid'))
model1.compile(optimizer='rmsprop',
              loss='binary_crossentropy',
              metrics=['accuracy'])
history1 = model1.fit(X_train, y_train, epochs=50, batch_size=32, validation_data=(X_validation, y_validation))

# NN with 0.2 dropout ratio before the hidden layer.
model2 = Sequential()
model2.add(Dense(32, activation='relu', input_dim=7))
model2.add(Dropout(0.2))
model2.add(Dense(16, activation='relu'))
model2.add(Dense(1, activation='sigmoid'))
model2.compile(optimizer='rmsprop',
              loss='binary_crossentropy',
              metrics=['accuracy'])
history2 = model2.fit(X_train, y_train, epochs=50, batch_size=32, validation_data=(X_validation, y_validation))

# NN with L1(Lasso) regularization
model3 = Sequential()
model3.add(Dense(32, activation='relu', input_dim=7, kernel_regularizer=l1(l=0.01)))
model3.add(Dense(16, activation='relu', kernel_regularizer=l1(l=0.01)))
model3.add(Dense(1, activation='sigmoid'))
model3.compile(optimizer='rmsprop',
              loss='binary_crossentropy',
              metrics=['accuracy'])
history3 = model3.fit(X_train, y_train, epochs=50, batch_size=32, validation_data=(X_validation, y_validation))

# NN with L2(Ridge) Regularization
model4 = Sequential()
model4.add(Dense(32, activation='relu', input_dim=7, kernel_regularizer=l2(l=0.01)))
model4.add(Dense(16, activation='relu', kernel_regularizer=l2(l=0.01)))
model4.add(Dense(1, activation='sigmoid'))
model4.compile(optimizer='rmsprop',
              loss='binary_crossentropy',
              metrics=['accuracy'])
history4 = model4.fit(X_train, y_train, epochs=50, batch_size=32, validation_data=(X_validation, y_validation))

loss1 = history1.history['loss']
val_loss1 = history1.history['val_loss']
loss2 = history2.history['loss']
val_loss2 = history2.history['val_loss']
loss3 = history3.history['loss']
val_loss3 = history3.history['val_loss']
loss4 = history4.history['loss']
val_loss4 = history4.history['val_loss']


fig = go.Figure()
fig.add_trace(go.Scatter(x=np.arange(len(loss1)), y=loss1,
                    name='Training Loss without Regularization', line=dict(color='royalblue')))
fig.add_trace(go.Scatter(x=np.arange(len(val_loss1)), y=val_loss1,
                    name='Validation Loss without Regularization', line = dict(color='firebrick')))

fig.add_trace(go.Scatter(x=np.arange(len(loss2)), y=loss2,
                    name='Training Loss with Dropout', line=dict(color='royalblue', dash='dash')))
fig.add_trace(go.Scatter(x=np.arange(len(val_loss2)), y=val_loss2,
                    name='Validation Loss with Dropout', line = dict(color='firebrick', dash='dash')))

fig.add_trace(go.Scatter(x=np.arange(len(loss3)), y=loss3,
                    name='Training Loss with L1 Regularization', line=dict(color='royalblue', dash='dot')))
fig.add_trace(go.Scatter(x=np.arange(len(val_loss3)), y=val_loss3,
                    name='Validation Loss with L1 Regularization', line = dict(color='firebrick', dash='dot')))

fig.add_trace(go.Scatter(x=np.arange(len(loss4)), y=loss4,
                    name='Training Loss with L2 Regularization', line=dict(color='royalblue', dash='longdashdot')))
fig.add_trace(go.Scatter(x=np.arange(len(val_loss4)), y=val_loss4,
                    name='Validation Loss with L2 Regularization', line = dict(color='firebrick', dash='longdashdot')))


fig.update_layout(xaxis_title='Epochs',
                  yaxis_title='Loss',
                  title={'text': "Training and Validation Losses for Different Models",
                                                'x':0.5,
                                                'xanchor': 'center',
                                                'yanchor': 'top'})
iplot(fig)

model = Sequential()
model.add(Dense(32, activation='relu', input_dim=7, kernel_regularizer=l2(l=0.01)))
model.add(Dropout(0.3))
model.add(Dense(32, activation='relu', kernel_regularizer=l2(l=0.01)))
model.add(Dense(1, activation='sigmoid'))
model.compile(optimizer='rmsprop',
                loss='binary_crossentropy',
                metrics=['accuracy'])
history = model.fit(X_train, y_train, epochs=50, batch_size=32)

"""# So all the models seem to have a high accuracy around 98-99% """