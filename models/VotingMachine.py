from sklearn.linear_model import LogisticRegression as LR
from sklearn.ensemble import RandomForestClassifier as RF
from sklearn.svm import SVC
from sklearn.ensemble import VotingClassifier
from sklearn.model_selection import cross_val_score
import pandas as pd


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

# Initialize classifiers
# logistic_regression = LR(random_state=0)
random_forest = RF(random_state=0)
support_vector_machine = SVC(probability=True, random_state=0)

# Fit the models (ensure that x_train and y_train are available)
# logistic_regression.fit(x_train, y_train)
random_forest.fit(x_train, y_train)
support_vector_machine.fit(x_train, y_train)

# Create the VotingClassifier
ensemble = VotingClassifier(estimators=[
    # ('lr', logistic_regression), 
    ('rf', random_forest), 
    ('svm', support_vector_machine)
], voting='hard')

# Fit the ensemble model
ensemble.fit(x_train, y_train)

#predicting the tests set result
y_pred = ensemble.predict(x_test)

# Evaluate the ensemble model
from sklearn.metrics import accuracy_score
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy of the model: {accuracy * 100} %")

# Cross-validation score
val_score = cross_val_score(ensemble, x_train, y_train, cv=3, scoring='accuracy').mean()
print(f"Cross-validation score: {val_score}")

#confusion matrix
from sklearn.metrics import confusion_matrix, pair_confusion_matrix
cm = confusion_matrix(y_test, y_pred)
print(cm)

'''
# Visualizing the confusion matrix
from sklearn.metrics import pair_confusion_matrix 
pair_confusion_matrix(ensemble, x_test, y_test, display_labels=['Class 0', 'Class 1'], cmap=plt.cm.Blues, values_format='d')
plt.show()

'''

'''
ENSEMBLED VOTING MACHINE MODEL SPECS:

Accuracy of the model: 95.80318379160637 %
Cross-validation score: 0.9598352235339181
Confusion Matrix:
[       True  False
    +ve [1200   49]
    -ve [67   1448]
]
'''