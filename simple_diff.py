import cv2
import numpy as np
import pdb
import sys
from helper import write_if_yes

from simple_crop import crop

# normalize a picture with rg normalization
def to_cv_image(filename):
	img = cv2.imread(filename, 1)
	return img

if __name__ == "__main__":
	if len(sys.argv) < 3:
		print 'Two filenames are required as an argument to run this script'
	else:
		if len(sys.argv) > 3:
			THRESHOLD = int(sys.argv[3])

		file1, file2 = sys.argv[1], sys.argv[2]
		img_1 = to_cv_image(file1)
		img_2 = to_cv_image(file2)

		height = min(img_1.shape[0], img_2.shape[0])
		width = min(img_1.shape[1], img_2.shape[1])
		img_1 = crop(img_1, 0, height, 0, width)
		img_2 = crop(img_2, 0, height, 0, width)
		img = img_1 - img_2

		# pdb.set_trace()
		cv2.imshow('First', img_1)
		cv2.imshow('Second', img_2)
		cv2.imshow('The diff', img)

		cv2.waitKey(0)
		cv2.destroyAllWindows()

		write_if_yes(img, file1, 'diff')