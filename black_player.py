import cv2
import numpy as np

def rectContains(rect,mid_point):
    logic = rect[0]<mid_point[0]<rect[2] and rect[1]<mid_point[1]<rect[3]
    return logic

def player_position(img , thresold_value,boxes):
    bool_position = np.zeros((8,8),dtype=int)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    matrix,thresold = cv2.threshold(gray,thresold_value,255,cv2.THRESH_BINARY_INV)
    contours,_= cv2.findContours(thresold,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    required_contoures = []
    required_contoures_mid_point = []
    cnt_rectangle = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if(area > 800):
            (x, y, w, h) = cv2.boundingRect(cnt)
            required_contoures.append(cnt)
            required_contoures_mid_point.append([x+int(w/2),y+int(h/2)])
            cnt_rectangle.append([x,y,w,h])
            # cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)

    flag = np.zeros((8,8),dtype=int)
    for i in range(8):
            for j in range(8):
                for mid_point in required_contoures_mid_point:
                    if(rectContains(boxes[i][j],mid_point)) and flag[i][j]==0:
                        bool_position[i][j] = 1
                        flag[i][j]=1
                        # cv2.rectangle(img,(boxes[i][j][0],boxes[i][j][1]),(boxes[i][j][2],boxes[i][j][3]),(255,255,0),2)
    
    # cv2.imshow("Game",img)
    # cv2.waitKey(0)
    return bool_position