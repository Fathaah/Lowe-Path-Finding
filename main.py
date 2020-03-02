import numpy as np
import sys
import cv2
import matplotlib.pyplot as plt
import astar
np.set_printoptions(threshold=sys.maxsize)
img = cv2.imread('p_map3.jpg')
img = cv2.resize(img, (64,64))
# plt.imshow(im, cmap = 'gray')
# plt.show()
#print((im).astype(np.uint))
plt.imshow(img) 
plt.show()



