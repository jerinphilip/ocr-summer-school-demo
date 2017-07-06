import sys

sys.path.insert(0, '/home/solomon/ss-demo/')
sys.path.insert(0, '/home/solomon/ss-demo/OCR')
sys.path.insert(0, '/home/solomon/ss-demo/OCR/ocr')
from OCR import OCR, segmentation

image_fname = sys.argv[1]
language = sys.argv[2]


text = OCR(image_fname, language)
print(text)
