import cv2
import numpy as np
import os 
ix,iy = -1,-1
img = 0 

###################################################################################
## Code For Detect corner points 
###################################################################################

def draw_circle(event,x,y,flags,param):
    global ix,iy
    if event == cv2.EVENT_LBUTTONDBLCLK:
        cv2.circle(img,(x,y),2,(255,0,0),-1)
        ix,iy = x,y

def get_points(image,numOfPoints):
    global img 
    img = image.copy()
    img = cv2.resize(img,(800,800))
    width, height = image.shape[:2]
    cv2.namedWindow("image")
    cv2.setMouseCallback("image",draw_circle)
    points = []
    print("Press a for add point : ")
    while len(points) != numOfPoints:
        cv2.imshow("image",img)
        k = cv2.waitKey(1)
        if k == ord('a'):
            points.append([int(ix),int(iy)])
            cv2.circle(img,(ix,iy),3,(0,0,255),-1)
    cv2.destroyAllWindows()
    return list(points)
