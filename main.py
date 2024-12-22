import cv2
from cvzone.HandTrackingModule import HandDetector
import cvzone

cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

cx, cy, w, h = 50, 50, 100, 100


class DragRect:
    def __init__(self,posCenter,size=[100,100]):
        self.posCenter=posCenter
        self.size=size
    def update(self,cursor):
        cx, cy = self.posCenter
        w, h = self.size
        if cx-w//2<cursor[0]<cx+w//2 and cy-h//2<cursor[1]<cy+h//2:
                colorP = 0,255,0
                self.posCenter = cursor

detector = HandDetector(detectionCon=1)
# color
colorP = (255,0,255)
colorB = (255,0,0)
colorC = (0,255,255)

rectList = []
for x in range(8):
    rectList.append(DragRect([x*150+100,100]))
while True:
    success, img = cap.read()
    img = cv2.flip(img,1)
    img = detector.findHands(img)
    # bounding Box = bbox
    lmList, bbox= detector.findPosition(img)

    if lmList:
        l,_,_ = detector.findDistance(8,12,img,draw=False)
        print(l)
        if l<40:
            cursor = lmList[8]
            # calling part
            for rect in rectList:
                rect.update(cursor)
    
    # to draw rectangle
    for rect in rectList:
        cx, cy = rect.posCenter
        w, h = rect.size
        cv2.rectangle(img,(cx-w//2,cy-h//2),(cx+w//2,cy+h//2),colorP,cv2.FILLED)
        cvzone.cornerRect(img,(cx-w//2,cy-h//2,w,h),20,rt=0)
    cv2.rectangle(img,(cx-w//2,cy-h//2),(cx+w//2,cy+h//2),colorC,cv2.FILLED)
    cvzone.cornerRect(img,(cx-w//2,cy-h//2,w,h),20,rt=0)

    cv2.imshow('Image',img)
    cv2.waitKey(1)
    