import astar
import cv2
import numpy as np

class PathFinder():
	def __init__(self, window_size):

		self.window_size = window_size
		self.img = cv2.imread('p_map3.jpg')
		self.img = cv2.resize(self.img, (125,125))
		self.img = cv2.erode(self.img, np.ones((3,3)), iterations=1) 
		self.img = np.asarray(self.img[:,:,1] < 200 ).astype(np.uint)
		#self.dot_path = []
		self.current_loc = []
		self.my_loc = [(60,30), 0, (-1,-1), (-1,-1)]
		self.idx = []
		self.idx_name = []

	def find(self, items_to_buy):
		#print(len(items_to_buy))
		item_pick_up = items_to_buy.copy()
		flag = 0
		#print('removed')
		self.current_loc = self.my_loc
		item_pick_up.sort(key=lambda x: self.L2_dis(self.current_loc[0], x.pos))
		path = []
		self.idx = []
		self.idx_name = []
		for near_item in range(len(item_pick_up)):
			#print(near_item)
			#for e in items_to_buy:
				#print(e.item_name)
			#near_item = self.find_nearest(self.current_loc[0],item_pick_up)
			path = path + self.get_path(self.current_loc,item_pick_up[near_item])
			#item_pick_up.remove(item_pick_up[near_item])
			self.idx.append(len(path))
			self.idx_name.append(item_pick_up[near_item].item_name)
			self.current_loc = [item_pick_up[near_item].pos, 0, item_pick_up[near_item].pos_1, item_pick_up[near_item].pos_2]
			#print(self.current_loc)
			#item_pick_up.pop(near_item)
			#print(near_item)
		print(path)
		return path, self.idx, self.idx_name
	def get_path(self, current_loc, dest_loc):
		#Case 1: The current loc is in the open, not between shelves
		if current_loc[2] == (-1,-1):
			#Go to the loc of the shelf then to the item loc
			#print(dest_loc)
			#print(current_loc)
			enter_shelf_loc = dest_loc.pos_1 if self.L2_dis(dest_loc.pos_1,current_loc[0]) < self.L2_dis(dest_loc.pos_2,current_loc[0]) else dest_loc.pos_2
			path1 = astar.find_path(self.img,current_loc[0],enter_shelf_loc)
			path2 = astar.find_path(self.img,enter_shelf_loc, dest_loc.pos)
			#Update current_loc
			return path1 + path2
		else:
		# Case 2: The current loc is between shelves          
			#Exit the current shelf
			exit_shelf_loc = current_loc[2] if self.L2_dis(dest_loc.pos,current_loc[2]) < self.L2_dis(dest_loc.pos,current_loc[3]) else current_loc[3]
			path1 = astar.find_path(self.img,current_loc[0], exit_shelf_loc) 
			enter_shelf_loc = dest_loc.pos_1 if self.L2_dis(dest_loc.pos_1,exit_shelf_loc) < self.L2_dis(dest_loc.pos_2,exit_shelf_loc) else dest_loc.pos_2
			#Go to the new shelf
			path2 = astar.find_path(self.img,exit_shelf_loc,enter_shelf_loc)
			#Go to the item
			path3 = astar.find_path(self.img,enter_shelf_loc, dest_loc.pos)

			return path1 + path2 +path3
	def find_nearest(self,current_loc, items_to_buy):
		dis = 1e5
		near_item = ''
		#print(len(items_to_buy))
		for item in range(len(items_to_buy)):
			i_dis = self.L2_dis(items_to_buy[item].pos, current_loc)#(addresses[item][0][0] - current_loc[0])**2 + (addresses[item][0][1] - current_loc[1])**2 #L2 Distance
			if i_dis < dis:
				near_item = item
				dis = i_dis
		return near_item

	def L2_dis(self, a, b):
		#print(a)
		#print(b)
		return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2