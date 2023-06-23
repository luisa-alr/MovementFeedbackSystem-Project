from helpers.io import loadRecording, rebaseTimestamp, rebaseTimestampMarker
from helpers.plotter import *
from helpers.preprocessing import *
import pandas as pd

# get total acceleration from x, y, z accelerations
def getTotalAcc(df):
    del df['ACC_3']
    x = df['ACC_0']
    y = df['ACC_1']
    z = df['ACC_2']
    df['ACC_Total'] = np.sqrt((x**2)+(y**2)+(z**2))

# get the maximum acceleration from all throws
# def getMaxAcc(df):
#     maxAcc = 0
#     for acc in df['ACC_Total']:
#         if acc > maxAcc:
#             maxAcc = df.loc[df['ACC_Total'] == acc]
#     ts_max = maxAcc.loc[maxAcc['timestamp']]
#     total_max = maxAcc.loc[maxAcc['ACC_Total']]
#     print('The maximum acceleration of: ' + total_max + 'happened at: '+ ts_max)


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
    #getMaxAcc(df)
    return newdf


#load recordings that you want results from, process is made manually, can we make it automated?
df_marker = loadRecording(
    "./new2_custommarkerstream_userslulu-custom_marker_stream-2023-06-14_11-48-231686743384.p", columns=["marker"])
df1 = loadRecording("./new2_xsensdot-hydra6_xsensdot-hydra6-acc1686743384.p")
df2 = loadRecording("./new2_xsensdot-hydra10_xsensdot-hydra10-acc1686743384.p")
#dfv = loadRecording("./test1video_framemarker1_1876c2da-5100-46e6-b44a-06eb6d59cace1686140437.p")

#adjust the timestamps in each dataset so that they are all based on the same timeframe
baseTimestamp = df1.index[0]
rebaseTimestampMarker(baseTimestamp, df1, df_marker)
rebaseTimestamp(baseTimestamp, df2)
#rebaseTimestamp(baseTimestamp, dfv)

#convert the data derived from the pickle file into a csv dataframe for simpler manipulation
df1.to_csv('test1video_h1_acc.csv', sep=',', encoding='utf-8')
df2.to_csv('test1video_h2_acc.csv', sep=',', encoding='utf-8')
df_marker.to_csv('test1video_marker.csv', sep=',', encoding='utf-8')
#dfv.to_csv('test1video_video.csv', sep=',', encoding='utf-8')

df1_csv = pd.read_csv('test1video_h1_acc.csv')
df2_csv = pd.read_csv('test1video_h2_acc.csv')
m_csv = pd.read_csv('test1video_marker.csv')
    #dfv_csv = pd.read_csv('test1video_video.csv')
    
#get total acceleration at each timestamp
getTotalAcc(df1_csv)
getTotalAcc(df2_csv)

#determine markers timestamps
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

#process dataframes
mov1hand = DataCleanup(df1_csv, beginExpTime1, stopTime4)
mov1wrist = DataCleanup(df2_csv, beginExpTime1, stopTime4)
#dfv_csv = DataCleanup(dfv_csv, beginExpTime1, stopTime4)

#save into scv files that will be plotted when main.py is ran
mov1hand.to_csv('throw1_hand.csv', index=False)
mov1wrist.to_csv('throw1_wrist.csv', index=False)
m_csv.to_csv('throw1_marker.csv', index=False)
#dfv_csv.to_csv('test1video_dfv_processed.csv', index=False)
