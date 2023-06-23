"""Program that reads a multi-channel time series from LSL and plots timestamp and calculated total acceleration from Xsens DOT """

from pylsl import StreamInlet, resolve_streams
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

#function to calculate total acceleration 
def calcTotalAcc(data):
        x = data[0]
        y = data[1]
        z = data[2]
        return np.sqrt((x**2)+(y**2)+(z**2))

def animate(ax):
    #defining arrays to plot timestamp and total acc
    x = []
    y = []

    # create a new inlet to read from the stream
    inlet = StreamInlet(stream[1])
    sample, timestamp = inlet.pull_sample()
    
    #for each timestamp pulled from stream
    if timestamp:
        #append values to array so that they are displayed
        x.append(timestamp)
        y.append(calcTotalAcc(sample))
        
        #this will update the plot window
        if len(x) > 100:
            x.pop(0)
            y.pop(0)

    #clear animation colors
    ax.clear()
        
    #plot
    ax.plot(x, y)


if __name__ == '__main__':
    # first resolve a stream on the lab network
    print('looking for stream...')
    stream = resolve_streams()

    #create figures to be displayed
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(1, 1, 1)

    ani1 = animation.FuncAnimation(fig1, animate(ax1), interval=1000)

    plt.show()
