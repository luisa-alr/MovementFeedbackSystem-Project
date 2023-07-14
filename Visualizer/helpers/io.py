import pickle
import pandas as pd
import numpy as np

def loadRecording(filename, columns=None):
    data = []
    channel_count = 0

    with open(filename, "rb") as file:
        try:
            while True:
                picklePart = pickle.load(file)
                for line in picklePart:
                    tmp = []
                    tmp.append(line[0])
                    tmp.extend(line[1])
                    channel_count = len(line[1])
                    data.append(tmp)
        except EOFError:
            pass

    if columns is None:
        cols = ["timestamp"]
        cols.extend(["ACC_" + str(x) for x in range(channel_count)])
    else:
        cols = ["timestamp"]
        cols.extend(columns)

    df = pd.DataFrame(data, columns=cols)

    df.set_index("timestamp", inplace=True)
    return df

def rebaseTimestampMarker(baseTimestamp, df1, df2):
    df1.index = df1.index - baseTimestamp
    df2.index = df2.index - baseTimestamp

def rebaseTimestamp(baseTimestamp, df3):
    df3.index = df3.index - baseTimestamp

# def rebaseVideo(baseTimestamp, dfv):
#     dfv['timestamp'] = dfv['timestamp'] - baseTimestamp
#     return dfv

def loadVideo(filename):
    pass

