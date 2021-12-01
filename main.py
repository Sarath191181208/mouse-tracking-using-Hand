import cv2
import mouse 
from colorama import Fore, Style

# user defined modules
from handTracking import HandDetector
import utils

# !! Heads up  !!
# ** -> power operator in python 
# // -> integer divisoion in python
# x, y = y, x -> tuple unpacking
# !! /Heads up !!

TRESHOLD_PARAMS = {
    "left"  : 90,  # Left click treshold
    "right" : 40,  # Right click treshold
}

#################################
######## HANDY CONSTANTS ########
#################################
WIN_WIDTH, WIN_HEIGHT = utils.get_screen_resolution()

# 0 if you want to use your web cam 1 if you use external webcam ex:phone
cap    = cv2.VideoCapture(0)
# cap.read also returns a sucess var
_, img = cap.read()
SCALE_FACTOR = 0.7
CAM_HEIGHT, CAM_WIDTH, NO_CHANNELS = img.shape
# BOUNDARY_WIDTH/ HEIGHT are the boundaries which capture the gestures
BOUNDARY_WIDTH, BOUNDARY_HEIGHT = int(CAM_WIDTH*SCALE_FACTOR), int(CAM_HEIGHT*SCALE_FACTOR)
# TRANSLATION FACTORS USED LATER
TRANSLATE_X, TRANSLATE_Y        = (CAM_WIDTH-BOUNDARY_WIDTH)//2, (CAM_HEIGHT-BOUNDARY_HEIGHT)//2
# This is done because dragging the hand down is much harder and error prone than dragging up
# So we just make the capturing rectangle higher 
TRANSLATE_Y = int(TRANSLATE_Y*SCALE_FACTOR)
################################

def transform_cord(x, y):
    # Transforms coordinated to mouse movement onto the screen
    x-=TRANSLATE_X
    y-=TRANSLATE_Y

    if x<0 or x>BOUNDARY_WIDTH or y<0 or y>BOUNDARY_HEIGHT:
        return None, None

    # Interpolate converts a range of values of different range of values
    # MATHS!!!
    x = utils.interpolate(0, BOUNDARY_WIDTH, 0, WIN_WIDTH, x)
    y = utils.interpolate(0, BOUNDARY_HEIGHT, 0, WIN_HEIGHT, y)

    return x, y

def move_mouse(x, y):

        x, y = transform_cord(x, y)
        # Error handling 
        if x is None or y is None:
            return
        # In camera we have mirror image of ourselves  therefore we must 
        # mirror x
        x = WIN_WIDTH-x

        mouse.move(x, y, absolute=True, duration=0)

def draw_sq(img):
    cv2.rectangle(img, (TRANSLATE_X, TRANSLATE_Y),
                ( TRANSLATE_X+BOUNDARY_WIDTH, TRANSLATE_Y+BOUNDARY_HEIGHT),(0, 255, 0), 2)

def click(click_btn, x1, y1, x2, y2, img):

    TRESHOLD = TRESHOLD_PARAMS[click_btn]
    dis = utils.calc_dis(x1, y1, x2, y2)
    # Mid point formula 
    # MATHS !!!
    mid_x, mid_y = (x1+x2)//2, (y1+y2)//2

    clicked = False
    clr = (0, 0, 255)

    if dis< TRESHOLD:
        clr = (160, 230, 20)
        clicked = True
        # TODO: must implement waiting mech or else ...... DOOM!
        mouse.click(click_btn)

    cv2.line(img, (x1, y1), (x2, y2), clr, 2)
    cv2.circle(img, (mid_x, mid_y), 10, clr, cv2.FILLED)

    # return true or false if right click or not to make scroll work
    return clicked

def drag(delta_y):
    mouseX, mouseY = mouse.get_position()
    mouse.drag(mouseX, mouseY, mouseX, delta_y ,absolute=True, duration=0)

# These are all the gestures of the project
def gestures(thumb_finger, index_finger, mid_finger, num_open_fingers):
    # ----  Moving mouse -----
    if index_finger.is_open and num_open_fingers==1:
        x, y = index_finger.x, index_finger.y
        move_mouse(x, y)

    # ----  Left click   -----
    elif index_finger.is_open and thumb_finger.is_open and num_open_fingers == 2:
        idx_x, idx_y = index_finger.x, index_finger.y 
        tmb_x, tmb_y = thumb_finger.x, thumb_finger.y 

        click("left", idx_x, idx_y, tmb_x, tmb_y, img)

    # ----- Right click ------
    elif index_finger.is_open and mid_finger.is_open and num_open_fingers == 2:

        idx_x, idx_y = index_finger.x, index_finger.y 
        mid_x, mid_y = mid_finger.x, mid_finger.y 
        # if the click was legitemate or not
        clicked = click("right", idx_x, idx_y, mid_x, mid_y, img)

    # -----    Drag    ------
        if not clicked:
            trans_x, trans_y = transform_cord(idx_x, idx_y )
            drag(trans_y)


def main():

    detector = HandDetector(detectionCon=0.8)

    while True:

        success, img = cap.read()
        # draws the boundary square
        draw_sq(img)

        img = detector.findHands(img,draw=True)
        finger_pnts, boundary_box = detector.findPosition(img, handNo=0, draw=False, showNumbers=False)

        # we are only observing the three fingers therefore cutting our array to 3 elements
        finger_tips = detector.get_finger_tips(finger_pnts, no_of_fingers=3, draw=True, img=img)[:3]
        open_fingers = detector.countFingers(finger_pnts, count=False)[:3]

        # reduntant open_fingers check just for safety
        if finger_tips is not None and open_fingers is not None:
            # Python garbage collector can handle multiple assign's
            thumb_finger = utils.Finger(open_fingers[0], finger_tips[0])
            index_finger = utils.Finger(open_fingers[1], finger_tips[1])
            mid_finger   = utils.Finger(open_fingers[2], finger_tips[2])

            num_open_fingers = sum(open_fingers)
            gestures(thumb_finger, index_finger, mid_finger, num_open_fingers)

        cv2.imshow("Image", img)
        key = cv2.waitKey(1)

        # 113 : q
        # 27  : esc
        if key in [113, 27]:
            break
    quit()

if __name__ == '__main__':
    main()