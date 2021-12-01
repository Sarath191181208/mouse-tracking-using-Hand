import cv2
import mouse 
from colorama import Fore, Style

from handTracking import HandDetector

# Heads up
# ** -> power operator in python 
# // _> integer divisoion in python
TRESHOLD_PARAMS = {
    "left"  : 90,  # Left click treshold
    "right" : 40,  # Right click treshold
    "scroll": 100  # Scroll up or down treshold
}

class Finger():
    def __init__(self,is_open, pos) -> None:
        self.x, self.y = int(pos[0]), int(pos[1])
        self.is_open   = is_open
    

def get_screen_resolution():
    import tkinter

    root   = tkinter.Tk()
    width  = root.winfo_screenwidth()
    height = root.winfo_screenheight()

    return width, height

WIN_WIDTH, WIN_HEIGHT = get_screen_resolution()

# 0 if you want to use your web cam 1 if you use external webcam ex:phone
cap    = cv2.VideoCapture(0)
_, img = cap.read()
SCALE_FACTOR = 0.7
CAM_HEIGHT, CAM_WIDTH, NO_CHANNELS = img.shape
# BOUNDARY_WIDTH/ HEIGHT are the boundaries which capture the gestures
BOUNDARY_WIDTH, BOUNDARY_HEIGHT = int(CAM_WIDTH*SCALE_FACTOR), int(CAM_HEIGHT*SCALE_FACTOR)
TRANSLATE_X, TRANSLATE_Y        = (CAM_WIDTH-BOUNDARY_WIDTH)//2, (CAM_HEIGHT-BOUNDARY_HEIGHT)//2
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

def calc_dis(x1, y1, x2, y2):
    # **2 is the squaring operation in python.
    return ((x1-x2)**2+(y1-y2)**2)**0.5

def draw_sq(img):
    cv2.rectangle(img, (TRANSLATE_X, TRANSLATE_Y),
                ( TRANSLATE_X+BOUNDARY_WIDTH, TRANSLATE_Y+BOUNDARY_HEIGHT),(0, 255, 0), 2)

def click(click_btn, x1, y1, x2, y2, img):

    TRESHOLD = TRESHOLD_PARAMS[click_btn]
    dis = calc_dis(x1, y1, x2, y2)
    # Mid point formula 
    # MATHS !!!
    mid_x, mid_y = (x1+x2)//2, (y1+y2)//2

    clr = (0, 0, 255)

    if dis< TRESHOLD:
        clr = (160, 230, 20)
        # TODO: must implement waiting mech or else ...... DOOM!
        mouse.click(click_btn)

    cv2.line(img, (x1, y1), (x2, y2), clr, 2)
    cv2.circle(img, (mid_x, mid_y), 10, clr, cv2.FILLED)

def drag(delta_y):
    mouseX, mouseY = mouse.get_position()
    mouse.drag(mouseX, mouseY, mouseX, mouseY+(delta_y*TRESHOLD_PARAMS["scroll"]) ,absolute=True, duration=0.5)


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
            # Python garbage collector can handle multiple assign's

            thumb_finger = Finger(open_fingers[0], finger_tips[0])
            index_finger = Finger(open_fingers[1], finger_tips[1])
            mid_finger   = Finger(open_fingers[2], finger_tips[2])

            no_open_fingers = sum(open_fingers)

            # ---- Moving mouse -----
            if index_finger.is_open and no_open_fingers==1:
                x, y = index_finger.x, index_finger.y
                move_mouse(x, y)
            # ---- Left click   -----
            elif index_finger.is_open and thumb_finger.is_open and no_open_fingers == 2:
                idx_x, idx_y = index_finger.x, index_finger.y 
                tmb_x, tmb_y = thumb_finger.x, thumb_finger.y 
                # Calc dis caluculates the distance between two points given x, y cords of two points
                # MATHS !!!
                click("left", idx_x, idx_y, tmb_x, tmb_y, img)
            # ----- Right click ------
            elif index_finger.is_open and mid_finger.is_open and no_open_fingers == 2:
                idx_x, idx_y = index_finger.x, index_finger.y 
                mid_x, mid_y = mid_finger.x, mid_finger.y 
                click("right", idx_x, idx_y, mid_x, mid_y, img)

        cv2.imshow("Image", img)
        cv2.waitKey(1)

if __name__ == '__main__':
    main()