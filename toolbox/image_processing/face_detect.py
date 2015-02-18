""" Experiment with face detection and image filtering using OpenCV """

import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while(True):
	#Capture frame-by-frame
	ret, frame = cap.read()

	#Display frame
	cv2.imshow('frame', frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

#release Capture
cap.release()
cv2.destroyAllWindows()