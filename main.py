import cv2
import mouse 
from colorama import Fore, Style

from handTracking import HandDetector

def get_screen_resolution():
    import tkinter

    root = tkinter.Tk()
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()

    return width, height

WIN_WIDTH, WIN_HEIGHT = get_screen_resolution()

# 0 if you want to use your web cam 1 if you use external webcam ex:phone
cap = cv2.VideoCapture(0)
_, img = cap.read()
CAM_HEIGHT, CAM_WIDTH, NO_CHANNELS = img.shape
SCALE_FACTOR = 0.7
# BOUNDARY_WIDTH/ HEIGHT are the boundaries which capture the gestures
BOUNDARY_WIDTH, BOUNDARY_HEIGHT = int(CAM_WIDTH*SCALE_FACTOR), int(CAM_HEIGHT*SCALE_FACTOR)
TRANSLATE_X, TRANSLATE_Y = (CAM_WIDTH-BOUNDARY_WIDTH)//2, (CAM_HEIGHT-BOUNDARY_HEIGHT)//2
# This is done because dragging the hand down is much harder and error prone than dragging up
# So we just make the capturing rectangle higher 
TRANSLATE_Y = int(TRANSLATE_Y*SCALE_FACTOR)

def interpolate(x_min, x_max, y_min, y_max, num):
    return (((num-x_min)/(x_max-x_min))* (y_max-y_min) ) + y_min

def move_mouse(x, y):
        # Interpolate converts a range of values of different range of values
        # MATHS!!!
        x-=TRANSLATE_X
        y-=TRANSLATE_Y

        if x<0 or x>BOUNDARY_WIDTH or y<0 or y>BOUNDARY_HEIGHT:
            print("outside bounds")
            return

        x = interpolate(0, BOUNDARY_WIDTH, 0, WIN_WIDTH, x)
        y = interpolate(0, BOUNDARY_HEIGHT, 0, WIN_HEIGHT, y)
        # In camera we have mirror image of ourselves  therefore we must 
        # mirror x
        x = WIN_WIDTH-x

        mouse.move(x, y, absolute=True, duration=0)

def draw_sq(img):
    cv2.rectangle(img, (TRANSLATE_X, TRANSLATE_Y),
                ( TRANSLATE_X+BOUNDARY_WIDTH, TRANSLATE_Y+BOUNDARY_HEIGHT),(0, 255, 0), 2)

def main():

    detector = HandDetector(detectionCon=0.8)

    while True:

        success, img = cap.read()
        # draws the boundary square
        draw_sq(img)
        img = detector.findHands(img,draw=True)
        finger_pnts, boundary_box = detector.findPosition(img, handNo=0, draw=False, showNumbers=False)

        finger_tips = detector.get_finger_tips(finger_pnts, no_of_fingers=3, draw=True, img=img)
        # we are only observing the three fingers therefore cutting our array to 3 elements
        open_fingers = detector.countFingers(finger_pnts, count=False)[0:3]

        # reduntant open_fingers check just for safety
        if finger_tips is not None and open_fingers is not None:
            # ---- Moving mouse
            if open_fingers[1] == 1 and sum(open_fingers) == 1:
                # Here 1 represents the index finger
                x, y = finger_tips[1]
                move_mouse(x, y)
            # ---- / Moving mouse;
        

        cv2.imshow("Image", img)
        cv2.waitKey(1)

if __name__ == '__main__':
    main()