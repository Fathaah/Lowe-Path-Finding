import numpy as np
import sys
import cv2
import matplotlib.pyplot as plt
import astar
np.set_printoptions(threshold=sys.maxsize)
img = cv2.imread('p_map.jpg')
img = cv2.resize(img, (64,64))
im = (im[:,:,1] < 200 ).astype(np.uint)
# plt.imshow(im, cmap = 'gray')
# plt.show()
#print((im).astype(np.uint))
path = astar.find_path(im,(55,30),(2,3))
print(path[0][1])
for i in range(len(path)):
    img[path[i][0],path[i][1]] = 127

plt.imshow(img) 
plt.show()



