import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import csv
import time

import dataCollection
import dataProcessing

from pynput import keyboard

# for knn classification
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler, LabelEncoder

# decision tree learning algorithm
# get data from data processing
data = pd.read_csv('key_log.csv')
press_time = dataProcessing.keypress_processing(data)[0]
wait_time = dataProcessing.searchtime_processing(data)[0]

# add labels to the data and also split them with the rest of the data
press_label = dataProcessing.keypress_processing(data)[1]
press_label = np.ravel(press_label)
wait_label  = dataProcessing.searchtime_processing(data)[1]
wait_label = np.ravel(wait_label)

# split data into train and test data
# add splits for the labels to the corresponding data splits
press_train, press_test, press_label_train, press_label_test = train_test_split(press_time, press_label, test_size=0.2, random_state=42)
wait_train, wait_test, wait_label_train, wait_label_test = train_test_split(wait_time, wait_label, test_size=0.2, random_state=42)

# feature scaling
scaler = StandardScaler()
press_train = scaler.fit_transform(press_train)
press_test  = scaler.transform(press_test)
wait_train  = scaler.fit_transform(wait_train)
wait_test   = scaler.transform(wait_test)

# initialise the clasifier
knn = KNeighborsClassifier(n_neighbors=5)

# train model and make predictions 
## for press times
knn.fit(press_train, press_label_train)
press_predictions_knn = knn.predict(press_test)
## for search times
knn.fit(wait_train, wait_label_train)
wait_predictions_knn = knn.predict(wait_test)

# evaluate {accuracy_score(y_test, y_pred) * 100:.2f}%"
print(f"Model Accuracy for press times with knn: {accuracy_score(press_label_test, press_predictions_knn) * 100:.2f}%")
print(f"Model Accuracy for wait times with knn: {accuracy_score(wait_label_test, wait_predictions_knn) * 100:.2f}%")

# make comparison of knn vs decisiontree ---------------------------------------------------------------
dectree = DecisionTreeClassifier(criterion='entropy', max_depth=5)
dectree.fit(press_train, press_label_train)
press_predictions_dt = dectree.predict(press_test)
dectree.fit(wait_train, wait_label_train)
wait_predictions_dt = dectree.predict(wait_test)

# evaluate accuracy of decision tree
print(f"Model Accuracy for press times with decisiont tree: {accuracy_score(press_label_test, press_predictions_dt) * 100:.2f}%")
print(f"Model Accuracy for wait times with decision tree: {accuracy_score(wait_label_test, wait_predictions_dt) * 100:.2f}%")

# run model on incoming data
# TODO: get this to run untill anomaly has been detected
print("Now run trained model on incomming data:")
log_file = "live_key_log.csv"
with open(log_file, mode='a', newline='', encoding='utf-8') as f:
  csv.writer(f).writerow(["timestamp", "key", "action"])

listener = keyboard.Listener(on_press=dataCollection.on_press_live, on_release=dataCollection.on_release_live)

print(f"--- Logging Started: start typing ---")
listener.start()
time.sleep(10)
# data = pd.read_csv("live_key_log.csv")
data = dataCollection.live_keys
press_data = dataProcessing.keypress_processing(data)[0]
wait_data = dataProcessing.searchtime_processing(data)[0]

press_data_predictions = knn.predict(press_data.values)
wait_data_predictions = knn.predict(wait_data.values)

if (press_data_predictions == 1).any() or (wait_data_predictions == 1).any():
  print("anomaly detected")
  listener.stop()
  print("\n--- Logging Finished: stop typing ---")