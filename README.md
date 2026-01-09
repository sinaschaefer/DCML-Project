# Data Collection and Machine Learning for Critical Cyber-Physical Systems Project: Keyboard Monitoring to detect Input Anomalies

### About this Project
This Project is in the context of the lecture Data Collection and Machine Learning for Critical Cyber-Physical Systems. 
It is a project that contains both data collection and machine learning on the collected data.
### Running this Project
In order to run this project please make sure that you have all dependencies installed.
YOu can run the code with the command
```
python model.py
```

## Data Collection
In this project we monitor keyboard activity to detect inout anomalies, e.g. a different user or maybe a different input language.
Every person has distinct keystroke dynamics which means the time frames between key presses ad well as how long the key is pressed is unique for every person.
This means we can learn the patterns of one person and then detect wheter the current user is this person or not.
We use the library `pynput` to monitor and collect the keyboard input data in the file `dataCollection.py`

### Data Pre-processing
In order to be ableto use the data we collected with `dataCollection.py`  in the file `key_log.csv`, we need to pre-process this data. 
We do this in the file `dataProcessing.py`. Here we build pairs of key activities and calculate the time difference. This way we can learn how long a user presses a key and the time until the next key press as well as the time until the next key press of the same key.

## Machine Learning
`model.py` 