"""Program that reads a multi-channel time series from LSL and saves timestamp and calculated total acceleration from Xsens DOT """

from pylsl import StreamInlet, resolve_streams
import numpy as np
import tkinter as tk

# function to calculate total acceleration


def calcTotalAcc(data):
    x = data[0]
    y = data[1]
    z = data[2]
    return np.sqrt((x**2)+(y**2)+(z**2))


def display(root, sample):
    text2 = tk.Text(root, height=20, width=100)
    text2.tag_configure('big', font=('Arial', 24, 'bold', 'italic'))
    text2.tag_configure('color', foreground='#476042',
                        font=('Tempus Sans ITC', 20, 'bold'))
    text2.insert(tk.END, '\nREACHED MAX SPEED!\n', 'big')
    quote = """Lightening FAST!!""" + """\n\n"""
    quote2 = """Your max acceleration was: """ + str(sample)
    text2.insert(tk.END, quote, 'color')
    text2.insert(tk.END, quote2, 'color')
    text2.pack(side=tk.LEFT)


def liveAcc(sample, i=None):
    root = tk.Tk()
    root.title('Movement Acceleration Feedback')

    display(root, sample)

    root.after(700, root.destroy)

    root.mainloop()


def main():
    # defining array to store timestamp and total acc
    # for this project, we read data from two sensors, one strapped to the hand (h), and one to the wrist (w)
    #handData = []
    #wristData = []
    maxAccData = []

    # define max_acc and counter variables
    max_acc = 100
    counter = 0

    # first resolve a stream on the lab network
    print('looking for streams...')
    stream = resolve_streams()

    # create a new inlet to read from each stream
    # the acceleration is the second stream of each Xsens (that's why we use 1 and 3)
    inlet_h = StreamInlet(stream[1])  # Hydra8-acceleration
    # inlet_w = StreamInlet(stream[3]) #Hydra10-acceleration

    while inlet_h and counter < 60000:
        sample_h, timestamp_h = inlet_h.pull_sample()
        #sample_w, timestamp_w = inlet_w.pull_sample()

        #timestamp_h = counter
        counter += 1

        sample_h = calcTotalAcc(sample_h)
        #sample_w = calcTotalAcc(sample_w)

        if sample_h > max_acc:
            print('REACHED MAX SPEED:' + str(sample_h))
            maxAccData.append([timestamp_h, max_acc])
            max_acc = sample_h
            # show alert that maximum acceleration was reached
            liveAcc(max_acc, 1)

        #handData.append([timestamp_h, sample_h])
        #wristData.append([timestamp_w, sample_w])

    #np.savetxt("handData.csv", handData, delimiter=',')
    #np.savetxt("wristData.csv", wristData, delimiter=',')
    np.savetxt("maxAccData.csv", maxAccData, delimiter=',')


if __name__ == '__main__':
    main()
