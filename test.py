import mouse
from colorama import Fore,Style
import tkinter as tk
from handTracking import HandDetector
import cv2

root = tk.Tk()

# 1280 x 800

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# print(f'{Fore.MAGENTA}{screen_width}  {Fore.LIGHTYELLOW_EX}{screen_height}') # Magneta == Purple

# print(Style.RESET_ALL)


detector = HandDetector(detectionCon=0.8)
# 0 if you want to use your web cam 1 if you use external webcam ex:phone
cap = cv2.VideoCapture(1)
success, img = cap.read()

img = detector.findHands(img,draw=True)
imageDimensions = img.shape
imageDimensions = imageDimensions[0],imageDimensions[1]
correctionFactor_x  = screen_width / imageDimensions[0]
correctionFactor_y  = screen_height / imageDimensions[1]

previous_mouse_pos_x ,previous_mouse_pos_y = mouse.get_position()
while True:
    success, img = cap.read()

    img = detector.findHands(img,draw=True)
    finger_pos = detector.findFinger(img,finger = 1,draw=False,drawHandPoints = False)
    
    if finger_pos != None:
        x = previous_mouse_pos_x - (finger_pos[0]*correctionFactor_x)
        y = previous_mouse_pos_y - (finger_pos[1]*correctionFactor_y)
        mouse.move(x,y,absolute=False)
        previous_mouse_pos_x,previous_mouse_pos_y = finger_pos[0]*correctionFactor_x,finger_pos[1]*correctionFactor_y
        print(x,y,correctionFactor_x,correctionFactor_y,mouse.get_position())

    cv2.imshow("Image", img)
    cv2.waitKey(1)