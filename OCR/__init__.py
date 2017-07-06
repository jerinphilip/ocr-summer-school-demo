import cv2
from ocr import GravesOCR
import os
import subprocess
import numpy as np

def segment(img):
    def crop(bbox):
        x, y, w, h = bbox
        line_crop = img[y:y+h, x:x+w]
    
        newHeight = 32
        aspectRatio = (float(w) / float(h))
        newWidth = int(np.ceil(aspectRatio * newHeight))
        try:
            resized_image = cv2.resize(line_crop, (int(newWidth), int(newHeight)), interpolation=cv2.INTER_AREA)
            return resized_image
        except Exception as e:
            print(e)
            print (int(newWidth), int(newHeight))

    return crop



def segmentation(image):
    folder = '/home/solomon/jlayoutV1/codes/'
    binary = folder + '/j-layout'
    command = "%s %s -psm %d"%(binary, image, 6)
    subprocess.call(command, shell=True)
    segmentation_filename = str(image)+'.lines.txt'
    segmentation_file = open(segmentation_filename)
    extract = lambda x: list(map(int, x.strip().split()))
    bboxes = map(extract, segmentation_file)
    img = cv2.imread(image)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binarized = cv2.threshold(gray, 0, 1, cv2.THRESH_OTSU)
    segments = list(map(segment(binarized), bboxes))
    return segments


def OCR(image, language):
    line_images = segmentation(image)
    images=[]
    param_folder = '/home/solomon/ss-demo/OCR/parameters'
    model = "%s/models/%s.xml"%(param_folder, language)
    lookup = "%s/lookups/%s.txt"%(param_folder, language)
    
    ocr = GravesOCR(model, lookup)
    
    for each_image in line_images:
        images.extend(each_image)

    predictions = [ocr.recognize(image) for image in images]
    return '\n'.join(predictions)
    

