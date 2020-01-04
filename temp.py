import os

import cv2
import numpy as np

from read_warp_img import get_warp_img

def nothing(X):
    pass
def thresold_calibreation(img):
    cv2.namedWindow("thresold_calibration")
    cv2.createTrackbar("thresold", "thresold_calibration", 0, 255, nothing)
    while True:
        t =  cv2.getTrackbarPos("thresold", "thresold_calibration")
        matrix,thresold = cv2.threshold(gray,t,255,cv2.THRESH_BINARY_INV)
        cv2.imshow("thresold",thresold)
        if cv2.waitKey(1) & 0xFF == ord('q'):
                break
dir_path = os.path.dirname(os.path.realpath(__file__))+"/numpy_saved/1" # path of current directory
device = cv2.VideoCapture(1)
ret , img = device.read()
img =   cv2.resize(img,(800,800))
img_resize = (800,800)
img = get_warp_img(img,dir_path,img_resize)

img = cv2.resize(img,(800,800))
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
cv2.imshow("Image",gray)
cv2.waitKey(0)
thresold_calibreation(gray)
matrix,thresold = cv2.threshold(gray,9,255,cv2.THRESH_BINARY_INV)
cv2.imshow("thresold",thresold)
cv2.waitKey(0)

# kernel = np.ones((3,3),np.uint8)
# erosion = cv2.erode(thresold,kernel,iterations = 1)
# cv2.imshow("erosion",erosion)
# cv2.waitKey(0)

kernel = np.ones((3,3),np.uint8)
# closing = cv2.morphologyEx(thresold, cv2.MORPH_CLOSE, kernel,iterations=5)
# cv2.imshow("closing",closing)
# cv2.waitKey(0)

contours,_= cv2.findContours(thresold,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
required_contoures = []
required_contoures_mid_point = []
cnt_rectangle = []

for cnt in contours:
    area = cv2.contourArea(cnt)
    if(area > 500):
        print(area)
        (x, y, w, h) = cv2.boundingRect(cnt)
        required_contoures.append(cnt)
        required_contoures_mid_point.append([x+int(w/2),y+int(h/2)])
        cnt_rectangle.append([x,y,w,h])
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
    
cv2.imshow("final",img)
cv2.waitKey(0)
# HSV  = cv2.cvtColor(thresold,cv2.COLOR_BGR2HSV)
# board_color_calibration.color_calibration(HSV,"b")
# lower__b =  np.load(dir_path+"/chess_b_color_points.npz")['lower']
# upper__b = np.load(dir_path+"/chess_b_color_points.npz")['upper']
# cv2.waitKey(0)
cv2.destroyAllWindows()
