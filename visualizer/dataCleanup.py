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
# def DataCleanup(df, beginMovTime, stop):
#     newdf = df
#     lenght = len(newdf.index)
#     increment = lenght / (stop - beginMovTime)
#     new_time = 0
#     for time in newdf['timestamp']:
#         if (time < beginMovTime) or (time > stop):
#             newdf.drop(newdf[newdf['timestamp'] == time].index, inplace=True)
#         else:
#             newdf.replace(newdf['timestamp'], new_time, inplace=True)
#             new_time += increment
#     return newdf


def videoCleanup(df):
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

    # lenght = len(newdf.index)
    # increment = lenght / (stopExpTime - beginExpTime)
    # new_time = 0
    # for time in newdf['timestamp']:
    #     if (time < beginExpTime) or (time > stopExpTime):
    #         newdf.drop(newdf[newdf['timestamp'] == time].index, inplace=True)
    #     else:
    #         newdf.replace(newdf['timestamp'], new_time, inplace=True)
    #         new_time += increment
    return newdf


# load recordings that you want results from, process is made manually, can we make it automated?
df_marker = loadRecording("./finaltest1_throwmarkerstream_markers1689841738.p", columns=["marker"])
df1 = loadRecording("./finaltest1_xsensdot-dot2_xsensdot-dot2-acc1689841738.p") #hand
df2 = loadRecording("./finaltest1_xsensdot-dot3_xsensdot-dot3-acc1689841738.p") #wrist
dfv = loadRecording("./finaltest1_framemarker1_landmarks1689841738.p")

# adjust the timestamps in each dataset so that they are all based on the same timeframe
baseTimestamp = df1.index[0]
rebaseTimestampMarker(baseTimestamp, df1, df_marker)
rebaseTimestamp(baseTimestamp, df2)
rebaseTimestamp(baseTimestamp, dfv)

# convert the data derived from the pickle file into a csv dataframe for simpler manipulation
df1.to_csv('uluisa_test_hand.csv', sep=',', encoding='utf-8')
df2.to_csv('uluisa_test_wrist.csv', sep=',', encoding='utf-8')
df_marker.to_csv('uluisa_test_marker.csv', sep=',', encoding='utf-8')
dfv.to_csv('uluisa_test_video.csv', sep=',', encoding='utf-8')

df1_csv = pd.read_csv('uluisa_test_hand.csv')
df2_csv = pd.read_csv('uluisa_test_wrist.csv')
m_csv = pd.read_csv('uluisa_test_marker.csv')
dfv_csv = pd.read_csv('uluisa_test_video.csv')

# get total acceleration at each timestamp
getTotalAcc(df1_csv)
getTotalAcc(df2_csv)

beginExpTime = 0
stopExpTime = 0

# determine markers timestamps
for m in m_csv.index:
    markerType = str(m_csv.loc[m]['marker'])
    if markerType == "START_TESTING":
        beginExpTime = m_csv.loc[m]['timestamp']
        beginExp = m_csv.loc[m]['marker']
    elif markerType == "START_THROW":
        startThrTime = m_csv.loc[m]['timestamp']
        startThrExp = m_csv.loc[m]['marker']
    elif markerType == "STOP_THROW":
        stopThrTime = m_csv.loc[m]['timestamp']
        stopThrExp = m_csv.loc[m]['marker']
    elif markerType == "STOP_TESTING":
        stopExpTime = m_csv.loc[m]['timestamp']
        stopExp = m_csv.loc[m]['marker']


# process dataframes
mov1hand = df1_csv #DataCleanup(df1_csv, beginExpTime, stopExpTime)
mov1wrist = df2_csv #DataCleanup(df2_csv, beginExpTime, stopExpTime)
dfv_csv = videoCleanup(dfv_csv)

# save into scv files that will be plotted when main.py is ran
mov1hand.to_csv('uluisa_test_hand_processed.csv', index=False)
mov1wrist.to_csv('uluisa_test_wrist_processed.csv', index=False)
dfv_csv.to_csv('uluisa_test_video_processed.csv', index=False)
