"""Program that reads a multi-channel time series from LSL and saves timestamp and calculated total acceleration from Xsens DOT """

from pylsl import StreamInlet, resolve_streams
import numpy as np
from Visualizer.helpers.io import rebaseTimestamp
from keyboard import is_pressed
#function to calculate total acceleration 
def calcTotalAcc(data):
    x = data[0]
    y = data[1]
    z = data[2]
    return np.sqrt((x**2)+(y**2)+(z**2))

def main():
    #defining array to store timestamp and total acc
    #for this project, we read data from two sensors, one strapped to the hand (h), and one to the wrist (w)
    handData = []
    #wristData = []

    #define max_acc and counter variables
    max_acc = 0
    counter = 0

    # first resolve a stream on the lab network
    print('looking for streams...')
    stream = resolve_streams()

    # create a new inlet to read from each stream
    # the acceleration is the second stream of each Xsens (that's why we use 1 and 3)
    inlet_h = StreamInlet(stream[1]) #Hydra8-acceleration
    #inlet_w = StreamInlet(stream[3]) #Hydra10-acceleration

    while inlet_h and counter < 500:
        sample_h, timestamp_h = inlet_h.pull_sample()
        #sample_w, timestamp_w = inlet_w.pull_sample()

        timestamp_h = counter
        counter += 1

        sample_h = calcTotalAcc(sample_h)
        #sample_w = calcTotalAcc(sample_w)

        if sample_h > max_acc:
            print('REACHED MAX SPEED:' + str(timestamp_h) + ',' + str(sample_h))
            max_acc = sample_h
        
        handData.append([timestamp_h, sample_h])
        #wristData.append([timestamp_w, sample_w])

    #adjust the timestamps in each dataset
    # baseTimestamp = handData.index[0]
    # rebaseTimestamp(baseTimestamp, wristData)

    np.savetxt("handData.csv", handData, delimiter=',')
    #np.savetxt("wristData.csv", wristData, delimiter=',')


if __name__ == '__main__':
    main()
