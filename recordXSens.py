from threading import Thread
from pylsl import resolve_byprop, StreamInlet
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import scipy.signal as signal

#function to calculate total acceleration 
def calcTotalAcc(data):
    x = data[0]
    y = data[1]
    z = data[2]
    return np.sqrt((x**2)+(y**2)+(z**2))

class RecordThread(Thread):

    def __init__(self, inlet):
        Thread.__init__(self, daemon=True)
        self.running = False
        self.inlet = inlet
        #self.timeCorrection = inlet.time_correction()

    def run(self):
        self.running = True
        self.inlet.open_stream(timeout=10.0)
        while self.running:
            sample, ts = self.inlet.pull_sample() #timeout=1.0
            if ts:
                self.timestamp.append(ts)
                sample = calcTotalAcc(sample)
                self.data.append(sample)
                self.timestamp.pop(0)
                self.data.pop(0)
        self.inlet.close_stream()


class VisualizeThread(Thread):

    def __init__(self):
        Thread.__init__(self, daemon=True)
        self.running = False
        #self.timeCorrection = inlet.time_correction()

    def animate(ax):
        #defining arrays to plot timestamp and total acc
        x = []
        y = []
        
        #for each timestamp pulled from stream
        for ts in RecordThread.timestamp:
            #append values to array so that they are displayed
            x.append(ts)
            y.append(calcTotalAcc(sample))
            print(x[])

            
            #this will update the plot window
            if len(x) > 100:
                x.pop(0)
                y.pop(0)

        #clear animation colors
        ax.clear()
            
        #plot
        ax.plot(x, y)

#declaring variables
rawData = []
source_id = "xsensdot-Hydra#6-acc"

# resolve a stream on the lab network
print("Resolving stream")
stream = resolve_byprop('source_id', source_id, timeout=20.0)
print("Found stream")

#record source_id specific inlet 
inlet = StreamInlet(stream[0])
record_thread = RecordThread(inlet)
record_thread.start()
print("Started recording")

#vizualize daata gathered
visualize_thread = VisualizeThread()
visualize_thread.start()
print("started visualize")

#create figure to be displayed
fig1 = plt.figure()
ax1 = fig1.add_subplot(1, 1, 1)
ani1 = animation.FuncAnimation(fig1, VisualizeThread.animate(ax1), interval=100)
print("ploted figure")
plt.show()

time.sleep(5)
record_thread.running = False
record_thread.join()
visualize_thread.running = False
visualize_thread.join()
