import cv2
import numpy as np
import sys
from helper import write_if_yes

def crop(img, y1, y2, x1, x2):
	return img[y1:y2, x1:x2]

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print 'A filename is required as an argument to run this script'
	else:
		filename = sys.argv[1]
		img = cv2.imread(filename, 1)

		if len(sys.argv) == 6:
			y1 = sys.argv[2]
			y2 = sys.argv[3]
			x1 = sys.argv[4]
			x2 = sys.argv[5]
		else:
			y = img.shape[0]
			x = img.shape[1]
			x1, x2, y1, y2 = x/4, x*3/4, y/4, y*3/4
		
		print 'Cropping coordinates: {},{},{},{}'.format(x1, x2, y1, y2)

		cropped = crop(img, y1, y2, x1, x2)
		cv2.imshow('The cropped image', cropped)
		cv2.imshow('The original image', img)
		cv2.waitKey(0)
		cv2.destroyAllWindows()

		write_if_yes(cropped, filename, 'cropped')