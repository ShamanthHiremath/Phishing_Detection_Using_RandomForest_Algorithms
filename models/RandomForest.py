# importing libraries
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

# Importing the dataset
dataset = pd.read_csv("datasets/phishyFeatures.csv")
dataset = dataset.drop('id', axis=1) # removing unwanted column

x = dataset.iloc[:, :-1].values
y = dataset.iloc[:, -1].values

# Ensure y is a 1D array
y = y.ravel()

# Splitting the dataset into training set and test set
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=0)

# Applying grid search to find best performing parameters 
from sklearn.model_selection import GridSearchCV
parameters = [{'n_estimators': [100, 700],
    'max_features': ['sqrt', 'log2'],
    'criterion': ['gini', 'entropy']}]

grid_search = GridSearchCV(RandomForestClassifier(), parameters, cv=5, n_jobs=-1)
grid_search.fit(x_train, y_train)

acc = grid_search.best_score_
print("Best Accuracy =", str(acc* 100), " %")

# Printing best parameters 
print("Best Accuracy =", str(acc))
print("Best parameters =", str(grid_search.best_params_))

# Fitting RandomForest regression with best params 
best_params = grid_search.best_params_
classifier = RandomForestClassifier(n_estimators=best_params['n_estimators'], 
                                    criterion=best_params['criterion'], 
                                    max_features=best_params['max_features'],  
                                    random_state=0)
classifier.fit(x_train, y_train)

# Predicting the test set results
y_pred = classifier.predict(x_test)

# Cross-validation score
from sklearn.model_selection import cross_val_score
val_score = cross_val_score(classifier, x_train, y_train, cv=3, scoring='accuracy').mean()
print(f"Cross-validation score: {val_score}")

# Confusion matrix
from sklearn.metrics import confusion_matrix, pair_confusion_matrix
cm = confusion_matrix(y_test, y_pred)
print(cm)

'''
# Visualizing the confusion matrix
pair_confusion_matrix(classifier, x_test, y_test, display_labels=['Class 0', 'Class 1'], cmap=plt.cm.Blues, values_format='d')
plt.show()



# Features Importance random forest
names = dataset.iloc[:, :-1].columns
importances = classifier.feature_importances_
sorted_importances = sorted(importances, reverse=True)
indices = np.argsort(-importances)
var_imp = pd.DataFrame(sorted_importances, names[indices], columns=['importance'])

# Plotting variable importance
plt.title("Variable Importances")
plt.barh(np.arange(len(names)), sorted_importances, height=0.7)
plt.yticks(np.arange(len(names)), names[indices], fontsize=7)
plt.xlabel('Relative Importance')
plt.show()
'''
# Pickle file joblib
joblib.dump(classifier, 'trained_models/randomForest_final.pkl', protocol=4)

'''
RANDOM FOREST MODEL SPECS:

Accuracy of the model: 97.31789746464618  %
Best Accuracy = 0.9731789746464618
Best parameters = {'criterion': 'entropy', 'max_features': 'log2', 'n_estimators': 100}

Cross-validation score: 0.9693641373263504

Confusion Matrix:
[       True  False
    +ve [1186   63]
    -ve [26   1489]
]
'''