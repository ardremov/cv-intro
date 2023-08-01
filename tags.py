from dt_apriltags import Detector
import matplotlib.pyplot as plt
import numpy as np
import cv2

cameraMatrix = np.array([ 1060.71, 0, 960, 0, 1060.71, 540, 0, 0, 1]).reshape((3,3))
tag_size = 0.1
camera_params = (cameraMatrix[0,0], cameraMatrix[1,1], cameraMatrix[0,2], cameraMatrix[1,2])

def get_tags(img):
    at_detector = Detector(families='tag36h11',
                       nthreads=1,
                       quad_decimate=1.0,
                       quad_sigma=0.0,
                       refine_edges=1,
                       decode_sharpening=0.25,
                       debug=0)

    tags = at_detector.detect(img, True, camera_params, tag_size)
    return tags

def get_positions(tags):
    ret = []
    for tag in tags:
        ret.append([tag.center[0], tag.center[1], tag.tag_id])
    return ret

def error_relative_to_center(centers, width, height):
    ret = []
    xcenter = height / 2
    ycenter = width / 2
    print(xcenter, ycenter)
    for center in centers:
        ret.append([center[0] - xcenter, ycenter - center[1] ,center[2]])
    return ret

def draw_tags(tags, img):
    ret_img = img

    for tag in tags:
        
        for idx in range(len(tag.corners)):
            cv2.line(ret_img, tuple(tag.corners[idx - 1, :].astype(int)), tuple(tag.corners[idx, :].astype(int)), (0, 255, 0), thickness = 5)

        cv2.putText(ret_img, str(tag.tag_id),
                    org = (tag.corners[0, 0].astype(int) + 10, tag.corners[0, 1].astype(int) + 10),
                    fontFace = cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale = 0.8,
                    color = (255, 0, 0),
                    thickness = 5
                    )
    
    return ret_img