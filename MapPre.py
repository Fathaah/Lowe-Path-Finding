import numpy as np
import sys
import cv2
import matplotlib.pyplot as plt
import astar
np.set_printoptions(threshold=sys.maxsize)
img = cv2.imread('p_map.jpg',0)
img = cv2.resize(img, (64,64))
# im = np.asarray(img)
img = np.asarray((img[:] > 250 ).astype(np.uint))
plt.imshow(img, cmap = 'gray')
plt.show()