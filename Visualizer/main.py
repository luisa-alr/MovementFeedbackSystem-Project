from helpers.plotter import *
from helpers.preprocessing import *
from dataCleanup import *
import matplotlib.pyplot as plt


#specify markers colors for plotting the data
def expMarkers(df_marker, marker, ax):
    for x in df_marker.index:
        mark = str(df_marker["marker"][x])
        if mark == beginExp1:
            ax.axvline(x, color="deeppink")
        elif mark == stopExp1:
            ax.axvline(x, color='red')
        elif mark == stopExp2:
            ax.axvline(x, color='red')
        elif mark == stopExp3:
            ax.axvline(x, color='red')
        elif mark == stopExp4:
            ax.axvline(x, color='red')
        elif mark == stopExp5:
            ax.axvline(x, color='red')
        else:
            ax.axvline(x, color="green")

#determine exp markers
def plotMarkers(ax):
    expMarkers(df_marker, str(beginExp1), ax)
    expMarkers(df_marker, str(stopExp1), ax)  
    expMarkers(df_marker, str(stopExp2), ax) 
    expMarkers(df_marker, str(stopExp3), ax)
    expMarkers(df_marker, str(stopExp4), ax)
    expMarkers(df_marker, str(stopExp5), ax)

# Plotting details for acceleration graph
def plotACC(ax):
    ax.legend(handles=[acc1_hand, acc2_wrist])

    plotMarkers(ax)

    ax.set (xlabel='Seconds', ylabel='Acceleration')
    ax.set_title('Acceleration During Movement')

# Plotting details for angle graph (static line graph)
def plotANG(ax):
    ax.legend(handles=[ang1_shoulder, ang2_elbow])

    plotMarkers(ax)

    ax.set (xlabel='Timestamp', ylabel='Angle')
    ax.set_title('Angle Variation During Movement')

if __name__ == '__main__':
    fig, (ax1, ax2) = plt.subplots(2, figsize=(15, 5))

    # Plot the angle data (static line graph)
    ang1_shoulder, = ax1.plot(dfv_csv['timestamp'], dfv_csv["shoulder angle"], linewidth=.7, color='#9966ff', label='Shoulder-Elbow')
    ang2_elbow, = ax1.plot(dfv_csv['timestamp'], dfv_csv["elbow angle"], linewidth=.7, color='#009999', label='Elbow-Wrist') 
    plotANG(ax1)
    # ani = animation.FuncAnimation(fig, plotANG, frames=len(dfv_csv), interval=10, blit=False)

    #plotting both lines (for hand and wrist) on the same graph
    acc1_hand, = ax2.plot(mov1hand['timestamp'], mov1hand["ACC_Total"], linewidth=.7, color='#FFA500', label='Hand')
    acc2_wrist, = ax2.plot(mov1wrist['timestamp'], mov1wrist["ACC_Total"], linewidth=.7, color='#722F37', label='Wrist')
    plotACC(ax2)

    fig.tight_layout()
    plt.show()



