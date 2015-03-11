""" Detect Colors? """

import cv2
import numpy as np
import imghdr

#general functions
def avg(lis):
    """ average """
    return sum(lis)/len(lis)

def w_avg(lis, weights):
    """ weighted average """
    avg_w = avg(weights)
    w_lis = [lis[i] * weights[i] / avg_w for i in range(len(lis))]
    return avg(w_lis)

#conversion functions
def pos_to_note(r):
    max_x = 600.
    min_note = 1
    note_range = 19
    scaled_x = 1 - r[0] / max_x
    return int(min_note + (note_range * scaled_x))

def pos_to_vol(r):
    max_y = 500.
    min_vol = 0
    vol_range = 5
    scaled_y = 1 - r[1] / max_y
    return min_vol + (vol_range * scaled_y)

#openCv stuff
class Ball(object):
    def __init__(self, min_color, max_color):
        """
            initialize ball class by starting a video Capture
            and setting initial values for frame, x, and y
            Take in a min and max HSV type color
            for the ball's color threshold
        """
        self.min_color = min_color
        self.max_color = max_color
        self.cap = cv2.VideoCapture(0)
        ret, self.frame = self.cap.read()
        self.filterd = self.frame
        self.x = 0
        self.y = 0

    def filter(self):
        """
            Filter out the desired Colors
            Resets frame to a greyscale image
            with only black and the desired color
        """
        HSV = cv2.COLOR_BGR2HSV
        kernel = np.ones((21, 21), 'uint8')

        gray_image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY, 3)

        hsv_pic = cv2.cvtColor(self.frame, HSV)
        inRange_pic = cv2.inRange(hsv_pic, self.min_color, self.max_color)
        eroded_pic = cv2.erode(inRange_pic, kernel)
        dilated_pic = cv2.dilate(eroded_pic, kernel)

        #res_pic = self.frame - res_pic
        blured_pic = cv2.medianBlur(dilated_pic,5)

        self.filtered = cv2.bitwise_and(gray_image, gray_image, mask = blured_pic)
        #print gray_image

    def find_center(self):
        """
            Uses HoughCircles on the filtered frame to fit circles into the ball
            averages the center of the circles, weighted by their radii
            Sets self.x and self.y to the calculated position
        """
        circles = cv2.HoughCircles(self.filtered, cv2.cv.CV_HOUGH_GRADIENT, 1, 20, param1=30,param2=15,minRadius=0,maxRadius=0)
        if circles == None:
            self.y = 500
        else:
            circles = np.uint16(np.around(circles))

            allx = [i[0] for i in circles[0,:]]
            ally = [i[1] for i in circles[0,:]]
            weights = [i[2] for i in circles[0,:]]

            self.x = w_avg(allx, weights)
            self.y = w_avg(ally, weights)

    def position(self):
        """ Finds the position of the ball """
        ret, self.frame = self.cap.read()
        self.filter()
        self.find_center()

    def print_pos(self):
        """
            For Testing -
                prints positon (x, y) of ball
        """
        print (self.x, self.y)

    def draw(self):
        """ draws frame with ball """
        np.set_printoptions(threshold=np.inf)
        cv2.imshow('frame', cv2.flip(self.filtered, 1))


if __name__ == "__main__":
    #purple
    min_HSV_color = (90, 50, 50)
    max_HSV_color = (140, 255, 255)

    #yellow
    #min_HSV_color = (20, 40, 50)
    #max_HSV_color = (60, 255, 255)

    ball = Ball(min_HSV_color, max_HSV_color)

    while True:

        ball.position()
        ball.draw()
        ball.print_pos()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break



    #release Capture
    ball.cap.release()
    cv2.destroyAllWindows()