# program that analyses movement patterns as a direct real-time feedback approach to sport/movement improvement
import cv2
import mediapipe as mp
from helpers import *
from recorder import relevance

#Start of program
print("Hello, let's improve some movements! :) \n\n")

#userID specification
userID = input('What is the user ID(the video output will be saved with this filename):')

#study specification 
groupLandmarks = 'Landmarks'
groupRawVideo = 'Raw Video'
group = input('Which group is this user a part of? (landmarks (l) or raw (r))')
if group == 'l':
    group = 'Landmarks'
else:
    group = 'Raw Video'

# movement specification
rightHand = 'throwR'
leftHand = 'throwL'
hand = input('Is the user left-handed or right-handed? (l or r)')
if hand == 'l':
    move = leftHand
else:
    move = rightHand

# font
font = cv2.FONT_HERSHEY_SIMPLEX

# Colors (in BGR)
blue = (255, 127, 0)
red = (50, 50, 255)
green = (0, 205, 0)
yellow = (0, 255, 255)

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
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    filename = os.path.join(dir_out, userID + '.mov')
    out = cv2.VideoWriter(filename, fourcc, (fps/2), (int(width), int(height)))
    frameCounter = 1
    outlet = createOutlet(dev, filename)

    # initialize Pose estimator
    mp_drawing = mp.solutions.drawing_utils # type: ignore
    mp_pose = mp.solutions.pose # type: ignore

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

        # Fliping the image as said in question
        flipped = cv2.flip(image, 1)

        # process the RGB frame to get the result
        keypoints = pose.process(flipped)

        # Convert the image back to BGR.
        flipped = cv2.cvtColor(flipped, cv2.COLOR_RGB2BGR)

        # Use lm and lmPose as representative of the following methods.
        lm = keypoints.pose_landmarks
        lmPose = mp_pose.PoseLandmark

        # give value to angles if landmark is not found
        es_ang = 0
        ew_ang = 0
        total_ang = 0

        if lm is not None:

            # if user is left handed, now that the video is flipped, we need to select the right side landmarks
            if move == leftHand:
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

                # Calculate angles
                # elbow-shoulder angulation
                es_ang = findAngle(r_elb_x, r_elb_y, r_shldr_x, r_shldr_y)
                # elbow-wrist angulation
                ew_ang = findAngle(r_elb_x, r_elb_y, r_wrs_x, r_wrs_y)
                #full angle (from sholder to wrist)
                total_ang = findTotalAngle(r_shldr_x, r_shldr_y, r_elb_x, r_elb_y, r_wrs_x, r_wrs_y)

                if group == 'Landmarks':
                    # Create landmarks nodes
                    cv2.circle(flipped, (r_shldr_x, r_shldr_y), 7, yellow, -1)
                    cv2.circle(flipped, (r_elb_x, r_elb_y), 7, yellow, -1)
                    cv2.circle(flipped, (r_wrs_x, r_wrs_y), 7, yellow, -1)

                    # Join movement landmarks
                    cv2.line(flipped, (r_shldr_x, r_shldr_y),
                            (r_elb_x, r_elb_y), green, 4)
                    cv2.line(flipped, (r_elb_x, r_elb_y),
                            (r_wrs_x, r_wrs_y), green, 4)

                    # Create movement conditions
                    if (ew_ang > 30) and (ew_ang < 170):
                        # Join movement landmarks (movement to be improved).
                        cv2.line(flipped, (r_elb_x, r_elb_y),
                                (r_wrs_x, r_wrs_y), red, 4)
                    if (es_ang > 30) and (es_ang < 155):
                        # Join movement landmarks (movement to be improved).
                        cv2.line(flipped, (r_shldr_x, r_shldr_y),
                                (r_elb_x, r_elb_y), red, 4)

            # if user is right handed, now that the video is flipped, we need to select the left side landmarks
            if move == rightHand:
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
                # 24 - left hip
                l_hip_x = int(lm.landmark[lmPose.LEFT_HIP].x * width)
                l_hip_y = int(lm.landmark[lmPose.LEFT_HIP].y * height)

                # Calculate angles
                # elbow-shoulder angulation
                es_ang = findAngle(l_elb_x, l_elb_y, l_shldr_x, l_shldr_y)
                # elbow-wrist angulation
                ew_ang = findAngle(l_elb_x, l_elb_y, l_wrs_x, l_wrs_y)
                #full angle (from sholder to wrist)
                total_ang = findTotalAngle(l_shldr_x, l_shldr_y, l_elb_x, l_elb_y, l_wrs_x, l_wrs_y)

                if group == 'Landmarks':
                    # Create landmarks nodes
                    cv2.circle(flipped, (l_shldr_x, l_shldr_y), 7, yellow, -1)
                    cv2.circle(flipped, (l_elb_x, l_elb_y), 7, yellow, -1)
                    cv2.circle(flipped, (l_wrs_x, l_wrs_y), 7, yellow, -1)

                    # Join movement landmarks
                    cv2.line(flipped, (l_shldr_x, l_shldr_y),
                            (l_elb_x, l_elb_y), green, 4)
                    cv2.line(flipped, (l_elb_x, l_elb_y),
                            (l_wrs_x, l_wrs_y), green, 4)

                    # Create movement conditions
                    if (ew_ang > 30) and (ew_ang < 170):
                        # Join movement landmarks (movement to be improved).
                        cv2.line(flipped, (l_elb_x, l_elb_y),
                                (l_wrs_x, l_wrs_y), red, 4)
                    if (es_ang > 30) and (es_ang < 155):
                        # Join movement landmarks (movement to be improved).
                        cv2.line(flipped, (l_shldr_x, l_shldr_y),
                                (l_elb_x, l_elb_y), red, 4)

        # show the final output
        #TODO: can I get relevance from recorder?
        if relevance:
            out.write(flipped)
            outlet.push_sample([frameCounter, es_ang, ew_ang, total_ang])
        cv2.imshow('Movement Feedback', flipped)
        frameCounter += 1
        if cv2.waitKey(1) == ord('q'):
            break
    
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print('Saved output video to:', filename)
