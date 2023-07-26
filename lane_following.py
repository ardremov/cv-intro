import cv2
import numpy as np
import math
import matplotlib.pyplot as plt
from dt_apriltags import Detector
import lane_detection

def get_lane_center(lanes, width = 1566):
    center_lane = int(lanes[len(lanes) / 2])
    (slope, intercept) = lane_detection.get_slopes_intercepts(center_lane)
    return (slope, intercept)
        
def recommend_direction(center, slope, width = 1566):
    if center < width / 2:
        return 'left'
    elif center == width / 2:
        return 'forward'
    else:
        return 'right'

