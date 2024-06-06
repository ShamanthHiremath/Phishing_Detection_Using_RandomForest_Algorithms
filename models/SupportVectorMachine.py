# -*- coding: utf-8 -*-

#importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.svm import SVC
import joblib

#importing the dataset
dataset = pd.read_csv("datasets/phishyFeatures.csv")
dataset = dataset.drop('id', axis=1) #removing unwanted column

x = dataset.iloc[: , :-1].values
y = dataset.iloc[:, -1:].values

# Ensure y is a 1D array
y = y.ravel()

#spliting the dataset into training set and test set
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x,y,test_size = 0.25, random_state =0 )

#applying grid search to find best performing parameters 
from sklearn.model_selection import GridSearchCV
parameters = [{'C':[1, 10, 100, 1000], 'gamma': [ 0.1, 0.2,0.3, 0.5]}]
grid_search = GridSearchCV(SVC(kernel='rbf' ),  parameters,cv =5, n_jobs= -1)
grid_search.fit(x_train, y_train)

acc = grid_search.best_score_
print("Best Accuracy =", str(acc* 100), " %")

#printing best parameters 
print("Best Accurancy =" +str(grid_search.best_score_))
print("best parameters =" + str(grid_search.best_params_)) 

#fitting kernel SVM  with best parameters calculated 

model = SVC(C=1000, kernel = 'rbf', gamma = 0.2 , random_state = 0)
model.fit(x_train, y_train)

#predicting the tests set result
y_pred = model.predict(x_test)

#confusion matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)
print(cm)

#pickle file joblib
joblib.dump(model, 'trained_models/svm_final.pkl')
