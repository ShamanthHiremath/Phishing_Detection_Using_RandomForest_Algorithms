import joblib
import numpy as np
import sys
import os

# Add the parent directory to the sys.path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

# Now you can import the module
from feature_extraction.concat_features import *

url = input("Enter the URL for prediction: ")

# Extract features from the new data
features = extract_url_features(url)
new_data = np.array(features).reshape(1, -1)

# Load the trained model
classifier = joblib.load('trained_models/randomForest_final.pkl')

# Predict the class for the new data
prediction = classifier.predict(new_data)

# Print the predicted class
if prediction[0]==1:
    print("Phishy URL")
else:
    print(f"Legitimate URL")
