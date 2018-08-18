import numpy as np
import cv2

#open image 
img = cv2.imread('image/cat.jpg')

#apply thresholding filter
#ret, img2 = cv2.threshold(img,150,255,cv2.THRESH_BINARY) 
img2 = cv2.resize(img,None,fx=2, fy=2, interpolation = cv2.INTER_CUBIC)

kernel = np.ones((5,5),np.float32)/25
img2 = cv2.filter2D(img,-1,kernel)

#display original and altered images
cv2.imshow('original',img)
cv2.imshow('thresh',img2)

#save img2
cv2.imwrite('catThresh.jpg',img2)

#type any key to end program
cv2.waitKey(0)
cv2.destroyAllWindows()

