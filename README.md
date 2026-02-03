# Data Collection and Machine Learning for Critical Cyber-Physical Systems Project: Keyboard Monitoring to Detect Input Anomalies

### About this Project
This Project is in the context of the lecture Data Collection and Machine Learning for Critical Cyber-Physical Systems. 
It is a project that contains both data collection and machine learning on the collected data.
### Running this Project
In order to run this project please make sure that you have all dependencies installed.

The file `key_log.csv` contains data I have collected on which the saved model has been trained.
In case you prefer to collect your own data, please make sure that the `key_log.csv` file is empty before collecting your data, otherwise it will contain both my collected data that is already in the file as well as your newly collected data and the labeling will no longer match.
To collect your own data please run the following command after emptying the `key_log.csv` file, and then follow the instructions on the terminal
```
python dataCollection.py
```
You can then run the model with the command
```
python model.py
```
If you want to run the trained model on live data input run the following command and follow the instructions on the terminal output
```
python realtimeModel.py
```

## Data Collection
In this project we monitor keyboard activity to detect input anomalies, e.g. a different user.
Every person has distinct keystroke dynamics which means the time frames between key presses ad well as how long the key is pressed is unique for every person.
This means we can learn the patterns of one person and then detect whether the current user is said person or not.
We use the library `pynput` to monitor and collect the keyboard input data in the file `dataCollection.py`

### Data Pre-processing
In order to be able to use the data we collected with `dataCollection.py` in the file `key_log.csv`, we need to pre-process this data. 
We do this in the file `dataProcessing.py`. Here we build pairs of key activities and calculate the time difference. This way we can learn how long a user presses a key and the time until the next key press as well as the time until the next key press of the same key.

## Machine Learning
We compare two classification algorihtms on the collected data in the file `model.py`. 

### K-nearest-neighbours classification
We use the k-nearest-neighbour classifier with a neighbour count of 5 and then determine the accuracy of the predictions made by this classifier for both the press times and the search times.

### Decision-tree classification
The other clasifier we implement is the decision-tree classifier with a maximum depth of 5. Again, we determine the accuracy of this classifier's predictions for both the press times and the wait times.

## Anomaly detection on live data
After training the models, we save them and then load them in the file `raltimeModel.py`.
Then we use the pretrained model to detect anomalies on the incoming data. We collect the live data in a similar fashion to the data collection step in the `dataCollection.py` file, but instead of writing it into a CSV file, we collect it in a buffer and then pass it to the data pre-processing and then to the model to predict possible anomalies.
If an anomaly is detected, we stop the live data monitoring.