import pandas as pd
import numpy as np
# Importing the dataset
dataset = pd.read_csv("datasets/phishyFeatures.csv")
dataset = dataset.drop('id', axis=1) # removing unwanted column
print(dataset)

headers = dataset.columns

columns = dataset.iloc[:, :-1].values
labels = dataset.iloc[:, -1].values

# Ensure label is a 1D array
labels = labels.ravel()

j = 0
 
avg_label = np.sum(labels)
if avg_label > 0:
    print("Average label: 1")
else:
    print("Average label: -1")

for i in range(0, len(columns[0])):
    print(f"{headers[j]}: {columns[:, i]}")
    one = 0
    neg_one = 0
    zero = 0
    for k in range(0, len(columns[:, i])):
        if(columns[k, i] == 1):
            one += 1
        elif(columns[k, i] == -1):
            neg_one += 1
        else:
            zero += 1
    if(one>zero and one>neg_one):
        print(f"Average label for {headers[j]}: 1")
    elif(neg_one>zero and neg_one>one):
        print(f"Average label for {headers[j]}: -1")
    else:
        print(f"Average label for {headers[j]}: 0")
    
    j+=1
    
    