""" Experiment with face detection and image filtering using OpenCV """

import cv2
import numpy as np

cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier('/home/rdiverdi/haarcascade_frontalface_alt.xml')
kernel = np.ones((51,51),'uint8')

def draw_face(frame, left, top, width, height):
    white = (255, 255, 255)
    black = (150, 20, 150)
    red = (0, 0, 255)

    eye1x = int(left + width/3)
    eye2x = int(left + 2*width/3)
    eyey = int(top + height/3)
    eye_size = width / 13
    cv2.circle(frame, (eye1x, eyey), eye_size, white, -1)
    cv2.circle(frame, (eye2x, eyey), eye_size, white, -1)
    cv2.circle(frame, (eye1x + eye_size/4, eyey + eye_size/8), eye_size/2, black, -1)
    cv2.circle(frame, (eye2x + eye_size/4, eyey + eye_size/8), eye_size/2, black, -1)

    mouthx = int(left + width/2)
    mouthy = int(top + height/2)
    cv2.ellipse(frame, (mouthx, mouthy), (width/4, width/4), 0, 20, 160, red, width/30)



while(True):
    #Capture frame-by-frame
    ret, frame = cap.read()
    faces = face_cascade.detectMultiScale(frame, scaleFactor=1.2, minSize=(20,20))
    for (x, y, w, h) in faces:
        frame[y:y+h,x:x+w,:] = cv2.dilate(frame[y:y+h,x:x+w,:], kernel)
        #cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255))
        draw_face(frame, x, y, w, h)
    #Display frame
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#release Capture
cap.release()
cv2.destroyAllWindows()