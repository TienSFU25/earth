import cv2
import numpy as np
import pdb
import sys

from helper import write_if_yes

# normalize a picture with rg normalization
def to_channels(filename, normalize):
	img = cv2.imread(filename, 1)
	b, g, r = cv2.split(img)
	total = np.sum(img, axis=2).astype(np.float64)

	r_ = (r.astype(np.float64)/total*255).astype(np.uint8)
	g_ = (g.astype(np.float64)/total*255).astype(np.uint8)
	b_ = (b.astype(np.float64)/total*255).astype(np.uint8)

	if (normalize):
		return r_, g_, b_
	else:
		return r, g, b

def to_cv_image(channels):
	assert len(channels) == 3
	return cv2.merge(channels)

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print 'A filename is required as an argument to run this script'
	else:
		filename = sys.argv[1]
		rgb = to_channels(sys.argv[1], normalize=True)
		img = to_cv_image(rgb)
		cv2.imshow('The normalized image', img)
		cv2.waitKey(0)
		cv2.destroyWindow('The normalized image')

		write_if_yes(img, filename, 'normalized')