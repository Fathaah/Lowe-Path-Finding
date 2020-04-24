import astar
import cv2
import numpy as np
from main import Data

class PathFinder():
	def __init__(self, window_size, item_dict):

		self.window_size = window_size
		self.img = cv2.imread('p_map3.jpg')
		self.img = cv2.resize(self.img, (64,64))
		self.img = cv2.erode(self.img, np.ones((2,2)), iterations=1) 
		self.img = np.asarray(self.img[:,:,1] < 200 ).astype(np.uint)
		#self.dot_path = []
		self.current_loc = []
		self.my_loc = [(120//2,64//2), 0, (-1,-1), (-1,-1)]
		self.check_out_1 = Data('Check_out_1',(115//2,40//2),0,(100 // 2,25 // 2),(100 // 2,52 // 2), None)
		self.check_out_2 = Data('Check_out_2',(115//2,96//2),0,(100 // 2,73 // 2),(100,100 // 2), None)
		self.item_dict = item_dict
		self.idx = []
		self.idx_name = []
	def find(self, items_to_buy):
		#print(len(items_to_buy))
		item_pick_up = items_to_buy.copy()
		print(items_to_buy)
		flag = 0
		#print('removed')
		self.current_loc = self.my_loc
		path = []
		self.idx = []
		self.idx_name = []
		self.heavy = []
		item_pot = None
		#for light items
		for i in range(len(item_pick_up)):
			#print(near_item)
			#for e in items_to_buy:
				#print(e.item_name)
			#near_item = self.find_nearest(self.current_loc[0],item_pick_up)
			
			item_pick_up.sort(key=lambda x: self.L2_dis(self.current_loc[0], x.pos) )
			item_pick_up.sort(key = lambda x: x.heavy)

			path = path + self.get_path(self.current_loc,item_pick_up[0])
			#item_pick_up.remove(item_pick_up[near_item])
			self.idx.append(len(path))
			self.idx_name.append(item_pick_up[0].item_name)
			if item_pick_up[0].pot_buy:
				item_pot = [item_pick_up[0].pot_buy] + self.item_dict[item_pick_up[0].pot_buy] + [item_pick_up[0].item_name]

			if(item_pick_up[0].heavy == 1):
				self.heavy.append(1)
			else:
				self.heavy.append(0)
			self.current_loc = [path[-1], 0, item_pick_up[0].pos_1, item_pick_up[0].pos_2]
			print('pick up ', i, ' ' + item_pick_up[0].item_name + ' ' + str(item_pick_up[0].heavy))
			item_pick_up.pop(0)
		if (len(items_to_buy) < 4 and len(items_to_buy) > 0):
			path = path + self.get_path(self.current_loc, self.check_out_2)
			self.idx.append(len(path))
			self.idx_name.append('Check Out')
		elif(len(items_to_buy) != 0):
			path = path + self.get_path(self.current_loc,self.check_out_1)
			self.idx.append(len(path))
			self.idx_name.append('Check Out')
		return path, self.idx, self.idx_name, self.heavy, item_pot
	def get_path(self, current_loc, dest_loc):
		#Case 1: The current loc is in the open, not between shelves
		if dest_loc.pos_1 == current_loc[2] or dest_loc.pos_1 == current_loc[2]:
			path = astar.find_path(self.img,current_loc[0],dest_loc.pos)
			return path
		if current_loc[2] == (-1,-1):
			#Go to the loc of the shelf then to the item loc
			#print(dest_loc)
			#print(current_loc)
			if dest_loc.pos_1 != (-1, -1):
				enter_shelf_loc = dest_loc.pos_1 if self.L2_dis(dest_loc.pos_1,current_loc[0]) < self.L2_dis(dest_loc.pos_2,current_loc[0]) else dest_loc.pos_2
				path1 = astar.find_path(self.img,current_loc[0],enter_shelf_loc)
				path2 = astar.find_path(self.img,path1[-1], dest_loc.pos)
			else:
				path1 = []
				path2 = astar.find_path(self.img,current_loc[0], dest_loc.pos)
			#Update current_loc
			return path1 + path2
		else:
		# Case 2: The current loc is between shelves          
			#Exit the current shelf
			exit_shelf_loc = current_loc[2] if self.L2_dis(dest_loc.pos,current_loc[2]) < self.L2_dis(dest_loc.pos,current_loc[3]) else current_loc[3]
			path1 = astar.find_path(self.img,current_loc[0], exit_shelf_loc) 
			
			if dest_loc.pos_1 != (-1, -1):
				enter_shelf_loc = dest_loc.pos_1 if self.L2_dis(dest_loc.pos_1,exit_shelf_loc) < self.L2_dis(dest_loc.pos_2,exit_shelf_loc) else dest_loc.pos_2
				#Go to the new shelf
				path2 = astar.find_path(self.img,path1[-1],enter_shelf_loc)
				#Go to the item
				path3 = astar.find_path(self.img,path2[-1], dest_loc.pos)
			elif dest_loc.pos_1 == (-1, -1):
				path2 = []
				path3 = astar.find_path(self.img,path1[-1], dest_loc.pos)
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
