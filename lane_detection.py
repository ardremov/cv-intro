import cv2
import numpy as np
import math
import matplotlib.pyplot as plt
from dt_apriltags import Detector

def detect_lines(img, 
                 threshold1 = 50, 
                 threshold2 = 150, 
                 apertureSize = 3, 
                 minLineLength = 100, 
                 maxLineGap = 10):
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
    edges = cv2.Canny(gray, threshold1, threshold2, apertureSize) 
    lines = cv2.HoughLinesP(
                    edges,
                    1, 
                    np.pi/180, 
                    100, 
                    minLineLength=minLineLength, 
                    maxLineGap=maxLineGap, 
            ) 
    
    return lines

def draw_lines(img, lines, color = (0, 255, 0)):
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(img, (x1, y1), (x2, y2), color, 10)
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

def draw_slopes(img, lines):
    for line in lines:
        slope = round(getSlope(line), 3)
        x1, y1, x2, y2 = line[0]
        cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        print(f'{slope = }')
        cv2.putText(img, f'{slope = }', (x1, y1), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 2)
    return cv2.cvtColor(img, cv2.BGR2RGB)

def getSlope(line: cv2.HoughLinesP) -> float:
    x1, y1, x2, y2 = line[0]
    if x1 == x2:
        slope = None
    else:
        slope = round((y2 - y1) / (x2 - x1), 4) 
    return slope

def getXInt(line: cv2.HoughLinesP) -> float:
        x1, y1, x2, y2 = line[0]
        if y1 == y2:
            intercept = None
        else:
            slope = getSlope(line)
            intercept = (-y1 + (x1 * slope)) / slope
        return (intercept, 0)

def get_slopes_intercepts(lines: cv2.HoughLinesP):
    slopes = []
    intercepts = []
    for line in lines:
        slopes.append(getSlope(line))
        intercepts.append(getXInt(line))
    return (slopes, intercepts)

def detect_lanes(lines: cv2.HoughLinesP):
    lanes = []
    
    (slopes, intercept_points) = get_slopes_intercepts(lines)
    x_intercepts = [point[0] for point in intercept_points]
    dict  = dict(zip(x_intercepts, lines))

    return lanes

def draw_lanes(img: cv2.imread, lanes):
    
    pass