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

# for classifiers
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler, LabelEncoder

# define buffer size
buffer_size = 20

print("Now run trained model on incomming data:")

# load models
loaded_press_model_knn = joblib.load('knn_press_model.pkl')
loaded_wait_model_knn = joblib.load('knn_wait_model.pkl')
loaded_press_model_dt = joblib.load('dt_press_model.pkl')
loaded_wait_model_dt = joblib.load('dt_wait_model.pkl')

def get_live_data():
  # get data with listener
  print(f"--- Logging Started: start typing ---")
  raw_data = dataCollection.live_keys

# list is shared between the Listener and the Main Loop
raw_event_buffer = []

# build and initialaise the listener
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
    # check length of buffer list
    current_count = len(raw_event_buffer)
    
    if current_count < buffer_size:
      print(f"Current Buffer: {current_count}/{buffer_size} keys...", end="\r")
      time.sleep(0.5)
      continue
    
    # convert to DataFrame for processing
    print("\nThreshold reached-> processing...")
    
    # create DF from the snapshot of the buffer
    data_to_process = pd.DataFrame(raw_event_buffer[:buffer_size])
    
    # data processing
    print("processing data")
    press_data = dataProcessing.keypress_processing(data_to_process)[0]
    wait_data = dataProcessing.searchtime_processing(data_to_process)[0]

    # prediction
    press_data_predictions_knn = loaded_press_model_knn.predict(press_data.values)
    wait_data_predictions_knn = loaded_wait_model_knn.predict(wait_data.values)

    press_data_predictions_dt = loaded_press_model_dt.predict(press_data.values)
    wait_data_predictions_dt = loaded_wait_model_dt.predict(wait_data.values)

    print(f"press_label knn: {press_data_predictions_knn}")
    print(f"wait_labels knn: {wait_data_predictions_knn}")
    print(f"press_label dt: {press_data_predictions_dt}")
    print(f"wait_labels dt: {wait_data_predictions_dt}")
    
    # anomaly detection: if label predictions are 1 -> anomaly
    if ((press_data_predictions_knn == 1).any() or (wait_data_predictions_knn == 1).any()
       or (press_data_predictions_dt == 1).any() or (wait_data_predictions_dt == 1).any()):
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
