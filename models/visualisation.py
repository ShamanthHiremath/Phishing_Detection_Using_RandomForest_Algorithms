import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os

# Add the parent directory to the sys.path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

# Now you can import the module
from models.RandomForest import *

# Visualizing the confusion matrix
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Class 0', 'Class 1'], yticklabels=['Class 0', 'Class 1'])
plt.title('Confusion Matrix')
plt.xlabel('Predicted Labels')
plt.ylabel('True Labels')
plt.show()

# Features Importance random forest
names = dataset.iloc[:, :-1].columns
importances = classifier.feature_importances_
sorted_importances = sorted(importances, reverse=True)
indices = np.argsort(-importances)

# Plotting variable importance
plt.figure(figsize=(10, 8))
plt.barh(np.arange(len(names)), sorted_importances, align='center')
plt.yticks(np.arange(len(names)), names[indices], fontsize=8)
plt.xlabel('Relative Importance')
plt.title('Feature Importances')
plt.show()