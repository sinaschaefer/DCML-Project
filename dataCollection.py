import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#from google.colab import files
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from pyod.models.hbos import HBOS
from sklearn.metrics import confusion_matrix, accuracy_score

# for keyboard monitoring
import time
import csv
from pynput import keyboard
from datetime import datetime

# define file name for logging file of keyboard activity
# note: the file will not be overwritten data just get appended
log_file = "key_log.csv"
with open(log_file, mode='a', newline='', encoding='utf-8') as f:
  csv.writer(f).writerow(["timestamp", "key", "action"])

# collecting data
def on_press(key):
  try:
    # get current timestamp
    timestamp = datetime.now()
    
    # determine the key string representation
    if hasattr(key, 'char') and key.char is not None:
        k = key.char  # alphanumeric keys
    else:
        k = str(key)  # special keys e.g. space, enter, etc.

    # append to the CSV file: key, timestamp and D('down' for key press)
    with open(log_file, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, k, "D"])
          
  except Exception as e:
    print(f"Error: {e}")
  except KeyboardInterrupt:
    print("Keyboard interrupt: manually stopped")


def on_release(key):
  try:
    # get current timestamp
    timestamp = datetime.now()

  # determine the key string representation
    if hasattr(key, 'char') and key.char is not None:
        k = key.char  # alphanumeric keys
    else:
        k = str(key)  # special keys e.g. space, enter, etc.
    
    # append to the CSV file: key, timestamp and U('up' for key release)
    with open(log_file, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, k, "U"])
  
  except Exception as e:
    print(f"Error: {e}")
  except KeyboardInterrupt:
    print("Keyboard interrupt: manually stopped")


def main():
  duration = 30  # Duration in seconds
  
  # Initialize the listener
  listener = keyboard.Listener(on_press=on_press, on_release=on_release)
  
  print(f"--- Logging Started ---")
  print(f"Monitoring for {duration} seconds...")
  
  # Start the background thread
  listener.start()
  
  # Record the start time
  start_time = time.time()
  
  try:
    while time.time() - start_time < duration:
      # Calculate remaining time
      remaining = int(duration - (time.time() - start_time))
      print(f"Time remaining: {remaining}", end="\r")
      time.sleep(1) # Check every second
          
  except KeyboardInterrupt:
    print("\nManually stopped by user.")
  
  # Stop the listener thread
  listener.stop()
  print("\n--- Logging Finished ---")
  print(f"Data saved to {log_file}")

if __name__ == "__main__":
  main()