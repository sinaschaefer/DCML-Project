import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import csv
import time
import joblib

import dataCollection
import dataProcessing
import model

from pynput import keyboard
from datetime import datetime

# for knn classification
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler, LabelEncoder

# define buffer size
buffer_size = 20

# run model on incoming data
print("Now run trained model on incomming data:")

# load model
loaded_press_model = joblib.load('knn_press_model.pkl')
loaded_wait_model = joblib.load('knn_wait_model.pkl')

def get_live_data():
  # get data with listener
  print(f"--- Logging Started: start typing ---")
  raw_data = dataCollection.live_keys

# This list is shared between the Listener and the Main Loop
raw_event_buffer = []

def on_press_live(key): 
  if hasattr(key, 'char') and key.char is not None:
    k = ord(key.char)
  else:
    k = hash(key)

  raw_event_buffer.append({'timestamp': datetime.now(), 'key': k, 'action': 1})

def on_release_live(key):
  if hasattr(key, 'char') and key.char is not None:
    k = ord(key.char)
  else:
    k = hash(key)

  raw_event_buffer.append({'timestamp': datetime.now(), 'key': k, 'action': 0})

listener = keyboard.Listener(on_press=on_press_live, on_release=on_release_live)
listener.start() 

try:
  while True:
    # check the length of buffer list
    current_count = len(raw_event_buffer)
    
    if current_count < buffer_size:
        print(f"Current Buffer: {current_count}/{buffer_size} keys...", end="\r")
        time.sleep(0.5)
        continue
    
    # convert to DataFrame for processing
    print("\nThreshold reached-> processing...")
    
    # Create DF from the snapshot of the buffer
    data_to_process = pd.DataFrame(raw_event_buffer[:buffer_size])
    
    # data processing
    print("processing data")
    press_data = dataProcessing.keypress_processing(data_to_process)[0]
    wait_data = dataProcessing.searchtime_processing(data_to_process)[0]

    # prediction
    press_data_predictions = loaded_press_model.predict(press_data.values)
    wait_data_predictions = loaded_wait_model.predict(wait_data.values)
    
    # anomaly detection: if label predictions are 1 -> anomaly
    if (press_data_predictions == 1).any() or (wait_data_predictions == 1).any():
      # trigger alert, shut down process
      print(f"ANOMALY DETECTED: stoped logging")
      listener.stop()
      break 
    else:
      print("No anomaly detected")
    
    # sliding window: remove only the oldest 2 events (one press/release pair)
    del raw_event_buffer[:2] 
        
except KeyboardInterrupt:
  print("Monitoring stopped manually.")
  listener.stop()

'''
try:
  while True:
    # get the new data point
    new_batch = get_live_data()

    # check if data is availabe for preprocessing, if not wait
    if new_batch is not None:
      all_collected_data = pd.concat([all_collected_data, new_batch], ignore_index=True)

    if len(all_collected_data) < buffer_size:
      print(f"Collecting data")
      time.sleep(0.5) 
      continue

    # preprocess live data
    print("processing data")
    press_data = dataProcessing.keypress_processing(all_collected_data)[0]
    wait_data = dataProcessing.searchtime_processing(all_collected_data)[0]
    
    # 4. Predict
    press_data_predictions = loaded_press_model.predict(press_data.values)
    wait_data_predictions = loaded_wait_model.predict(wait_data.values)
    
    # anomaly detection: if label predictions are 1 -> anomaly
    if (press_data_predictions == 1).any() or (wait_data_predictions == 1).any():
      # trigger alert, shut down process
      print(f"ANOMALY DETECTED: stoped logging")
      listener.stop()
      break 
    else:
      print("No anomaly detected")
        
    time.sleep(1) # frequency of checks

except KeyboardInterrupt:
  print("Monitoring stopped manually.")
'''