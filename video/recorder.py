from threading import Thread
from pylsl import StreamInfo, StreamOutlet, StreamInlet, resolve_byprop, IRREGULAR_RATE
import time
import keyboard
import pandas as pd

class RecordThread(Thread):
    def __init__(self, inlet):
        Thread.__init__(self, daemon=True)
        self.running = False
        self.inlet = inlet
        self.data = []
        self.valuable = True
        #self.timeCorrection = inlet.time_correction()

    def run(self):
        self.running = True
        self.inlet.open_stream(timeout=10.0)
        while self.running:
            sample, ts = self.inlet.pull_sample() #timeout=1.0
            if ts:
                if self.valuable:
                     self.data.append(sample)
        self.inlet.close_stream()
        
class VisualizeThread(Thread):
    def __init__(self):
        Thread.__init__(self, daemon=True)
        self.running = False

#declaring variables
#TODO: add relevant angles to dataframe
df_from_recorder = pd.DataFrame(columns=['timestamp', 'frame', 'shoulder angle', 'elbow angle', 'total angle'])
source_id = "landmarks"
testing = True
relevance = False

# resolve a stream on the lab network
print("Resolving stream")
stream = resolve_byprop('source_id', source_id, timeout=20.0)
print("Found stream")

#record source_id specific inlet 
inlet = StreamInlet(stream[0])
record_thread = RecordThread(inlet)
record_thread.start()
print("Started recording")

# make it work
info = StreamInfo(name='ThrowMarkerStream', type='Markers', channel_count=1, nominal_srate=IRREGULAR_RATE, channel_format='string', source_id='markers') # type: ignore
markerOutlet = StreamOutlet(info)


#loop to get markers onto stream
while testing:
    if keyboard.read_key() == "t":
        markerOutlet.push_sample(["START_TESTING"])
    if keyboard.read_key() == "s":
        markerOutlet.push_sample(["START_THROW"])
        relevance = True
    if keyboard.read_key() == "d":
        markerOutlet.push_sample(["STOP_THROW"])
        relevance = False
    if keyboard.read_key() == "y":
        markerOutlet.push_sample(["STOP_TESTING"])
        testing = False
    if relevance == True:
        df_from_recorder = df_from_recorder.append({'timestamp':timestamp, 'frame':frame, 'shoulder angle':s_ang, 'elbow angle':w_ang, 'total angle':t_ang}, ignore_index=True) # type: ignore

# time.sleep(5)
print(record_thread.data)
record_thread.running = False
record_thread.join()

