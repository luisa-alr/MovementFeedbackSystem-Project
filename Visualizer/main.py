from helpers.plotter import *
from helpers.preprocessing import *
from helpers.dataCleanup import *

#specify markers colors for plotting the data
def expMarkers(df_marker, marker):
    for x in df_marker.index:
        if str(df_marker["marker"][x]) == beginExp1:
            plt.axvline(x, color="deeppink")
        elif str(df_marker["marker"][x]) == stopExp1:
            plt.axvline(x, color='red')
        elif str(df_marker["marker"][x]) == stopExp2:
            plt.axvline(x, color='red')
        elif str(df_marker["marker"][x]) == stopExp3:
            plt.axvline(x, color='red')
        elif str(df_marker["marker"][x]) == stopExp4:
            plt.axvline(x, color='red')
        else:
            plt.axvline(x, color="green")

#plotting details
def plotLsl():
    plt.legend(handles=[line1, line2])
    expMarkers(df_marker, str(beginExp1))
    expMarkers(df_marker, str(stopExp1))  
    expMarkers(df_marker, str(stopExp2)) 
    expMarkers(df_marker, str(stopExp3))
    expMarkers(df_marker, str(stopExp4))
    plt.xlabel('Seconds')
    plt.ylabel('Acceleration')

if __name__ == '__main__':
    #plotting both lines (for hand and wrist) on the same graph
    line1, = plt.plot(mov1hand['timestamp'], mov1hand["ACC_Total"], linewidth=.7, color='#FFA500', label='Hand')
    line2, = plt.plot(mov1wrist['timestamp'], mov1wrist["ACC_Total"], linewidth=.7, color='#722F37', label='Wrist')

    plotLsl()
    plt.show()



