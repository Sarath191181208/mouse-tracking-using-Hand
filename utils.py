def get_screen_resolution():
    import tkinter

    root   = tkinter.Tk()
    width  = root.winfo_screenwidth()
    height = root.winfo_screenheight()

    return width, height

# converts a value in a range to a value in another range 
# MATHS !!!
def interpolate(x_min, x_max, y_min, y_max, num):
    return (((num-x_min)/(x_max-x_min))* (y_max-y_min) ) + y_min

# Calc dis caluculates the distance between two points given x, y cords of two points
# MATHS !!!
def calc_dis(x1, y1, x2, y2):
    # **2 is the squaring operation in python.
    return ((x1-x2)**2+(y1-y2)**2)**0.5

class Finger():
    def __init__(self,is_open, pos) -> None:
        self.x, self.y = int(pos[0]), int(pos[1])
        self.is_open   = is_open