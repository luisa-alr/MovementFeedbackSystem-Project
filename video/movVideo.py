# program that analyses movement patterns as a direct real-time feedback approach to sport/movement improvement
import cv2
import mediapipe as mp
from helpers import *
from pylsl import StreamInfo, StreamOutlet
import pandas as pd

# Start of program
userID, group, move = startProgram()

# font
font = cv2.FONT_HERSHEY_SIMPLEX


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
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    filename = os.path.join(dir_out, userID + ".mov")
    out = cv2.VideoWriter(filename, fourcc, (fps / 2), (int(width), int(height)))
    frameCounter = 1
    relevance = False
    testing = 'not started'
    data = []
    outlet = createOutlet(dev, filename)

    markerInfo = StreamInfo("ThrowMarkerStream", "Markers", 1, 0, "string", "markers")  # type: ignore
    markerOutlet = StreamOutlet(markerInfo)

    # initialize Pose estimator
    mp_drawing = mp.solutions.drawing_utils  # type: ignore
    mp_pose = mp.solutions.pose  # type: ignore

    pose = mp_pose.Pose(min_detection_confidence=0.9, min_tracking_confidence=0.9)

    while True:
        key = cv2.waitKey(1)
        if key == ord("q"):
            break
        relevance, testing = reactToKeyPress(key, markerOutlet, relevance, testing)


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
        es_ang = -1
        ew_ang = -1
        t_ang = -1

        if lm is not None:
            es_ang, ew_ang, t_ang = calcLandmarks(move, lm, lmPose, width, height, cv2, group, flipped)
            
            if relevance == True:
                data.append([frameCounter, es_ang, ew_ang, t_ang])
            
            if testing == 'done':
                df_data = pd.DataFrame(data, columns=['frame', 'shoulder angle', 'elbow angle', 'total angle'])
                df_data.to_csv('recorderAngles.csv', sep=',', encoding='utf-8')

        out.write(flipped)
        outlet.push_sample([frameCounter, es_ang, ew_ang, t_ang])
        cv2.imshow("Movement Feedback", flipped)
        frameCounter += 1

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print("Saved output video to:", filename)
