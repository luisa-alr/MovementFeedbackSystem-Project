from helpers.plotter import *
from helpers.preprocessing import *
from dataCleanup import *
import matplotlib.pyplot as plt

# Plotting details for angle bar graph (dynamic bar)
def updateBarANG(ax, percent, color, plotName):
    ax.clear()
    ax.bar(0, percent, color=color)  # Plot bar at percent %
    ax.set_xlim(-0.5, 0.5)
    ax.set_ylim(0, 100)
    ax.set_ylabel('Percentage of Good Angles')
    ax.set_xticks([])
    ax.set_title('Angle Accuracy ' + plotName)
    
    if __name__ == '__main__':
    elbBadAng = 0
    elbGoodAng = 0
    shldrBadAng = 0
    shldrGoodAng = 0
    elbAngPercent = 0
    shldrAngPercent = 0

    total_iterations = len(dfv_csv)  # Total number of iterations

    fig, (ax1, ax2) = plt.subplots(2, figsize=(7, 6))

    # Iterate over your timestamps and angles data
    for index, row in dfv_csv.iterrows():
        # Convert angle to radians
        aShldr = row['shoulder angle']
        aElb = row['elbow angle']

        if aElb > 30 and aElb < 150 or aElb > 210 and aElb < 330:
            elbBadAng += 1
        else:
            elbGoodAng += 1

        # elbAngPercent = elbGoodAng / total_iterations
        elbAngPercent = elbGoodAng / (elbBadAng + elbGoodAng)
        elbAngPercent = elbAngPercent * 100

        # Update the bar plot for elbow angle with different colors
        if elbAngPercent < 25:
            updateBarANG(ax1, elbAngPercent, color='red', plotName='of Elbow-Wrist')
        elif 25 <= elbAngPercent < 50:
            updateBarANG(ax1, elbAngPercent, color='orange', plotName='of Elbow-Wrist')
        elif 50 <= elbAngPercent < 75:
            updateBarANG(ax1, elbAngPercent, color='yellow', plotName='of Elbow-Wrist')
        elif 75 <= elbAngPercent < 90:
            updateBarANG(ax1, elbAngPercent, color='#99ff66', plotName='of Elbow-Wrist')
        elif elbAngPercent >= 90:
            updateBarANG(ax1, elbAngPercent, color='green', plotName='of Elbow-Wrist')

        if aShldr > 30 and aShldr < 150 or aShldr > 210 and aShldr < 330:
            shldrBadAng += 1
        else:
            shldrGoodAng += 1

        #shldrAngPercent = shldrGoodAng / total_iterations
        shldrAngPercent = shldrGoodAng / (shldrBadAng + shldrGoodAng)
        shldrAngPercent = shldrAngPercent *100

        # Update the bar plot for shoulder angle with different colors
        if shldrAngPercent < 25:
            updateBarANG(ax2, shldrAngPercent, color='red', plotName='of Shoulder-Elbow')
        elif 25 <= shldrAngPercent < 50:
            updateBarANG(ax2, shldrAngPercent, color='orange', plotName='of Shoulder-Elbow')
        elif 50 <= shldrAngPercent < 70:
            updateBarANG(ax2, shldrAngPercent, color='yellow', plotName='of Shoulder-Elbow')
        elif 70 <= shldrAngPercent < 90:
            updateBarANG(ax2, shldrAngPercent, color='#99ff66', plotName='of Shoulder-Elbow')
        elif shldrAngPercent >= 90:
            updateBarANG(ax2, shldrAngPercent, color='green', plotName='of Shoulder-Elbow')
        
        # Pause briefly to show the updated plot
        plt.pause(0.1)
    plt.show()