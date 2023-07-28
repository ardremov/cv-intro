import cv2
import numpy as np
import math
import matplotlib.pyplot as plt
from dt_apriltags import Detector

def get_array_x_int(elem):
    return elem[1]

def detect_lines(img, 
                 threshold1 = 50, 
                 threshold2 = 150, 
                 apertureSize = 3, 
                 minLineLength = 100, 
                 maxLineGap = 10):
    
    blur = cv2.GaussianBlur(img, (9, 9), 0)
    gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY) 
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

def draw_lines(img, lines, color = (0, 255,0)): # THANKS TOBY!
    temp_img = img
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(temp_img, (x1, y1), (x2, y2), color, 2)

    return temp_img

def draw_slopes(img, lines):
    for line in lines:
        slope = round(getSlope(line), 3)
        x1, y1, x2, y2 = line[0]
        cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        print(f'{slope = }')
        cv2.putText(img, f'{slope = }', (x1, y1), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 2)
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

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

# def merge_collinear_lines(lines: cv2.HoughLinesP):
#     if len(lines) < 4: # TODO: temporary magic number
#         return lines    
#     else:
#         (slopes, intercepts) = get_slopes_intercepts(lines)
#         new_lines = []
#         for i, line in enumerate(lines):
#             if i == 0:
#                 i = 1
#             if i == len(lines):
#                 i = len(lines - 1)
#             rel_tol = 0.1
#             if (math.isclose(slopes[i], slopes[i - 1], rel_tol=rel_tol) or math.isclose(slopes[i], slopes[i + 1], rel_tol=rel_tol)) and (math.isclose(intercepts[i], intercepts[i - 1], rel_tol=rel_tol) or math.isclose(intercepts[i], intercepts[i + 1], rel_tol=rel_tol)):
#                 lines.pop(i)
#         return merge_collinear_lines(lines)    

def detect_lanes(lines): # THANKS TOBY

    #MERGE LINES
    lanes = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        deltaY = y2 - y1
        if x2 == x1:
            slope = None
            xInt = x1
        else:
            slope = (y2 - y1)/(x2 - x1)
            if y2 == y1:
                xInt = None
            else:
                xInt = ((1080-y1)/slope) + x1
        if slope != None and xInt != None and deltaY != 0:
            lanes.append([slope, xInt, x1, y1, x2, y2])

    cleanedLines = []
    for line in lanes:
        canAdd = True
        for cleanedLine in cleanedLines:
            if abs(cleanedLine[0] - line[0]) < 0.1:
                canAdd = False

        if canAdd:
            cleanedLines.append(line)
    # DONE MERGING LINES
    #------
    # DELETE LINES NOT PART OF A LANE

    sorted_lines = cleanedLines
    sorted_lines.sort(key=get_array_x_int)
    if len(sorted_lines) > 2:  
        oneToZero = sorted_lines[1][1] - sorted_lines[0][1]
        twoToOne = sorted_lines[2][1] - sorted_lines[1][1]

        if(twoToOne < oneToZero):
            sorted_lines.pop(0)
        if len(sorted_lines) % 2 != 0:
            sorted_lines.pop(len(sorted_lines) - 1)
    # DONE DELETING LINES NOT IN LANE
    #------
    #PAIR LINES

    pairs = []
    if len(sorted_lines) >= 2:
        #pair 
        for i in range(0,len(sorted_lines)-1, 2):
            pairs.append([sorted_lines[i],sorted_lines[i+1]])
    #print(pairs)

    if len(pairs) > 0:
        if len(pairs) % 2 == 0: 
            center_lane = pairs[int((len(pairs))/2) -1]
        else:
            center_lane = pairs[int((len(pairs) + 1)/2) - 1]
        #print(center_lane)
    else:
        return []


    return center_lane

def draw_lanes(img, lanes): # THANKS TOBY!
    temp_img = img
    for line in lanes:
        x1 = line[2]#USING CONVENTION FROM DETECT_LANES
        y1 =line[3]
        x2 = line[4]
        y2 =line[5]
        cv2.line(temp_img, (x1, y1), (x2, y2), (0, 255, 0), 2)
    return temp_img