import mediapipe as mp
import cv2
import time

##address="https://192.168.0.109:8080/video"
##cap.open(address)

class handDetector():
    def __init__(self, mode=False, maxHands=1, complexity = 1, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.complexity = complexity
        self.detectionCon = detectionCon
        self.trackCon = trackCon


        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.complexity,
                                        self.detectionCon, self.trackCon,)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self,img,draw=True):
        imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results=self.hands.process(imgRGB)
        
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img , handLms , self.mpHands.HAND_CONNECTIONS)
##                for id,lm in enumerate(handLms.landmark):
##
##                    h,w,c=img.shape
##                    cx,cy=int(lm.x*w),int(lm.y*h)
##
##                    if id in [4,8,12,16,20]:
##                        cv2.circle(img,(cx,cy),10,(0,255,255),-1)
        return img

    def findPosition(self,img ,handNo=0,draw=True):
        
        lmList=[]
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]

            for id,lm in enumerate(myHand.landmark):
                h,w,c=img.shape
                cx,cy=int(lm.x*w),int(lm.y*h)
##                print(id,cx,cy)
                lmList.append([id,cx,cy])

                if draw:
                    cv2.circle(img,(cx,cy),5,(0,255,255),-1)

        return lmList

            
                

##    khkvg    

def main():
    cap=cv2.VideoCapture(0)

    pTime=0
    cTime=0
    detector=handDetector()

    while True:
        success, img =cap.read()
        img=detector.findHands(img)

        lmList=detector.findPosition(img)
##        if len(lmList)!=0:
##            print(lmList[4])

        cTime=time.time()
        fps=1/(cTime-pTime)
        pTime=cTime

        cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(0,255,0),3)

        ## cv2.imshow('image',img)
        cv2.imshow('image',img)
        cv2.waitKey(1)



if __name__=="__main__":
    main()






    
