from threading import Thread
from pylsl import StreamInfo, StreamInlet, StreamOutlet, resolve_byprop
import time

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


# class VisualizeThread(Thread):

#     def __init__(self):
#         Thread.__init__(self, daemon=True)
#         self.running = False
#         #self.timeCorrection = inlet.time_correction()

#     def animate(ax):
#         #defining arrays to plot timestamp and total acc
#         x = []
#         y = []
        
#         #for each timestamp pulled from stream
#         for ts in RecordThread.timestamp:
#             #append values to array so that they are displayed
#             x.append(ts)
#             y.append(calcTotalAcc(sample))
#             print(x[])

            
#             #this will update the plot window
#             if len(x) > 100:
#                 x.pop(0)
#                 y.pop(0)

#         #clear animation colors
#         ax.clear()
            
#         #plot
#         ax.plot(x, y)

#declaring variables
rawData = []
source_id = "landmarks"

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


# while loop:
#     if pressed s key:
#         markerOutlet.push_sample(["START_TESTING"])
#     if pressed t key:
#         markerOutlet.push_sample(["START_THROW"])
#         relevance = True
#     if pressed y key:
#         markerOutlet.push_sample(["STOP_THROW"])
#         relevance = False
#     if pressed p key:
#         markerOutlet.push_sample(["STOP_TESTING"])



#vizualize daata gathered
# visualize_thread = VisualizeThread()
# visualize_thread.start()
# print("started visualize")

#create figure to be displayed
# fig1 = plt.figure()
# ax1 = fig1.add_subplot(1, 1, 1)
# ani1 = animation.FuncAnimation(fig1, VisualizeThread.animate(ax1), interval=100)
# print("ploted figure")
# plt.show()

time.sleep(5)
print(record_thread.data)
record_thread.running = False
record_thread.join()

