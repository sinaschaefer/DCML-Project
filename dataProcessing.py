import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import csv
# to plot pretty figures
import matplotlib as mpl
import matplotlib.pyplot as plt

# read data from csv file
data = pd.read_csv('key_log.csv')

# process data 
sortedData = data.sort_values(['key', 'timestamp'])
# shift next row into row such that we have key pairs per row
sortedData['next_timestamp'] = pd.to_datetime(sortedData.groupby('key')['timestamp'].shift(-1), errors='coerce')
sortedData['next_action']    = sortedData.groupby('key')['action'].shift(-1)

# filter out all rows that have same current action as next action
filtered = sortedData[sortedData['action'] != sortedData['next_action']]

# calculate time difference between last and next action
filtered['duration'] = filtered['next_timestamp'] - pd.to_datetime(filtered['timestamp'], errors='coerce')

# print data
# NOTE: the differences beween up and down pairs does not match the wait time one usualy analyses
#      it is the wait time until the same key is pressed again 
print('Key press times')
print(filtered)

# calculate the wait time between any key presses
timeData = data.sort_values(['timestamp'])
timeData['next_timestamp'] = pd.to_datetime(timeData['timestamp'].shift(-1), errors='coerce')
timeData['next_action']    = timeData['action'].shift(-1)
# only take rows that have the key press for the next action
timeData = timeData[timeData['next_action'] == 'D']
timeData['wait_time'] = timeData['next_timestamp'] - pd.to_datetime(timeData['timestamp'], errors='coerce')

print('\nWait times between key presses')
print(timeData)
