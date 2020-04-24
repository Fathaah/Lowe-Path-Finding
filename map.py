import kivy
from kivy.uix.scatter import Scatter
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.graphics import *
from kivy.core.window import Window
from kivy.core.text import Label as CoreLabel
from kivy.clock import Clock
import numpy as np
height_limit = 1500
width_limit = 1500
map_dim = 64
class Map(Scatter): 
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.do_rotation = False
        self.auto_bring_to_front =False
        #Load Image onto the screen
        self.window_size = Window.size
        self.msg_components = []
        with self.canvas:
            Color(1,1,1)
            Rectangle(source = 'Map4.jpg',pos = (-self.window_size[0] / 2, 0), size = (2  * self.window_size[0], 2 * self.window_size[1]))
        self.dot_path = []
        #self.Message()
    def remove_popup(self, touch):
        for item in self.msg_components:
            self.canvas.remove(item)
        self.msg_components = []
    def collide_point(self, x, y):
        x, y = self.to_local(x, y)
        return x <= width_limit and y <= height_limit
    def Message(self, pos, msg = ' is a heavy item, hence \nits planned  to be \npicked up towards the \nend of the shopping trip'):
        size = (300,90)
        print("message")
        with self.canvas:
            self.msg_components.append(Rectangle(source = 'Message.png', pos = (pos[0] - size[0] / 2, pos[1]), size = size))
            mylabel = CoreLabel(text=msg, font_size=16, color=(1, 0, 0, 1))
            mylabel.refresh()
            print(msg)
            texture = mylabel.texture
            texture_size = list(texture.size)
            self.msg_components.append(Rectangle(pos = (pos[0] - texture_size[0] / 2, pos[1] + 25), texture=texture, size=texture_size))
            Clock.schedule_once(self.remove_popup, 7)
    
    def on_transform_with_touch(self,touch):
        #print(self.bbox)
        if(self.bbox[0][0] > height_limit):
            self._set_pos((height_limit,self.bbox[0][1]))
        if(self.bbox[0][0] < -height_limit):
            self._set_pos((-height_limit,self.bbox[0][1]))
        if(self.bbox[0][1] > width_limit):
            self._set_pos((self.bbox[0][0],width_limit))
        if(self.bbox[0][1] < -width_limit):
            self._set_pos((self.bbox[0][0],-width_limit))
    def draw(self, path, idx, idx_name, heavy, item_pot):
        if self.dot_path != []:
            for dot in self.dot_path:
                self.canvas.remove(dot)
            self.remove_popup(self.dot_path)
            self.dot_path = []
        idx1 = [0] + idx
        with self.canvas:
            for k in range(1, len(idx1), 1):
                Color(np.clip(np.random.rand(), 0, .8), np.clip(np.random.rand(), 0, .8), np.clip(np.random.rand(), 0, .8))
                for i in range(idx1[k - 1], idx1[k], 1):
                    #print(i)
                    #Color(np.clip(0.2 + np.random.rand(), 0, 1), np.clip(0.2 + np.random.rand(), 0, 1), np.clip(0.2 + np.random.rand(), 0, 1))
                    self.dot_path.append(Ellipse(pos = ((path[i][1] * self.window_size[0] * 2 / map_dim) - self.window_size[0] // 2,((map_dim - path[i][0]) * self.window_size[1] * 2 / map_dim) - 12), size=(10, 10)))
                        #(x - 133,y)
            #print(heavy)
            Color(0,1,0)
            #print((idx))
            for i in range(len(idx)):
                Color(0,1,0)
                self.dot_path.append(Ellipse(pos = ((path[idx[i] - 1][1] * self.window_size[0] * 2 / map_dim) - self.window_size[0] // 2,((map_dim - path[idx[i] - 1][0]) * self.window_size[1] * 2 / map_dim) - 12), size=(7, 7)))
                Color(1,1,1)
                mylabel = CoreLabel(text=idx_name[i], font_size=20, color=(0, 0, 0, 1))
                mylabel.refresh()
                # Get the texture and the texture size
                texture = mylabel.texture
                texture_size = list(texture.size)
                self.dot_path.append(Rectangle(pos = ((path[idx[i] - 1][1] * self.window_size[0] * 2 / map_dim) - self.window_size[0] // 2 - texture.size[0] / 2,((map_dim - path[idx[i] - 1][0]) * self.window_size[1] * 2 / map_dim) - 12 - 14), texture=texture, size=texture_size))
                self.dot_path.append(Rectangle(pos = ((path[idx[i] - 1][1] * self.window_size[0] * 2 / map_dim) - self.window_size[0] // 2 - texture.size[0] / 2,((map_dim - path[idx[i] - 1][0]) * self.window_size[1] * 2 / map_dim) - 12 - 14), texture=texture, size=texture_size))
                self.dot_path.append(Rectangle(pos = ((path[idx[i] - 1][1] * self.window_size[0] * 2 / map_dim) - self.window_size[0] // 2 - texture.size[0] / 2,((map_dim - path[idx[i] - 1][0]) * self.window_size[1] * 2 / map_dim) - 12 - 14    ), texture=texture, size=texture_size))
            
            if(heavy != []):
                if(heavy[-1]):
                    Color(240/255,240/235,255/255)
                    self.Message(((path[idx[-2] - 1][1] * self.window_size[0] * 2 / map_dim) - self.window_size[0] // 2,((map_dim - path[idx[-2] - 1][0]) * self.window_size[1] * 2 / map_dim) - 12), msg = 'Items like ' + idx_name[-2]+' are categorised as \nheavy item, its planned to \nbe picked up in the end')
            if(item_pot):
                Color(110/255,210/255,250/255)
                self.Message((((item_pot[1][1]) * self.window_size[0] * 2 / map_dim) - self.window_size[0] // 2,((map_dim - item_pot[1][0]) * self.window_size[1] * 2 / map_dim) - 12), msg = 'You might need ' + item_pot[0]+' it is often bought \nwith ' + item_pot[-1] + '.')
