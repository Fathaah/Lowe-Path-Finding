import kivy
from kivy.app import App
from kivy.uix.scatter import Scatter
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.config import Config
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import *
from kivy.uix.textinput import TextInput
from kivy.core.text import Label as CoreLabel
import astar
from kivy.graphics import *
import astar
from functools import partial
import matplotlib.pyplot as plt
import cv2
import numpy as np
Window.size = (1080 / 4,2160 / 4)
dims = Window.size
print(dims)
scale_factor = 2
map_size = [dims[0] * scale_factor , dims[1] * scale_factor]
map_pos = [dims[0] / scale_factor - map_size[0] / scale_factor , dims[1] / scale_factor - map_size[1] / scale_factor]
print(map_size)
print(map_pos)
height_limit = 132
width_limit = 132
addresses = {}
items_to_buy = []
current_loc = [(60,30), 0, (-1,-1), (-1,-1)]

def L2_dis(a, b):
    print(a)
    print(b)
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2

def find_nearest(current_loc, items_to_buy):
    dis = 1e5
    near_item = ''
    for item in items_to_buy:
        i_dis = L2_dis(addresses[item][0], current_loc)#(addresses[item][0][0] - current_loc[0])**2 + (addresses[item][0][1] - current_loc[1])**2 #L2 Distance
        if i_dis < dis:
            near_item = item
            dis = i_dis
    return near_item

def find_near_marker(markers, loc):
    dis_list = []
    for marker in markers:
        dis_list.append(L2_dis(marker,loc))
    dis_list.sort()
    return dis_list
#image = Image(source='map.png', size = map_size , pos = map_pos)
class DataHandler():
    
    def __init__(self, Main, dis):
        addresses.update({'entrance': [(60,30), 0, (-1,-1), (-1,-1)],'check_out':[(23,4), 0, (23,4), (23,4)], 'hammer' : [(20, 50), 0, (20, 50), (20, 50)], 'paint': [(29,10),0,(29,0), (29,25) ], 'wood' : [(8, 40), 0, (8,36), (8,47)], 'nails': [(47,10),0,(47,0), (47,25)]})
        self.main = Main
        self.disp = dis
    def add(self,item):
        items_to_buy.append(item)
        self.disp.updateList()
        #Get address from the DB and append to the addresses
        self.main.FindPath()
        print(items_to_buy)


class DisplayList(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.updateList()
    def updateList(self):
        box = BoxLayout()
        content = ''
        k = 1
        if items_to_buy == []:
            content = 'Your shopping list is empty'
        for i in items_to_buy:
            content += '\n' + str(k) + '.' + i
            k += 1
        
        self.content = Label(text = content)


class Main_Box(Scatter):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        #self.on_transform_with_touch(self.check_pos)
        self.img = cv2.imread('p_map3.jpg')
        self.img = cv2.resize(self.img, (64,64))
        self.img_markers = cv2.imread('marker_map.jpg', 0)
        #self.img_markers = np.asarray(self.img[:,:] > 200 ).astype(np.uint)
        # plt.imshow(self.img_markers, cmap = 'gray')
        # plt.show()
        # self.junc_points = []
        # print(self.img_markers.shape)
        # for i in range(self.img_markers.shape[0]):
        #     for j in range(self.img_markers.shape[1]):
        #         if self.img_markers[i,j] > 240:
        #             self.junc_points.append((i,j))
        # print((self.junc_points))
        self.img = np.asarray(self.img[:,:,1] < 200 ).astype(np.uint)
        self.dot_path = []
    def Scan_loc(self, temp):
        print("Barcode Scanning")
        #Update start Location

    def on_transform_with_touch(self,touch):
        
        print(self.bbox)
        if(self.bbox[0][0] > height_limit):
            self._set_pos((height_limit,self.bbox[0][1]))
        if(self.bbox[0][0] < -height_limit):
            self._set_pos((-height_limit,self.bbox[0][1]))
        if(self.bbox[0][1] > width_limit):
            self._set_pos((self.bbox[0][0],width_limit))
        if(self.bbox[0][1] < -width_limit):
            self._set_pos((self.bbox[0][0],-width_limit))
        with self.canvas:
            Color(1.0,0,0)
            e = Ellipse(pos = (0,0), size=(10, 10))
    def FindPath(self):
        global current_loc
        #current_loc = [(60,30), 0, (-1,-1), (-1,-1)]
        print(items_to_buy)
        item_pick_up = items_to_buy.copy()
        flag = 0
        print('removed')
        if self.dot_path == []:
            pass
        else:
            for dots in self.dot_path:
                self.canvas.remove(dots)
            print('removed')
            self.dot_path = []
        while item_pick_up != []:
            if item_pick_up == []:
                path = astar.find_path(self.img,current_loc[0],addresses['check_out'][0]) 
                current_loc = addresses['check_out']
                flag = 1
                near_item = 'check_out'
            else:
                near_item = find_nearest(current_loc[0],item_pick_up)
                path= self.get_path(current_loc,addresses[near_item])
                item_pick_up.remove(near_item)
                current_loc = addresses[near_item]
            #self.canvas.clear()
            mylabel = CoreLabel(text=near_item, font_size=10, color=(1, 0, 0, 1))
            mylabel.refresh()
            # Get the texture and the texture size
            texture = mylabel.texture
            texture_size = list(texture.size)
            with self.canvas:
                Color(1.0,0,0)
                for i in range(len(path)):
                    self.dot_path.append(Ellipse(pos = ((path[i][1] * 540 / 64) - 133,((64 - path[i][0]) * 540 / 64) - 6 ), size=(3, 3)))
                    #(x - 133,y)
                Color(0,1,0)
                self.dot_path.append(Ellipse(pos = ((path[-1][1] * 540 / 64) - 133,((64 - path[-1][0]) * 540 / 64) - 6 ), size=(5, 5)))
            (self.canvas.add(Rectangle(pos = ((path[-1][1] * 540 / 64) - 133 - texture.size[0] / 2,((64 - path[-1][0]) * 540 / 64) - 6 + 10), texture=texture, size=texture_size)))
            #self.add_widget(Label(text = near_item, pos = (7 + (path[-1][1] * 540 / 64) - 133,((64 - path[-1][0]) * 540 / 64) - 6 )))
            if flag:
                break
    def get_path(self, current_loc, dest_loc):
        #Case 1: The current loc is in the open, not between shelves
        if current_loc[2] == (-1,-1):
            #Go to the loc of the shelf then to the item loc
            print(dest_loc)
            print(current_loc)
            enter_shelf_loc = dest_loc[2] if L2_dis(dest_loc[2],current_loc[0]) < L2_dis(dest_loc[3],current_loc[0]) else dest_loc[3]
            path1 = astar.find_path(self.img,current_loc[0],enter_shelf_loc)
            path2 = astar.find_path(self.img,enter_shelf_loc, dest_loc[0])
            #Update current_loc
            return path1 + path2
        else:
        # Case 2: The current loc is between shelves          
            #Exit the current shelf
            exit_shelf_loc = current_loc[2] if L2_dis(dest_loc[0],current_loc[2]) < L2_dis(dest_loc[0],current_loc[3]) else current_loc[3]
            path1 = astar.find_path(self.img,current_loc[0], exit_shelf_loc) 
            enter_shelf_loc = dest_loc[2] if L2_dis(dest_loc[2],exit_shelf_loc) < L2_dis(dest_loc[3],exit_shelf_loc) else dest_loc[3]
            #Go to the new shelf
            path2 = astar.find_path(self.img,exit_shelf_loc,enter_shelf_loc)
            #Go to the item
            path3 = astar.find_path(self.img,enter_shelf_loc, dest_loc[0])

            return path1 + path2 +path3
class InputManager(TextInput):
    

    def __init__(self,Main,disp, **kwargs):
        super().__init__(**kwargs)
        self.bind(on_text_validate=self.on_enter)
        self.data = DataHandler(Main, disp)
    def on_enter(instance,value):
        print(instance.text)
        instance.data.add(instance.text)
        instance.text = ''



class Map_image(Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #self.on_transform_with_touch(self.check_pos)
        self.source = 'map3.png'
        self.size = map_size
        self.pos = map_pos
        self.Rell = RelativeLayout()
        print(self.Rell.pos)
        self.add_widget(self.Rell)

class App_layout(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs) 
class TestApp(App):
    def build(self):
        map_img = Map_image()
        scatter = Main_Box(do_rotation = False,auto_bring_to_front =False, do_translation_y=False)
        popup = DisplayList(title='Shopping List ',
        size_hint=(.75, .75 ))
        t = InputManager(scatter,popup, text = 'Hello world',multiline = False, size_hint=(.8, .05 ),pos_hint={'x':.5 - 0.8 / 2, 'y':1 - .08})
        #btn1 = Button(text = 'Find Path', size_hint=(.8, .05 ),pos_hint={'x':.5 - 0.8 / 2, 'y':.08})
        btn2 = Button(text = 'Shopping List', size_hint=(.8, .05 ),pos_hint={'x':.5 - 0.8 / 2, 'y':.08})
        btn3 = Button(text = 'Scan and Get Position', size_hint=(.8, .05 ),pos_hint={'x':.5 - 0.8 / 2, 'y':.18})
        #btn1.bind(on_press = partial(scatter.FindPath))
        btn3.bind(on_press = scatter.Scan_loc)
        btn2.bind(on_press = popup.open)
        scatter.add_widget(map_img)
        f = App_layout()
        f.add_widget(scatter)
        f.add_widget(t)
        #f.add_widget(btn1)
        f.add_widget(btn2)
        f.add_widget(btn3)
        return f

if __name__ == '__main__':
    TestApp().run()




