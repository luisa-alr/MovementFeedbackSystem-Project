# Movement Feedback System (official name TBD)

### A Movement Feedback System (python-based) that uses accelerometers and augmented video (using OpenCV) with landmarks to provide feedback on a specific movement. The code is currently programmed to analyze the basketball free throw technique. All the components of this project become LSL streams in the network and allow time-synchronized recording of the data into binary pickle files.

__The main goal of this project is to__ keep updating this program so that more movement patterns are added and __enable the user to learn and improve their technique in other movements, not limited to sports__.

You will need the following Python libraries (at least):
* wxPython for the GUI
* pylsl for LSL functionality
* cv2 for OpenCV

Tested with python3 on MacOS Ventura 13.4 with an Apple M1 chip. 

## Instructions for running
0. The camera should be positioned in front of the user.
1. Run movVideo.py
   * 1.a. The program will ask for a name to save the file of the video recorded.
   * 1.b. Specify which feedback the user would like. A user can see himself augmented (displaying landmarks) or non-augmented.
   * 1.c. Specify if the user is right-handed or left-handed.
3. Connect two XsensDOT using the LSL app
   * 3.a. Place one Xsens on the wrist and one on top of the hand. The acceleration collected will be used to analyze movement further, checking for the wrist snap while performing the free throw.
4. Run MainGui.py
   * 4.a. __Check Streams__ will discover all currently running LSL streams in the network.
   * 4.b. Select the streams you want to record by selecting (clicking) the __row number__. Use Ctrl to select multiple.
   * 4.c. Press __Connect Streams__. Depending on the number of streams, this might take a while (half a minute).
   * 4.d. Streams are now connected and should display a time offset for each selected stream. The value is based on the streaming system's local clock.
   * 4.e. Hit __Record Streams__ the program will persistently write collected data to the hard drive each interval.
   * 4.f. Specify a folder location and file name. Each stream will have a separate pickle file. A summary file has details about the streams recorded.

## Pushing markers into LSL streams
The movVideo.py file is implemented with an output stream that pushes markers into the lsl recording. The markers should be pushed while the user is performing the movement:
    * press 'a' to determine the start of testing
    * press 's' to determine the start of the free throw movement
    * press 'd' to determine when the free throw movement finishes
    * press 'f' to determine the end of testing
    

## To receive feedback
*  --> After stopping the movVideo.py recording, run angAccuracy to receive a dynamic plot of the angles created by the user's movements during the recording. The plot will display how well/bad the alignment of the shoulder-elbow and elbow-wrist was during the movement. Indicating to the user which body area needs improvement/adjustments.
*  --> After stopping the LSL recording, update the name of the pickle files into dataCleanup.py and run main.py. This program will generate two plots. Plot 1 shows the angle variation of the shoulder-elbow and elbow-wrist angles during movement, while plot 2 displays the acceleration of the hand and wrist during the movement. 
*  + Because streams were recorded through LSL, all plots and data displays are time synchronized. 
