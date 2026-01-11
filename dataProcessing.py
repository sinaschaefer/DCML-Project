import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import csv

import dataCollection

from datetime import timedelta

anomalous_window = dataCollection.anomalous_window

# read data from csv file
data = pd.read_csv('key_log.csv')
sortedData = data.sort_values(['key', 'timestamp'])

# convert data into numerical data
sortedData['timestamp'] = pd.to_datetime(sortedData['timestamp'], errors='coerce')
sortedData['action'] = pd.to_numeric(sortedData['action'], errors='coerce').astype('Int64')
sortedData['key'] = pd.to_numeric(sortedData['key'], errors='coerce').astype('Int64')
# shift next row into row such that we have key pairs per row
sortedData['next_timestamp'] = sortedData.groupby('key')['timestamp'].shift(-1)
sortedData['next_action']    = sortedData.groupby('key')['action'].shift(-1)

# convert timestamp data into integers (in 1000 pico seconds or something)
sortedData['timestamp'] = sortedData['timestamp'].astype(int)
sortedData['next_timestamp'] = sortedData['next_timestamp'].astype(int)

# filter out all rows that have same current action as next action and where timestamps are larger than next
filtered = sortedData[sortedData['action'] != sortedData['next_action']]
filtered = sortedData[sortedData['next_timestamp'] > sortedData['timestamp']] #this makes copy warning

# calculate time difference between last and next action
filtered['duration'] = filtered['next_timestamp'] - filtered['timestamp']

# print data
# NOTE: the differences beween up and down pairs does not match the wait time one usualy analyses
#       it is the wait time until the same key is pressed again 
#       however this data is still usefull when detecting different writung patterns (e.g. languages)
print('Key press times')
print(filtered)

# creating labels for key press data
filtered_labels = filtered.sort_values(['timestamp'])
max_time = filtered_labels['timestamp'].max()
treshold = max_time - anomalous_window

press_labels = pd.DataFrame(columns=['label'])
press_labels['label'] = (filtered_labels['timestamp'] >= treshold).astype(int)

print("\npress labels")
print(press_labels)

# ----calculate the wait time between any key presses-------------------------------------------------------
# convert data into numerical data
timeData = data.sort_values(['timestamp'])
timeData['timestamp'] = pd.to_datetime(timeData['timestamp'], errors='coerce')
timeData['action'] = pd.to_numeric(timeData['action'], errors='coerce').astype('Int64')
timeData['key'] = pd.to_numeric(timeData['key'], errors='coerce').astype('Int64')
# shift data from next ron up
timeData['next_timestamp'] = timeData['timestamp'].shift(-1)
timeData['next_action']    = timeData['action'].shift(-1)

# convert timestamps into integers
timeData['timestamp'] = timeData['timestamp'].astype(int)
timeData = timeData.dropna(subset=['next_timestamp']) # drop NANs for safe convertion
timeData['next_timestamp'] = timeData['next_timestamp'].astype(int)

# only take rows that have the key press (1) for the next action
timeData = timeData[timeData['next_action'] == 1]
timeData['wait_time'] = timeData['next_timestamp'] - timeData['timestamp']

print('\nWait times between key presses')
print(timeData)

# creating labels for wait data
timeData_labels = timeData.sort_values(['timestamp'])
max_time = timeData_labels['timestamp'].max()
treshold = max_time - anomalous_window

wait_labels = pd.DataFrame(columns=['label'])
wait_labels['label'] = (timeData_labels['timestamp'] >= treshold).astype(int)

print("\nwait labels")
print(wait_labels)