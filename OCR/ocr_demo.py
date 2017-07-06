import cv2
from ocr import GravesOCR
import os
def segment(img):
	def crop(bbox):
		x, y, w, h = bbox
		line_crop = img[y:y+h, x:x+w]
	
		newHeight = 32
		aspectRatio = (float(w) / float(h))
		newWidth = int(np.ceil(aspectRatio * newHeight))
		try:
			resized_image = cv2.resize(line_crop, (int(newWidth), int(newHeight)), interpolation=cv2.INTER_AREA)
		except Exception as e:
			print (int(newWidth), int(newHeight))

	return crop



def segmentation(image):
	subprocess.call('./j-layout' + ' ' + image+' '+'-psm'+' '+str(6), shell=True)
	segmentation_file = str(image)+'.lines.txt'
	extract = lambda x: list(map(int, x.strip().split()))
	bboxes = map(extract, segmentation_file)
	img = cv2.imread(image)
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	_, binarized = cv2.threshold(grayscale, 0, 1, cv2.THRESH_OTSU)
	segments = list(map(segment(binarized), bboxes))
	return segments


def OCR(image, language):
	line_images = segmentation(image)
	images=[]
	model = 'parameters/models'+language+'.xml'
	lookup = 'parameters/lookups'+language+'.txt'
	ocr = GravesOCR(model, lookup)
	
	for each_image in line_images:
		images.extends(each_image)

	predictions = [ocr.recognize(image) for image in images]
	return '\n'.join(predictions)
	

