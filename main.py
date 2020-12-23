import numpy as np
import cv2 as cv2
from collections import deque

blueLower = np.array([90, 50, 50])
blueUpper = np.array([120, 255, 255])

redLower = np.array([165,50,50])
redUpper = np.array([180,255,255])
pts = deque(maxlen =64)

yellowLower = np.array([20,100,100])
yellowUpper = np.array([35,255,255])
pts2 = deque(maxlen =64)
whiteLower = np.array([20,20,100])

##############################
# 함수 정의
###############################
def findBall(idx, hsv, lower, upper):
    global rPoint
    global yPoint
    global wPoint
    mask = cv2.inRange(hsv, lower, upper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    #가장 바깥쪽 컨투어에 대해 꼭지점 좌표만 반환
    contours, hierarchy = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contour = contours[0]

    # 모멘트 계산
    mmt = cv2.moments(contour)
    # m10/m00 m01/m00 중심점 계산
    x = int(mmt['m10'] / mmt['m00'])
    y = int(mmt['m01'] / mmt['m00'])

    # 빨간공
    if idx == '0':
        rPoint = (x, y)
        print("red[x: %d, y: %d]" % (x, y))
        cv2.circle(img, (x, y), 3, (0, 255, 0), -1)
        cv2.circle(img, (x, y), 13, (0, 255, 0), 2)
        pts.appendleft(rPoint)
        for i in range(1, len(pts)):
            if pts[i-1] is None or pts[i] is None:
                break
            cv2.line(img, pts[i-1], pts[i], (0,0,255), 2)

    elif idx == '1':
        yPoint = (x, y)
        print("yellow[x: %d, y: %d]" % (x, y))
        cv2.circle(img, (x, y), 3, (0, 255, 0), -1)
        cv2.circle(img, (x, y), 13, (0, 255, 0), 2)
        pts2.appendleft(yPoint)
        for i in range(1, len(pts2)):
            if pts2[i-1] is None or pts2[i] is None:
                break
            cv2.line(img, pts2[i-1], pts2[i], (0,255,255), 2)

##############################
# main
###############################
cap = cv2.VideoCapture("game.mp4")

while True:
    ret, img = cap.read()
    # 다음 프레임 읽기
    if ret:
        blur = cv2.GaussianBlur(img, (3, 3), 0)
        hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

        # #ROI 지정(당구대)
        maskZ = np.zeros_like(hsv)
        cv2.rectangle(maskZ, (148,111), (1129,601), (255,255,255), -1)
        cv2.rectangle(img, (148,111), (1129,601), (255,255,255), 5)
        hsv = cv2.bitwise_and(hsv, maskZ)
        findBall('0', hsv, redLower, redUpper)
        findBall('1', hsv, yellowLower, yellowUpper)

    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
    cv2.imshow("ROC", img)

cv2.waitKey(0);


