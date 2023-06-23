# program that analyses movement patterns as a direct real-time feedback approach to sport/movement improvement
import cv2
import mediapipe as mp
import helpers
import os
import uuid
import math as m
from pylsl import StreamInlet, resolve_streams
import numpy as np

from pylsl import StreamInfo, StreamOutlet

class add_Xsens:
    #function to calculate total acceleration 
    def calcTotalAcc(data):
        x = data[0]
        y = data[1]
        z = data[2]
        return np.sqrt((x**2)+(y**2)+(z**2))

    def main():
        #defining array to store timestamp and total acc
        #for this project, we read data from two sensors, one strapped to the hand (h), and one to the wrist (w)
        handData = []
        #wristData = []

        #define max_acc and counter variables
        max_acc = 0
        counter = 0

        # first resolve a stream on the lab network
        print('looking for streams...')
        stream = resolve_streams()

        # create a new inlet to read from each stream
        # the acceleration is the second stream of each Xsens (that's why we use 1 and 3)
        inlet_h = StreamInlet(stream[1]) #Hydra8-acceleration
        #inlet_w = StreamInlet(stream[3]) #Hydra10-acceleration

        while inlet_h and counter < 500:
            sample_h, timestamp_h = inlet_h.pull_sample()
            #sample_w, timestamp_w = inlet_w.pull_sample()

            timestamp_h = counter
            counter += 1

            sample_h = add_Xsens.calcTotalAcc(sample_h)
            #sample_w = calcTotalAcc(sample_w)

            if sample_h > max_acc:
                acc_string = 'REACHED MAX SPEED:' + str(sample_h)
                cv2.putText(image, acc_string, (10, 700), font, 0.9, red, 2)
                max_acc = sample_h
            
            handData.append([timestamp_h, sample_h])
            #wristData.append([timestamp_w, sample_w])

        #adjust the timestamps in each dataset
        # baseTimestamp = handData.index[0]
        # rebaseTimestamp(baseTimestamp, wristData)

        np.savetxt("handData.csv", handData, delimiter=',')
        #np.savetxt("wristData.csv", wristData, delimiter=',')


# define function to determine offset distance between two points
def findDistance(x1, x2, y1, y2):
    dist = m.sqrt((x2-x1)**2 + (y2-y1)**2)
    return dist

# Angle / inclination of landmark lines
def findAngle(x1, y1, x2, y2):
    theta = m.acos((y2-y1)*(-y1) / (m.sqrt((x2-x1)**2 + (y2-y1)**2)*y1))
    degree = int(180/m.pi)*theta
    return degree

# When performing a bad movement, send alert
def sendWarning(x):
    pass

def createOutlet(index, filename):
    streamName = 'FrameMarker'+str(index+1)
    info = StreamInfo(name=streamName,
                      type='videostream',
                      channel_format='float32',
                      channel_count=1,
                      source_id=str(uuid.uuid4()))

    dir_file = os.path.dirname(filename)
    if not os.path.exists(dir_file):
        print('Creating folder', dir_file)
        os.makedirs(dir_file)
    videoFile = filename
    info.desc().append_child_value("videoFile", videoFile)
    return StreamOutlet(info)


# font
font = cv2.FONT_HERSHEY_SIMPLEX

# Colors (in BGR)
blue = (255, 127, 0)
red = (50, 50, 255)
green = (0, 205, 0)
yellow = (0, 255, 255)

# movement specification
move = 'throwR'

# get current directory path
dir_out = os.path.dirname(os.path.realpath(__file__))

# create capture object
# For webcam input replace file name with 0.
dev = 0
cap = cv2.VideoCapture(dev)

if __name__ == "__main__":
    # Meta.
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    filename = os.path.join(dir_out, 'outputMOVE' + '.avi')
    out = cv2.VideoWriter(filename, fourcc, fps, (int(width), int(height)))
    frameCounter = 1
    outlet = createOutlet(dev, filename)
    mov_count = 0
    bad_frames = 0
    good_frames = 0

    # initialize Pose estimator
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    poselandmarks_list = helpers.poselandmarks_list

    pose = mp_pose.Pose(
        min_detection_confidence=0.9,
        min_tracking_confidence=0.9)

    while True:
        # Capture frames.
        success, frame = cap.read()
        if not success:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        # convert the frame to RGB format
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # process the RGB frame to get the result
        keypoints = pose.process(image)

        # Convert the image back to BGR.
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Use lm and lmPose as representative of the following methods.
        lm = keypoints.pose_landmarks
        lmPose = mp_pose.PoseLandmark

        # draw detected skeleton on the frame
        mp_drawing.draw_landmarks(
            image, keypoints.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        if move == 'throwR':
            # 11 - left shoulder
            l_shldr_x = int(lm.landmark[lmPose.LEFT_SHOULDER].x * width)
            l_shldr_y = int(lm.landmark[lmPose.LEFT_SHOULDER].y * height)
            # 12 - right shoulder
            r_shldr_x = int(lm.landmark[lmPose.RIGHT_SHOULDER].x * width)
            r_shldr_y = int(lm.landmark[lmPose.RIGHT_SHOULDER].y * height)
            # 14 - right elbow
            r_elb_x = int(lm.landmark[lmPose.RIGHT_ELBOW].x * width)
            r_elb_y = int(lm.landmark[lmPose.RIGHT_ELBOW].y * height)
            # 16 - right wrist
            r_wrs_x = int(lm.landmark[lmPose.RIGHT_WRIST].x * width)
            r_wrs_y = int(lm.landmark[lmPose.RIGHT_WRIST].y * height)
            # 24 - right hip
            r_hip_x = int(lm.landmark[lmPose.RIGHT_HIP].x * width)
            r_hip_y = int(lm.landmark[lmPose.RIGHT_HIP].y * height)

            # get xsens data from lsl stream 
            add_Xsens.main()

            # Calculate angles
            # elbow-shoulder angulation
            es_ang = findAngle(r_elb_x, r_elb_y, r_shldr_x, r_shldr_y)
            # elbow-wrist angulation
            ew_ang = findAngle(r_elb_x, r_elb_y, r_wrs_x, r_wrs_y)

            # Create landmarks nodes
            cv2.circle(image, (r_shldr_x, r_shldr_y), 7, yellow, -1)
            cv2.circle(image, (r_hip_x, r_hip_y), 7, yellow, -1)
            cv2.circle(image, (l_shldr_x, l_shldr_y), 7, yellow, -1)
            cv2.circle(image, (r_elb_x, r_elb_y), 7, yellow, -1)
            cv2.circle(image, (r_wrs_x, r_wrs_y), 7, yellow, -1)

            # Join movement landmarks
            cv2.line(image, (r_shldr_x, r_shldr_y),
                     (r_hip_x, r_hip_y), green, 4)
            cv2.line(image, (l_shldr_x, l_shldr_y),
                     (r_shldr_x, r_shldr_y), green, 4)
            cv2.line(image, (r_shldr_x, r_shldr_y),
                     (r_elb_x, r_elb_y), green, 4)
            cv2.line(image, (r_elb_x, r_elb_y), (r_wrs_x, r_wrs_y), green, 4)

            # Create movement conditions
            if ew_ang > 40:
                # Join movement landmarks (movement to be improved).
                cv2.line(image, (r_elb_x, r_elb_y), (r_wrs_x, r_wrs_y), red, 4)
            if es_ang > 40 and es_ang < 100:
                # Join movement landmarks (movement to be improved).
                cv2.line(image, (r_shldr_x, r_shldr_y),
                         (r_elb_x, r_elb_y), red, 4)
                
            # Text strings for display.
            angle_text_string = 'Arm : ' + str(int(es_ang)) + '  Forearm : ' + str(int(ew_ang))
            throw_count_string = 'Throw #: ' + str(int(mov_count))

            # Determine whether good posture or bad posture.
            # The threshold angles have been set based on intuition.
            if (ew_ang > 40 and ew_ang < 100) or (es_ang > 40 and es_ang < 100):
                cv2.putText(image, angle_text_string, (10, 30), font, 0.9, red, 2)
            
            else:
                cv2.putText(image, angle_text_string, (10, 30), font, 0.9, green, 2)

            if cv2.waitKey(1) == ord('m'):
                mov_count += 1

            cv2.putText(image, throw_count_string, (1000, 30), font, 0.9, red, 2)
            
        # show the final output
        out.write(image)
        outlet.push_sample([frameCounter])
        cv2.imshow('Movement Feedback', image)
        frameCounter += 1
        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print('Saved output video to:', filename)
