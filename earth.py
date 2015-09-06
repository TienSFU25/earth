import cv2
import pdb
import sys
import numpy as np

image_dir = 'sample/IMG_'

if len(sys.argv) > 1:
	start_no = int(sys.argv[1])
	end_no = int(sys.argv[2])
	is_normalize = sys.argv[3] == 'y'
else:
	start_no = 1717
	end_no = 1748
	is_normalize = True

ZERO = 0.0001
result_dir = 'results/'

# these are the white, red and black "approximate" regions for the disc
white_x1 = 2876
white_y1 = 1867
white_x2 = 2894
white_y2 = 1877
red_x1 = 2861
red_y1 = 1886
red_x2 = 2872
red_y2 = 1900
black_x1 = 2896
black_y1 = 1887
black_x2 = 2908
black_y2 = 1901

x1s = [white_x1, red_x1, black_x1]
x2s = [white_x2, red_x2, black_x2]
y1s = [white_y1, red_y1, black_y1]
y2s = [white_y2, red_y2, black_y2]


# initializes an excel sheet with boilerplate rows as headers
def add_excel_boilerplate(start_image, end_image, is_normalized):
	import xlsxwriter
	import os.path as op

	if is_normalized:
		tmp = "Normalized"
	else:
		tmp = "Not-normalized"

	file_name = '{}-{}-{}.xlsx'.format(start_image, end_image, tmp)

	is_normalized = str(is_normalized)

	# Create a workbook and add a worksheet.
	workbook = xlsxwriter.Workbook(result_dir + file_name)
	worksheet = workbook.add_worksheet('MyWorksheet')

	first_col = ["Results", "White area", "Red area", "Blue area", "Start image", "End image", "IsNormalized"]
	first_row = ["Red std mean", "Red mean of means", "Green std mean", "Green mean of means"]

	curr_row = 1
	curr_col = 0

	for col in first_col:
		worksheet.write(0, curr_col, col)
		curr_col += 1

	for row in first_row:
		worksheet.write(curr_row, 0, row)
		curr_row += 1

	# write the parameters
	worksheet.write(1, 4, start_image);
	worksheet.write(1, 5, end_image);
	worksheet.write(1, 6, is_normalized);

	return workbook

def write_results(workbook, mean_means, std_averages):
	red_std_avg = std_averages[:3]
	green_std_avg = std_averages[3:6]
	red_mean_means = mean_means[:3]
	green_mean_means = mean_means[3:6]

	ws = workbook.worksheets()[0]
	row = 1
	col = 1

	for results in [red_std_avg, red_mean_means, green_std_avg, green_mean_means]:
		for result in results:
			ws.write(row, col, result)
			col+=1
		row+=1
		col=1

def crop(img, y1, y2, x1, x2):
	return img[y1:y2, x1:x2]

# normalize a picture with rg normalization
def normalize(filename):
	img = cv2.imread(filename, 1)
	b, g, r = cv2.split(img)
	total = np.sum(img, axis=2).astype(np.float64)

	r_ = (r.astype(np.float64)/total*255).astype(np.uint8)
	g_ = (g.astype(np.float64)/total*255).astype(np.uint8)

	if (is_normalize):
		return r_, g_
	else:
		return r, g

def to_cv_image(filename):
	img = cv2.imread(filename, 1)
	b, g, r = cv2.split(img)

	total = np.sum(img, axis=2).astype(np.float64)

	b_ = (b.astype(np.float64)/total*255).astype(np.uint8)
	g_ = (g.astype(np.float64)/total*255).astype(np.uint8)
	r_ = (r.astype(np.float64)/total*255).astype(np.uint8)

	img_ = cv2.merge((b_, g_, r_))

	return (img, img_)

print 'Running starting image: {}, end image: {}, normalize: {}'.format(start_no, end_no, is_normalize)

r_discs = []
g_discs = []

# for white, red and black areas
average_r = [[], [], []]
average_g = [[], [], []]

std_r = [[], [], []]
std_g = [[], [], []]

no_images = end_no - start_no + 1
for i in range(no_images):
	current = start_no + i
	image_path = image_dir + str(current) + '.cr2'

	# rg normalize an image and append the red/green channels to a list
	r, g = normalize(image_path)
	r_discs.append(r)
	g_discs.append(g)

for i in range(no_images):
	# process each area: white, red and black
	for j in range(len(x1s)):
		curr_red = crop(r_discs[i], y1s[j], y2s[j], x1s[j], x2s[j])
		curr_green = crop(g_discs[i], y1s[j], y2s[j], x1s[j], x2s[j])

		# pixel-wise average of the normalized region for red/green channels
		average_r[j].append(np.average(curr_red))
		average_g[j].append(np.average(curr_green))

		# standard deviation of pixels for the normalized region
		std_r[j].append(curr_red.std())
		std_g[j].append(curr_green.std())

# append results to lists to display results in an excel file
std_averages = []
mean_means = []
for average in [average_r, average_g]:
	for area in average:
		std_averages.append(np.array(area).std())
		mean_means.append(np.array(area).mean())

workbook = add_excel_boilerplate(start_no, end_no, is_normalize)
write_results(workbook, mean_means, std_averages)

workbook.close()
