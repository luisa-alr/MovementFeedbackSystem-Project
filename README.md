# Xterity
A recording application (python-based) that discovers LSL streams in the network and allows time-synchronized recording into binary pickle files.
You will need the following python libraries (at least):
* wxPython for the GUI
* pylsl for LSL functionality

Tested with python3 on Windows. Note that the implementation of pickle might differ between OS and most importantly between python2 and python3.
De-pickling python2 recordings will not be possible with python3.

## Instructions for recording
1. Run "python MainGui.py"
2. __Check Streams__ will discover all currently running LSL streams in the network. You might need to configure your firewall appropriately to allow access.
3. Select streams you want to record by selecting (clicking) the __row number__. Use Ctrl to select multiple.
4. Press __Connect Streams__. Depending on the number of streams this might take a while (half a minute). If streams are slow to respond this command might fail (possibly crashing emXterity); Repeat by restarting emXterity if needed.
5. Streams are now connected and should display a time offset for each selected stream. The value is based on the streaming system's local clock.
6. Specify a persistence duration (emXterity will persistently write collected data to the hard drive each interval) and hit __Record Streams__.
7. Specify a folder location and file name. Each stream will have a separate pickle file. A summary file contains all recorded streams and their details.

emXterity implements some safeguarding against loss of data such as persistence duration and automatic reconnect to lost streams if they become available again (through LSL reconnect via source id).
Additionally, a final summary shows estimated recording times for each streams based on the supplied sampling rate and received datapoints.
If these values are off (or different from what you expect), the specific streams might have been disconnected during the recording or did not deliver data up to its specified sampling rate.

## Specifying markers during the recording
emXterity supplies a python-based marker stream implementation of LSL (streams/MarkerStream.py). You can create individual strings markers for your experiment and send them as LSL stream. Do not forget to record this marker stream as well.
1. Run "python MarkerStream.py"
2. Specify your individual markers. One per line.
3. Hit __Generate Marker Buttons__. The LSL stream is now active. __Select it when recording with emXterity__.
4. Whenever you want to send a marker hit the respective button.

## Loading a recording

### read_pickle.py
You may use utils/read_pickle.py to extract data from recorded streams. Note that all streams within one recording are fully time-synchronized.

__Unpickling python2 recording might not work with python3!__