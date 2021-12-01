import cv2
import mediapipe as mp
from colorama import Fore, Style


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
        :param count = if true return the number of open fingers
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
            :param img an opencv image
            :param draw:bool if landmarks are drawn or not
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

        :param img = ! Must its an image from openCV ,
        :param handNo = 0 if you are tracking more than one hands
        :param draw = default : True if you neeed to draw points on screen
        '''
        lmList = []
        boundaryBox = []
        x_points,y_points = [],[]
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]

            for Id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                x_points.append(cx)
                y_points.append(cy)
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
        if len(x_points) > 0:
            x_min,x_max = min(x_points), max(x_points)
            y_min,y_max = min(y_points), max(y_points)
            width,height = x_max - x_min, y_max- y_min
            boundaryBox.append(x_min)
            boundaryBox.append(y_min)
            boundaryBox.append(width)
            boundaryBox.append(height)
            if draw:
                cv2.rectangle(img, (x_min - 20, y_min - 20),
                (x_min + width + 20, y_min + height + 20),(0, 255, 0), 2)
        return lmList,boundaryBox

    def findFinger(self,img,finger,handNo = 0,draw = True,drawHandPoints = False,drawHandNumbers = False,on = None):
        '''
            : returns the x,y coordinates of the given finger 

            :param img = openCV img
            :param finger = the finger you want position of
            :param handNo = 0 if you tracking more than one hand
            :param on = openCV img the surface on which you whish to draw
        '''
        # findPosition also returns boundary box
        list, _ = self.findPosition(img,handNo,drawHandPoints,drawHandNumbers)
        finger += 1
        finger *= 4
        if len(list) > 0:
            if draw and on is None:
                cv2.circle(img, (list[finger][1], list[finger][2]), 10, (255, 0, 255), 3)
            else:
                cv2.circle(on, (list[finger][1], list[finger][2]), 5, (196, 144, 228)[::-1], 3)
            return  [list[finger][1], list[finger][2]]
    
    def get_finger_tips(self, finger_pnts, no_of_fingers=5, draw=False, img=None):
        '''
            :returns an array containing cords of finger tips 
            :param finger_pnts the lmList of fingers
            :param no_of_fingers the no of fingers you want to track 
            :param draw:bool if you want to draw circles around the fingers or not
            :param img:OpenCv image the image you want to draw on
        '''
        finger_idx = 1
        finger_tips = []

        if len(finger_pnts) == 0:
            return None

        for _ in range(no_of_fingers):
            func, x, y = finger_pnts[finger_idx*4]
            finger_tips.append((x, y))
            finger_idx+=1
        if draw :
            if img is None:
                print(f"{Fore.RED} Image is None can't draw on it! {Style.RESET_ALL}")
                return finger_tips
            for finger in finger_tips:
                    cv2.circle(img, (finger[0], finger[1]), 10, (0, 0, 255), 3)

        return finger_tips


def main():
    detector = HandDetector(detectionCon=0.8)
    # 0 if you want to use your web cam 1 if you use external webcam ex:phone
    cap = cv2.VideoCapture(0)
    while True:
        success, img = cap.read()
        img = detector.findHands(img,draw=True)

        finger_pos = detector.findFinger(img,finger = 1,draw=True,drawHandPoints = False) 
        
        print(f'{Fore.GREEN}{finger_pos}')

        cv2.imshow("Image", img)
        cv2.waitKey(1)

if __name__ == '__main__':
    main()