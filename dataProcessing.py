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

# process data 
sortedData = data.sort_values(['key', 'timestamp'])
# shift next row into row such that we have key pairs per row
sortedData['timestamp'] = pd.to_datetime(sortedData['timestamp'], errors='coerce')
sortedData['next_timestamp'] = sortedData.groupby('key')['timestamp'].shift(-1)
sortedData['next_action']    = sortedData.groupby('key')['action'].shift(-1)

# convert timestamp data into integers (in 1000 pico seconds or something)
#sortedData['timestamp'] = sortedData['timestamp'].astype(int)
#sortedData['next_timestamp'] = sortedData['next_timestamp'].astype(int)

# filter out all rows that have same current action as next action and where timestamps are larger than next
filtered = sortedData[sortedData['action'] != sortedData['next_action']]
filtered = sortedData[sortedData['next_timestamp'] > sortedData['timestamp']]

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
treshold = max_time - pd.Timedelta(seconds=anomalous_window)
filtered_labels['label'] = (filtered_labels['timestamp'] >= treshold).astype(int)

print(filtered_labels)

# calculate the wait time between any key presses
timeData = data.sort_values(['timestamp'])
timeData['timestamp'] = pd.to_datetime(timeData['timestamp'], errors='coerce')
timeData['next_timestamp'] = timeData['timestamp'].shift(-1)
timeData['next_action']    = timeData['action'].shift(-1)

# convert timestamps into integers
#timeData['timestamp'] = timeData['timestamp'].astype(int)
#timeData['next_timestamp'] = timeData['next_timestamp'].astype(int)

# only take rows that have the key press for the next action
timeData = timeData[timeData['next_action'] == 'D']
timeData['wait_time'] = timeData['next_timestamp'] - timeData['timestamp']

print('\nWait times between key presses')
print(timeData)

# creating labels for wait data
timeData_labels = timeData.sort_values(['timestamp'])
max_time = timeData_labels['timestamp'].max()
treshold = max_time - pd.Timedelta(seconds=anomalous_window)
timeData_labels['label'] = (timeData_labels['timestamp'] >= treshold).astype(int)

print(timeData_labels)