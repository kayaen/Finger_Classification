# Finger_Classification
Classify the myo armband data using matlab nntool and use the coefficient of the result of classification as a multiplier to obtain real time result.

First, run record_data.py and it will connect and gather EMG data from myo armband. In Windows, shutdown the MyoConnect application because the python code will communicate via bluetooth. In Linux, give permission to bluetooth usb dongle. First input is number of example data and second is number of waiting between two hand position. If you don't want to wait, enter 1. At the end of the process, the recorded data is transformed to matlab data if press the 's' when it asks.

Second, run the personal_finger_train.m to classify the recorded data with neural network algorithm in Matlab. I tried the different neural network modules in python but they are not successful and efficient as Matlab. So, the code trains the neural network and gives the coefficient of the neural network to use in real time classification. 

Third, run data_classify_ardu_serial.py to classify the present data. If you connect a device to read from serial communication, the device can control servo motors to change finger positions. 
