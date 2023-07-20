from helpers.plotter import *
from helpers.preprocessing import *
from dataCleanup import *
import matplotlib.pyplot as plt


#specify markers colors for plotting the data
def expMarkers(df_marker, ax):
    for x in df_marker.index:
        mark = str(df_marker["marker"][x])
        if mark == "START_TESTING":
            ax.axvline(x, color="deeppink")
        elif mark == "STOP_THROW":
            ax.axvline(x, color='red')
        elif mark == "STOP_TESTING":
            ax.axvline(x, color='BLUE')
        else:
            ax.axvline(x, color="green") 

# Plotting details for acceleration graph
def plotACC(ax):
    ax.legend(handles=[acc1_hand, acc2_wrist])

    expMarkers(df_marker, ax)

    ax.set (xlabel='Seconds', ylabel='Acceleration')
    ax.set_title('Acceleration During Movement')

# Plotting details for angle graph (static line graph)
def plotANG(ax):
    ax.legend(handles=[ang1_shoulder, ang2_elbow])

    expMarkers(df_marker, ax)

    ax.set (xlabel='Timestamp', ylabel='Angle')
    ax.set_title('Angle Variation During Movement')

if __name__ == '__main__':
    fig, (ax1, ax2) = plt.subplots(2, figsize=(15, 5))

    # Plot the angle data (static line graph)
    ang1_shoulder, = ax1.plot(dfv_csv['timestamp'], dfv_csv["shoulder angle"], linewidth=.7, color='#9966ff', label='Shoulder-Elbow')
    ang2_elbow, = ax1.plot(dfv_csv['timestamp'], dfv_csv["elbow angle"], linewidth=.7, color='#009999', label='Elbow-Wrist') 
    plotANG(ax1)

    #plotting both lines (for hand and wrist) on the same graph
    acc1_hand, = ax2.plot(mov1hand['timestamp'], mov1hand["ACC_Total"], linewidth=.7, color='#FFA500', label='Hand')
    acc2_wrist, = ax2.plot(mov1wrist['timestamp'], mov1wrist["ACC_Total"], linewidth=.7, color='#722F37', label='Wrist')
    plotACC(ax2)

    fig.tight_layout()
    plt.show()



