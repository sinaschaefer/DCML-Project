import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import dataProcessing

#from google.colab import files
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from pyod.models.hbos import HBOS
from sklearn.metrics import confusion_matrix, accuracy_score

# for knn classification
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler

# decision tree learning algorithm
# get data from data processing
press_time = dataProcessing.filtered
wait_time = dataProcessing.timeData
# TODO: add labels to the data and also split them with the rest of the data
press_label = dataProcessing.filtered_labels
wait_label = dataProcessing.timeData_labels

# split data into train and test data
# TODO: add splits for the labels to the corresponding data splits
press_train, press_test, press_label_train, press_label_test = train_test_split(press_time, press_label, test_size=0.2, random_state=42)
wait_train, wait_test, wait_label_train, wait_label_test = train_test_split(wait_time, wait_label, test_size=0.2, random_state=42)

# feature scaling
scaler = StandardScaler()
press_train = scaler.fit_transform(press_train)
press_test  = scaler.transform(press_test)
wait_train  = scaler.fit_transform(wait_train)
wait_test   = scaler.transform(wait_test)


# initialise the clasifier and train model
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(press_train, press_label_train)
knn.fit(wait_train, wait_label_train)

# make predictions
press_predictions = knn.predict(press_test)
wait_predictions = knn.predict(wait_test)

# evaluate {accuracy_score(y_test, y_pred) * 100:.2f}%"
print(f"Model Accuracy for press times: {accuracy_score(press_label_test, press_predictions) * 100:.2f}%")
print(f"Model Accuracy for wait times: {accuracy_score(wait_label_test, wait_predictions) * 100:.2f}%")