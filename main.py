import cv2
import mouse 
from colorama import Fore

from handTracking import HandDetector

def get_screen_resolution():
    import tkinter

    root = tkinter.Tk()
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()

    return width, height

def interpolate(x_min, x_max, y_min, y_max, num):
    return (((num-x_min)/(x_max-x_min))* (y_max-y_min) ) + y_min

def main():
    detector = HandDetector(detectionCon=0.8)
    # 0 if you want to use your web cam 1 if you use external webcam ex:phone
    cap = cv2.VideoCapture(0)
    WIN_WIDTH, WIN_HEIGHT = get_screen_resolution()
    _, img = cap.read()
    CAM_WIDTH, CAM_HEIGHT, NO_CHANNELS = img.shape

    print(WIN_WIDTH, WIN_HEIGHT)
    print(CAM_WIDTH, CAM_HEIGHT)

    while True:
        success, img = cap.read()
        img = detector.findHands(img,draw=True)
        finger_pnts, boundary_box = detector.findPosition(img, handNo=0, draw=False, showNumbers=False)

        finger_tips = detector.get_finger_tips(finger_pnts, no_of_fingers=3, draw=True, img=img)
        # we are only observing the three fingers therefore cutting our array to 3 elements
        open_fingers = detector.countFingers(finger_pnts, count=False)[0:3]
        # print(open_fingers)

        # reduntant open_fingers just for safety
        if finger_tips is not None and open_fingers is not None:
            # ---- Moving mouse
            if open_fingers[1] == 1 and sum(open_fingers) == 1:
                # Here 1 represents the index finger
                x, y = finger_tips[1]
                
                mouseX, mouseY = mouse.get_position()
                # Interpolate converts a range of values of different range of values
                # MATHS!!!
                x = interpolate(0, CAM_WIDTH, 0, WIN_WIDTH, x)
                y = interpolate(0, CAM_HEIGHT, 0, WIN_HEIGHT, y)
                # In camera we have mirror image of ourselves  therefore we must 
                # mirror x
                x = WIN_WIDTH-x

                print(x, y, mouseX, mouseY)
                mouse.drag(mouseX, mouseY, x, y ,absolute=True, duration=0.0001)
            # ---- / Moving mouse;

            # cv2.circle(img, (finger_tips[0][0], finger_tips[0][1]), 10, (0, 255, 255), 3)
        

        cv2.imshow("Image", img)
        cv2.waitKey(1)

if __name__ == '__main__':
    main()