from threading import Thread
from pylsl import StreamInfo, StreamOutlet, StreamInlet, resolve_byprop, IRREGULAR_RATE
import keyboard
import pandas as pd

class RecordThread(Thread):
    def __init__(self, inlet):
        Thread.__init__(self, daemon=True)
        self.running = False
        self.inlet = inlet
        self.data = []
        #self.timeCorrection = inlet.time_correction()

    def run(self):
        self.running = True
        while self.running:
            sample, ts = self.inlet.pull_sample() 
            if ts:
                self.data.append([ts, sample])
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
    if keyboard.read_key() == "a":
        markerOutlet.push_sample(["START_TESTING"])
    if keyboard.read_key() == "s":
        markerOutlet.push_sample(["START_THROW"])
        relevance = True
        for record in record_thread.data:
            # Extract the relevant angles from the data sample
            timestamp = record['timestamp']
            frame = record['frame']
            shoulder_angle = record['shoulder angle']
            elbow_angle = record['elbow_angle']
            total_angle = record['total_angle']
            
        # Append the angles and timestamp to the dataframe
        df_from_recorder = df_from_recorder.append({'timestamp': timestamp, 'frame': frame, 'shoulder angle': shoulder_angle, 'elbow angle': elbow_angle, 'total angle': total_angle}, ignore_index=True) #type: ignore
        
    if keyboard.read_key() == "d":
        markerOutlet.push_sample(["STOP_THROW"])
        relevance = False
    if keyboard.read_key() == "f":
        markerOutlet.push_sample(["STOP_TESTING"])
        testing = False
    

# time.sleep(5)
print(record_thread.data)
record_thread.running = False
record_thread.join()

