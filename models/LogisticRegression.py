#importing libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LogisticRegression
import joblib

#importing the dataset
dataset = pd.read_csv("datasets/phishyFeatures.csv")
dataset = dataset.drop('id', axis=1) #removing unwanted column
x = dataset.iloc[ : , :-1].values
y = dataset.iloc[:, -1:].values

# Ensure y is a 1D array since its a column vector
y = y.ravel()

#spliting the dataset into training set and test set
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x,y,test_size = 0.25, random_state =0 )

#fitting logistic regression 
model = LogisticRegression(random_state = 0)
model.fit(x_train, y_train)

#predicting the tests set result
y_pred = model.predict(x_test)

from sklearn.metrics import accuracy_score
# Getting the accuracy of the model
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy of the model: {accuracy * 100} %")

from sklearn.model_selection import cross_val_score
val_score = cross_val_score(model, x_train, y_train, cv=3, scoring='accuracy').mean()
print(f"Cross-validation score: {val_score}")

#confusion matrix
from sklearn.metrics import confusion_matrix, pair_confusion_matrix
cm = confusion_matrix(y_test, y_pred)
print(cm)

'''
# Visualizing the confusion matrix
from sklearn.metrics import pair_confusion_matrix 
pair_confusion_matrix(model, x_test, y_test, display_labels=['Class 0', 'Class 1'], cmap=plt.cm.Blues, values_format='d')
plt.show()

'''
#pickle file joblib
joblib.dump(model, 'trained_models/logisticR_final.pkl')

'''
LOGISTIC REGRESION MODEL SPECS:

Accuracy of the model: 92.32995658465991 %
Cross-validation score: 0.9296824955361656
Confusion Matrix:
[       True  False
    +ve [1121  128] 
    -ve [84   1431]
]
'''