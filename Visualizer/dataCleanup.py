from helpers.io import loadRecording, rebaseTimestamp, rebaseTimestampMarker
from helpers.plotter import *
from helpers.preprocessing import *
import pandas as pd
import warnings

warnings.simplefilter('ignore', FutureWarning)
# get total acceleration from x, y, z accelerations
def getTotalAcc(df):
    del df['ACC_3']
    x = df['ACC_0']
    y = df['ACC_1']
    z = df['ACC_2']
    df['ACC_Total'] = np.sqrt((x**2)+(y**2)+(z**2))


# cleaning the data: removing indexes before begin experiment and after the last stop (they are irrelevant)
def DataCleanup(df, beginMovTime, stop):
    newdf = df
    lenght = len(newdf.index)
    increment = lenght / (stop - beginMovTime)
    new_time = 0
    for time in newdf['timestamp']:
        if (time < beginMovTime):
            newdf.drop(newdf[newdf['timestamp'] == time].index, inplace=True)
        elif (time > stop):
            newdf.drop(newdf[newdf['timestamp'] == time].index, inplace=True)
        else:
            newdf.replace(newdf['timestamp'], new_time, inplace=True)
            new_time += increment
    #TODO: getMaxAcceleration(df)
    return newdf


def videoCleanup(df, beginMovTime, stop):
    #test if I need this
    newdf = pd.DataFrame(columns=['timestamp', 'frame', 'shoulder angle', 'elbow angle', 'total angle'])
    for i in range(0, len(df), 4):
        if i + 2 < len(df):
            row = df.iloc[i]
            timestamp = row['timestamp']
            frame = row['ACC_0']
            s_ang = row['ACC_1']
            w_ang = row['ACC_2']
            t_ang = row['ACC_3']
            newdf = newdf.append({'timestamp':timestamp, 'frame':frame, 'shoulder angle':s_ang, 'elbow angle':w_ang, 'total angle':t_ang}, ignore_index=True) # type: ignore

    lenght = len(newdf.index)
    increment = lenght / (stop - beginMovTime)
    new_time = 0
    for time in newdf['timestamp']:
        if (time < beginMovTime):
            newdf.drop(newdf[newdf['timestamp'] == time].index, inplace=True)
        elif (time > stop):
            newdf.drop(newdf[newdf['timestamp'] == time].index, inplace=True)
        else:
            newdf.replace(newdf['timestamp'], new_time, inplace=True)
            new_time += increment
            
    return newdf


# load recordings that you want results from, process is made manually, can we make it automated?
df_marker = loadRecording(
    "./luisatest_custommarkerstream_userslulu-custom_marker_stream-2023-07-17_09-17-151689585549.p", columns=["marker"])
df1 = loadRecording("./luisatest_xsensdot-dot2_xsensdot-dot2-acc1689585549.p") #hand
df2 = loadRecording("./luisatest_xsensdot-dot3_xsensdot-dot3-acc1689585549.p") #wrist
dfv = loadRecording(
    "./luisatest_framemarker1_landmarks1689585549.p")

# adjust the timestamps in each dataset so that they are all based on the same timeframe
baseTimestamp = df1.index[0]
rebaseTimestampMarker(baseTimestamp, df1, df_marker)
rebaseTimestamp(baseTimestamp, df2)
rebaseTimestamp(baseTimestamp, dfv)

# convert the data derived from the pickle file into a csv dataframe for simpler manipulation
df1.to_csv('test2_hand.csv', sep=',', encoding='utf-8')
df2.to_csv('test2_wrist.csv', sep=',', encoding='utf-8')
df_marker.to_csv('test2_marker.csv', sep=',', encoding='utf-8')
dfv.to_csv('test2_video.csv', sep=',', encoding='utf-8')

df1_csv = pd.read_csv('test2_hand.csv')
df2_csv = pd.read_csv('test2_wrist.csv')
m_csv = pd.read_csv('test2_marker.csv')
dfv_csv = pd.read_csv('test2_video.csv')

# get total acceleration at each timestamp
getTotalAcc(df1_csv)
getTotalAcc(df2_csv)

# determine markers timestamps
beginExpTime1 = m_csv.loc[0]['timestamp']
beginExp1 = m_csv.loc[0]['marker']
startTime1 = m_csv.loc[1]['timestamp']
startExp1 = m_csv.loc[1]['marker']
stopTime1 = m_csv.loc[2]['timestamp']
stopExp1 = m_csv.loc[2]['marker']

startTime2 = m_csv.loc[3]['timestamp']
startExp2 = m_csv.loc[3]['marker']
stopTime2 = m_csv.loc[4]['timestamp']
stopExp2 = m_csv.loc[4]['marker']

startTime3 = m_csv.loc[5]['timestamp']
startExp3 = m_csv.loc[5]['marker']
stopTime3 = m_csv.loc[6]['timestamp']
stopExp3 = m_csv.loc[6]['marker']

startTime4 = m_csv.loc[7]['timestamp']
startExp4 = m_csv.loc[7]['marker']
stopTime4 = m_csv.loc[8]['timestamp']
stopExp4 = m_csv.loc[8]['marker']

startTime5 = m_csv.loc[9]['timestamp']
startExp5 = m_csv.loc[9]['marker']
stopTime5 = m_csv.loc[10]['timestamp']
stopExp5 = m_csv.loc[10]['marker']

# process dataframes
mov1hand = DataCleanup(df1_csv, beginExpTime1, stopTime5)
mov1wrist = DataCleanup(df2_csv, beginExpTime1, stopTime5)
dfv_csv = videoCleanup(dfv_csv, beginExpTime1, stopTime5)

# save into scv files that will be plotted when main.py is ran
mov1hand.to_csv('test2_hand_processed.csv', index=False)
mov1wrist.to_csv('test2_wrist_processed.csv', index=False)
dfv_csv.to_csv('test2_video_processed.csv', index=False)
