import joblib
import numpy as np
import sys
import os

# Add the parent directory to the sys.path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

# Now you can import the module
from feature_extraction.feature_extractor import *

url = input("Enter the URL for prediction: ")

# Extract features from the new data
features = extract_url_features(url)
new_data = np.array(features).reshape(1, -1)

print("[url_having_ip(url),url_length(url),url_short(url),having_at_symbol(url),doubleSlash(url),prefix_suffix(url),sub_domain(url),SSLfinal_State(url),domain_registration(url),favicon(url),port(url),https_token(url),request_url(url),url_of_anchor(url),Links_in_tags(url),sfh(url),email_submit(url),abnormal_url(url),redirect(url),on_mouseover(url),rightClick(url),popup(url),iframe(url),age_of_domain(url),check_dns(url),web_traffic(url),page_rank(url),google_index(url),links_pointing(url),statistical(url)]")

# Load the trained model
classifier = joblib.load('trained_models/randomForest_final.pkl')

# Probabilities of each class
# probabilities = classifier.predict_proba(new_data)

# Predict the class for the new data
prediction = classifier.predict(new_data)

# Print the predicted class
if prediction[0]==1:
    print("Phishy URL")
else:
    print(f"Legitimate URL")
    
# print("Confidence Score: ",  probabilities.max(axis=1))