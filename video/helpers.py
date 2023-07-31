import math as m
import numpy as np
import os
from pylsl import StreamInfo, StreamOutlet

# Colors (in BGR)
blue = (255, 127, 0)
red = (50, 50, 255)
green = (0, 205, 0)
yellow = (0, 255, 255)

def startProgram():
    print("Hello, let's improve some movements! :) \n\n")

    # userID specification
    userID = input("What is the user ID (the video output will be saved with this filename):")

    # study specification
    group = input("\n Which group is this user a part of? (landmarks (l) or raw (r))")
    if group == "l":
        group = "Landmarks"
    elif group == 'r':
        group = "Raw Video"

    # movement specification
    move = input("\n Is the user left-handed or right-handed? (l or r)")
    if move == "l":
        move = "throwL"
    elif move == 'r':
        move = "throwR"
    return userID, group, move

# outlet to create lsl stream
def createOutlet(index, filename):
    streamName = "FrameMarker" + str(index + 1)
    info = StreamInfo(
        name=streamName,
        type="videostream", nominal_srate=30,
        channel_format="float32",  # type: ignore
        channel_count=4,
        source_id="landmarks",
    )

    dir_file = os.path.dirname(filename)
    if not os.path.exists(dir_file):
        print("Creating folder", dir_file)
        os.makedirs(dir_file)
    videoFile = filename
    info.desc().append_child_value("videoFile", videoFile)
    return StreamOutlet(info)

def reactToKeyPress(key, markerOutlet, relevance, testing):  
    if key == ord("a"):
        markerOutlet.push_sample(["START_TESTING"])
        print('started')
        testing = "started"

    if key == ord("s"):
        markerOutlet.push_sample(["START_THROW"])
        print('started throw')
        relevance = True

    if key == ord("d"):
        markerOutlet.push_sample(["STOP_THROW"])
        print('finished throw')
        relevance = False

    if key == ord("f"):
        markerOutlet.push_sample(["STOP_TESTING"])
        print('stopped')
        testing = "done"
        
    return relevance, testing
        
        
# define function to determine offset distance between two points
def findDistance(x1, x2, y1, y2):
    dist = m.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return dist


# Angle / inclination of landmark lines
def findAngle(x1, y1, x2, y2):
    theta = m.acos((y2 - y1) * (-y1) / (m.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) * y1))
    degree = int(180 / m.pi) * theta
    return degree


# finding an angle between three points
def findTotalAngle(x1, y1, x2, y2, x3, y3):
    # Calculate vectors between the points
    v1 = np.array([x1 - x2, y1 - y2])
    v2 = np.array([x3 - x2, y3 - y2])

    # Calculate the dot product
    dot_product = np.dot(v1, v2)

    # Calculate the magnitudes of the vectors
    mag1 = np.linalg.norm(v1)
    mag2 = np.linalg.norm(v2)

    # Calculate the cosine of the angle
    cosine_angle = dot_product / (mag1 * mag2)

    # Calculate the angle in radians
    angle_rad = np.arccos(cosine_angle)

    # Convert the angle to degrees
    angle_deg = np.degrees(angle_rad)

    return angle_deg


def calcLandmarks(
    move, lm, lmPose, width, height, cv2, group, flipped
):
    # if user is left handed, now that the video is flipped, we need to select the right side landmarks
    if move == 'throwL':
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

        # Calculate angles
        # elbow-shoulder angulation
        es_ang = findAngle(r_elb_x, r_elb_y, r_shldr_x, r_shldr_y)
        # elbow-wrist angulation
        ew_ang = findAngle(r_elb_x, r_elb_y, r_wrs_x, r_wrs_y)
        # full angle (from sholder to wrist)
        t_ang = findTotalAngle(
            r_shldr_x, r_shldr_y, r_elb_x, r_elb_y, r_wrs_x, r_wrs_y
        )

        if group == "Landmarks":
            # Create landmarks nodes
            cv2.circle(flipped, (r_shldr_x, r_shldr_y), 7, yellow, -1)
            cv2.circle(flipped, (r_elb_x, r_elb_y), 7, yellow, -1)
            cv2.circle(flipped, (r_wrs_x, r_wrs_y), 7, yellow, -1)

            # Join movement landmarks
            cv2.line(flipped, (r_shldr_x, r_shldr_y), (r_elb_x, r_elb_y), green, 4)
            cv2.line(flipped, (r_elb_x, r_elb_y), (r_wrs_x, r_wrs_y), green, 4)

            # Create movement conditions
            if (ew_ang > 30) and (ew_ang < 170):
                # Join movement landmarks (movement to be improved).
                cv2.line(flipped, (r_elb_x, r_elb_y), (r_wrs_x, r_wrs_y), red, 4)
            if (es_ang > 30) and (es_ang < 155):
                # Join movement landmarks (movement to be improved).
                cv2.line(flipped, (r_shldr_x, r_shldr_y), (r_elb_x, r_elb_y), red, 4)

    # if user is right handed, now that the video is flipped, we need to select the left side landmarks
    if move == 'throwR':
        # 11 - left shoulder
        l_shldr_x = int(lm.landmark[lmPose.LEFT_SHOULDER].x * width)
        l_shldr_y = int(lm.landmark[lmPose.LEFT_SHOULDER].y * height)
        # 12 - right shoulder
        r_shldr_x = int(lm.landmark[lmPose.RIGHT_SHOULDER].x * width)
        r_shldr_y = int(lm.landmark[lmPose.RIGHT_SHOULDER].y * height)
        # 14 - left elbow
        l_elb_x = int(lm.landmark[lmPose.LEFT_ELBOW].x * width)
        l_elb_y = int(lm.landmark[lmPose.LEFT_ELBOW].y * height)
        # 16 - left wrist
        l_wrs_x = int(lm.landmark[lmPose.LEFT_WRIST].x * width)
        l_wrs_y = int(lm.landmark[lmPose.LEFT_WRIST].y * height)

        # Calculate angles
        # elbow-shoulder angulation
        es_ang = findAngle(l_elb_x, l_elb_y, l_shldr_x, l_shldr_y)
        # elbow-wrist angulation
        ew_ang = findAngle(l_elb_x, l_elb_y, l_wrs_x, l_wrs_y)
        # full angle (from sholder to wrist)
        t_ang = findTotalAngle(
            l_shldr_x, l_shldr_y, l_elb_x, l_elb_y, l_wrs_x, l_wrs_y
        )

        if group == "Landmarks":
            # Create landmarks nodes
            cv2.circle(flipped, (l_shldr_x, l_shldr_y), 7, yellow, -1)
            cv2.circle(flipped, (l_elb_x, l_elb_y), 7, yellow, -1)
            cv2.circle(flipped, (l_wrs_x, l_wrs_y), 7, yellow, -1)

            # Join movement landmarks
            cv2.line(flipped, (l_shldr_x, l_shldr_y), (l_elb_x, l_elb_y), green, 4)
            cv2.line(flipped, (l_elb_x, l_elb_y), (l_wrs_x, l_wrs_y), green, 4)

            # Create movement conditions
            if (ew_ang > 30) and (ew_ang < 170):
                # Join movement landmarks (movement to be improved).
                cv2.line(flipped, (l_elb_x, l_elb_y), (l_wrs_x, l_wrs_y), red, 4)
            if (es_ang > 30) and (es_ang < 155):
                # Join movement landmarks (movement to be improved).
                cv2.line(flipped, (l_shldr_x, l_shldr_y), (l_elb_x, l_elb_y), red, 4)
                
    return es_ang, ew_ang, t_ang #type:ignore
