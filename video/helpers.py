import math as m
import numpy as np
from pylsl import StreamInfo, StreamOutlet
import os

# define function to determine offset distance between two points
def findDistance(x1, x2, y1, y2):
    dist = m.sqrt((x2-x1)**2 + (y2-y1)**2)
    return dist

# Angle / inclination of landmark lines
def findAngle(x1, y1, x2, y2):
    theta = m.acos((y2-y1)*(-y1) / (m.sqrt((x2-x1)**2 + (y2-y1)**2)*y1))
    degree = int(180/m.pi)*theta
    return degree

# finding an angle between three points
def findTotalAngle(x1, y1, x2, y2, x3, y3):
    # Calculate vectors between the points
    vector1 = np.array([x1 - x2, y1 - y2])
    vector2 = np.array([x3 - x2, y3 - y2])

    # Calculate the dot product
    dot_product = np.dot(vector1, vector2)

    # Calculate the magnitudes of the vectors
    magnitude1 = np.linalg.norm(vector1)
    magnitude2 = np.linalg.norm(vector2)

    # Calculate the cosine of the angle
    cosine_angle = dot_product / (magnitude1 * magnitude2)

    # Calculate the angle in radians
    angle_rad = np.arccos(cosine_angle)

    # Convert the angle to degrees
    angle_deg = np.degrees(angle_rad)

    return angle_deg

#outlet to create lsl stream
def createOutlet(index, filename):
    streamName = 'FrameMarker'+str(index+1)
    info = StreamInfo(name=streamName,
                      type='videostream',
                      channel_format='float32', # type: ignore
                      channel_count=4,
                      source_id='landmarks')

    dir_file = os.path.dirname(filename)
    if not os.path.exists(dir_file):
        print('Creating folder', dir_file)
        os.makedirs(dir_file)
    videoFile = filename
    info.desc().append_child_value("videoFile", videoFile)
    return StreamOutlet(info)