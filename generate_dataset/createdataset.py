from feature_extraction import concat_features as extract
# import numpy as np
import pandas as pd
import csv
import os


def create_dataset(file_path, features_csv_file):
    
    data = pd.read_csv(file_path)
    
    if os.path.exists(features_csv_file):
    # If the file exists, truncate it to clear its contents
        with open(features_csv_file, 'w', newline='') as csvfile:
            csvfile.truncate()
            print(f"Cleared existing data in {features_csv_file}")
            
    # Open a CSV file to save the data
    with open(features_csv_file, 'w', newline='') as csvfile:
        #  write features parallely
        fieldnames = ['id', 'having_IP_Address', 'URL_Length', 'Shortining_Service', 'having_At_Symbol', 'double_slash_redirecting', 'Prefix_Suffix', 'having_Sub_Domain', 'SSLfinal_State', 'Domain_registeration_length', 'Favicon', 'port', 'HTTPS_token', 'Request_URL', 'URL_of_Anchor', 'Links_in_tags', 'SFH', 'Submitting_to_email', 'Abnormal_URL', 'Redirect', 'on_mouseover', 'RightClick', 'popUpWidnow', 'Iframe', 'age_of_domain', 'DNSRecord', 'web_traffic', 'Page_Rank', 'Google_Index', 'Links_pointing_to_page', 'Statistical_report', 'Result']

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
            
    id = 1
    
    for url, label in zip(data['Domain'], data['Label']):
        
        features = [id] # Adds id to the beginning of the features list
        features.append(extract.extract_url_features(url)) # Extracts URL features and appends to the features list 
        features.append(label) # Appends the label to the features list
        
        id += 1
        
        # Writing data to each row of the new dataset file
        writer.writerow(features)
        
    print(f"Dataset created successfully in {features_csv_file}")
    
    
create_dataset('datasets\3.new_legitimate_dataset.csv', 'datasets\3.legitimate.csv')



