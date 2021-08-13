import cv2
import mediapipe as mp
from colorama import Fore


class HandDetector:
    def __init__(self, mode=False, maxHands=1, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
        self.mode, self.maxHands, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def countFingers(self,lmList,count= False):
        ''' 
        :returns a list containing which fingers are open
        :param lmList ! List containing positon of fingers
        :param count = if true return return the number of open fingers
        '''
        fingers = []
        if len(lmList) != 0:

            if lmList[4][1] > lmList[3][1]:
                fingers.append(1)
            else:
                fingers.append(0)
            for n in range(2, 6):
                if lmList[4 * n][2] < lmList[4 * n - 1][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            if count == True:
                return sum(fingers)

        return fingers
    
    def findHands(self, img, draw:bool=False):
        '''
            :return the image of the hand
        '''
        imgRBG = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRBG)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(
                        img, handLms, self.mpHands.HAND_CONNECTIONS)

        return img

    def findPosition(self, img, handNo=0, draw:bool=True,showNumbers = True):
        '''
        :returns  an array containing the landmark List of points of hands with 0 having id , 1,2 respectively have x,y

        :parameter img = ! Must its an image from openCV ,
        :parameter handNo = 0 if you are tracking more than one hands
        :parameter draw = default : True if you neeed to draw points on screen
        '''
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]

            for Id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])

                if draw:
                    # to fill the dot
                    # cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)
                    # to stroke a circle 
                    cv2.circle(img, (cx, cy), 10, (255, 0, 255), 2)

                if showNumbers:
                    fontScale = 0.6
                    # here len(lmList)-1 is the text
                    cv2.putText(img,str(len(lmList)-1), (cx,cy), cv2.FONT_HERSHEY_SIMPLEX,fontScale, color = (0,0,0), thickness = 3)

        return lmList or None

    def findFinger(self,img,finger,handNo = 0,draw = True,drawHandPoints = False,drawHandNumbers = False):
        '''
            : returns the x,y coordinates of the given finger 

            :param img = openCV img
            :param finger = the finger you want position of
            :param handNo = 0 if you tracking more than one hand
        '''
        list = self.findPosition(img,handNo,drawHandPoints,drawHandNumbers)
        finger += 1
        finger *= 4
        if list != None:
            if draw:
                cv2.circle(img, (list[finger][1], list[finger][2]), 10, (255, 0, 255), 3)
            return  (list[finger][1], list[finger][2])


def main():
    detector = HandDetector(detectionCon=0.8)
    # 0 if you want to use your web cam 1 if you use external webcam ex:phone
    cap = cv2.VideoCapture(1)
    while True:
        success, img = cap.read()
        img = detector.findHands(img,draw=True)
        finger_pos = detector.findFinger(img,finger = 1,draw=False,drawHandPoints = False) 
        
        print(f'{Fore.GREEN}{finger_pos}')

        cv2.imshow("Image", img)
        cv2.waitKey(1)

if __name__ == '__main__':
    main()
