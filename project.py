import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import csv

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
log_file = "key_log.csv"

# collecting data
def on_press(key):
  try:
    # Get the current timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    
    # Determine the key string representation
    if hasattr(key, 'char') and key.char is not None:
        k = key.char  # Regular alphanumeric keys
    else:
        k = str(key)  # Special keys like Space, Enter, etc.
    # Append to the CSV file
    with open(log_file, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, k])
          
  except Exception as e:
    print(f"Error: {e}")
  except KeyboardInterrupt:
    print("Keyboard interrupt: manually stopped")

  # Collect events until released
  # with keyboard.Listener(on_press=on_press) as listener:
  #   print("Monitoring started... Press Ctrl+C in the terminal to stop.")
  #   listener.join()

def main():
  duration = 30  # Duration in seconds
  
  # Initialize the listener
  listener = keyboard.Listener(on_press=on_press)
  
  print(f"--- Logging Started ---")
  print(f"Monitoring for {duration} seconds...")
  
  # Start the background thread
  listener.start()
  
  # Record the start time
  print("start timer for listening")
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