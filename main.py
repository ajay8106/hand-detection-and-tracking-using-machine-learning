import cv2
import numpy as np
import handtracking as htm
import time
import autopy

wCam, hCam = 640, 480

frameR = 100
framel = 100
smoothening =5
plocx,plocy = 0,0
clocx,clocy = 0,0

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

pTime = 0
cTime = 0

detector = htm.handDetector(maxHands=1)
wScr, hScr = autopy.screen.size()
#print(wScr, hScr)

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox =  detector.findPosition(img)

    if len(lmList)!= 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        #print(x1, y1, x2, y2)

        finges = detector.fingersUp()
        #print(finges)
        cv2.rectangle(img, (frameR, framel), (wCam - frameR, hCam - framel), (255, 0, 255), 2)
        if finges[1]==1 and finges[2]==0:

            x3 = np.interp(x1, (frameR,wCam-frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, hCam-frameR), (0, hScr))

            clocx = plocx+(x3 - plocx)/smoothening
            clocy = plocy+(y3 - plocy)/smoothening

            autopy.mouse.move(wScr-clocx, clocy)
            cv2.circle(img,(x1, y1), 10, (0,0,255),cv2.FILLED)
            plocx,plocy = clocx,clocy

        if finges[1]==1 and finges[2]==1:
            length, img,lineInfo =detector.findDistance(8,12,img)
            print(length)
            if length <40:
                cv2.circle(img,(lineInfo[4], lineInfo[5]), 10, (0,255,0),cv2.FILLED)
                autopy.mouse.click()
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime=cTime
    cv2.putText(img,str(int(fps)),(20,50),cv2.FONT_HERSHEY_PLAIN,3 ,(255, 0,0),3)
    cv2.imshow("Image", img)
    cv2.waitKey(1)


