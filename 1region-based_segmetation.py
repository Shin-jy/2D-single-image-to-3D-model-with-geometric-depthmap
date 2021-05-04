import numpy as np
import cv2
from matplotlib import pyplot as plt

Input = './input/input.jpg'
Output = './output/seg/'

img = cv2.imread(Input)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
cv2.imwrite(Output+'gray.jpg',gray)

ret, thresh = cv2.threshold(gray,50,200,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
cv2.imshow('img1',thresh)
cv2.imwrite(Output+'seg_threshold.jpg', thresh)

kernel = np.ones((10,10), np.uint8)
open1 = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
cv2.imwrite(Output+'seg_morpholagy.jpg', open1)
cv2.imwrite('./output/seg_final.jpg', open1)

