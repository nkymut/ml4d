import numpy as np
import cv2

#open webcamera
cap = cv2.VideoCapture(0)

#display original and altered images
while(True):
	# Capture frame-by-frame
	ret, frame = cap.read()

	# Our operations on the frame come here
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	#apply thresholding filter
	ret, gray = cv2.threshold(gray,150,255,cv2.THRESH_BINARY)
	# Display the resulting frame
	cv2.imshow('frame',gray)
	# type "q" to end program
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

