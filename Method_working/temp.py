import cv2
from matplotlib import pyplot as plt 

def nothing(X):
    pass

def thresold_calibreation(img):
    cv2.namedWindow("thresold_calibration")
    cv2.createTrackbar("thresold", "thresold_calibration", 0, 255, nothing)
    while True:
        t =  cv2.getTrackbarPos("thresold", "thresold_calibration")
        matrix,thresold = cv2.threshold(img,t,255,cv2.THRESH_BINARY)
        cv2.imshow("thresold",thresold)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            return t

image1 = cv2.imread('Method_working\Images/2.jpg')
image2 = cv2.imread('Method_working\Images/3.jpg')

image1_gray = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
image2_gray = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

diff = cv2.absdiff(image1,image2)

cv2.imshow("diff", diff)
cv2.waitKey(0)

diff = cv2.resize(diff,(800,800))
cv2.imshow("diff",diff)
cv2.imwrite("Method_working/Images/Difference_image.jpg",diff)

diff_gray = cv2.cvtColor(diff,cv2.COLOR_BGR2GRAY)
cv2.imshow("diff_gray", diff_gray)
cv2.imwrite("Method_working/Images/Difference_GrayScale_image.jpg",diff_gray)
cv2.waitKey(0)

value = thresold_calibreation(diff_gray)

matrix,thresold = cv2.threshold(diff_gray,value,255,cv2.THRESH_BINARY)
cv2.imshow("thresold",thresold)

cnts,_ = cv2.findContours(thresold, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
print(len(cnts))

for c in cnts:
    area = cv2.contourArea(c)
    if area> 500:
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(diff, (x, y), (x + w, y + h), (0, 0, 255), 2)

cv2.imshow("diff", diff)
cv2.imwrite("Method_working/Images/show_Contours.jpg",diff)
cv2.waitKey(0)


result1 =  cv2.bitwise_and(image1,image1,mask = thresold)
cv2.imshow("result",result1)
cv2.imwrite("Method_working/Images/Result_image.jpg",result1)

cv2.waitKey(0)
cv2.destroyAllWindows()