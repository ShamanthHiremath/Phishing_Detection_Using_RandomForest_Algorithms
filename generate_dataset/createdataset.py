import numpy as np
import pandas as pd
import csv
import os
import sys

# Add the parent directory to the sys.path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)
    
from feature_extraction.feature_extractor import *

def create_dataset(file_path, features_csv_file):
    
    data = pd.read_csv(file_path)
    
    if os.path.exists(features_csv_file):
        # If the file exists, truncate it to clear its contents
        with open(features_csv_file, 'w', newline='') as csvfile:
            csvfile.truncate()
            print(f"Cleared existing data in {features_csv_file}")
            
    # Open a CSV file to save the data
    with open(features_csv_file, 'w', newline='') as csvfile:
        fieldnames = ['id', 'having_IP_Address', 'URL_Length', 'Shortining_Service', 'having_At_Symbol', 'double_slash_redirecting', 'Prefix_Suffix', 'having_Sub_Domain', 'SSLfinal_State', 'Domain_registeration_length', 'Favicon', 'port', 'HTTPS_token', 'Request_URL', 'URL_of_Anchor', 'Links_in_tags', 'SFH', 'Submitting_to_email', 'Abnormal_URL', 'Redirect', 'on_mouseover', 'RightClick', 'popUpWidnow', 'Iframe', 'age_of_domain', 'DNSRecord', 'web_traffic', 'Page_Rank', 'Google_Index', 'Links_pointing_to_page', 'Statistical_report', 'Result']

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
    id = 1
    
    for url, label in zip(data['Domain'], data['Label']):
        features = {'id': id}  # Create a dictionary for features
        features.update(extract_url_features(url))  # Extract URL features and update dictionary
        features['Result'] = label  # Add label to features
        
        writer.writerow(features)
        id += 1
        
    print(f"Dataset created successfully in {features_csv_file}")

# Adjusted file paths with raw string literals
create_dataset(r'datasets\reference_datasets\3.legitimate.csv', r'datasets\new_custom_dataset\3.newdataset.csv')
