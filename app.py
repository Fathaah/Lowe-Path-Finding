import kivy
from kivy.app import App
from kivy.uix.scatter import Scatter
from kivy.uix.floatlayout import FloatLayout
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
import astar
from kivy.graphics import *
import astar
from functools import partial
import matplotlib.pyplot as plt
import cv2
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



#image = Image(source='map.png', size = map_size , pos = map_pos)
class DataHandler():
    
    def __init__(self):
        self.shopping_list = []
        self.shopping_list.append('entrance')
        self.shopping_list.append('check_out')
        addresses.update({'entrance': (30,10),'check_out':(30,60), 'hammer' : (50, 64 - 25)})
    def add(self,item):
        self.shopping_list.append(item)
        print(self.shopping_list)


class Main_Box(Scatter):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #self.on_transform_with_touch(self.check_pos)
        self.img = cv2.imread('p_map.jpg')
        self.img = cv2.resize(self.img, (64,64))
        self.img = (self.img[:,:,1] < 200 )
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
    def FindPath(self, temp, data):
        print("Finding Path")

        path = astar.find_path(self.img,(60,30),(2,0))
        for i in range(len(path)):
            self.img[path[i][0],path[i][1]] = 127
        with self.canvas:
            Color(1.0,0,0)
            for i in range(len(path)):
                e = Ellipse(pos = ((path[i][1] * 540 / 64) - 133,((64 - path[i][0]) * 540 / 64) - 6 ), size=(3, 3))
                #(x - 133,y)

class InputManager(TextInput):
    

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(on_text_validate=self.on_enter)
        self.data = DataHandler()
    def on_enter(instance,value):
        print(instance.text)
        instance.data.add(instance.text)
        instance.text = ''



class Map_image(Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #self.on_transform_with_touch(self.check_pos)
        self.source = 'map2.png'
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
        scatter = Main_Box(do_rotation = False,auto_bring_to_front =False, do_translation_y=False)
        map_img = Map_image()
        t = InputManager(text = 'Hello world',multiline = False, size_hint=(.8, .05 ),pos_hint={'x':.5 - 0.8 / 2, 'y':1 - .08})
        btn1 = Button(text = 'Find Path', size_hint=(.8, .05 ),pos_hint={'x':.5 - 0.8 / 2, 'y':.08})
        btn1.bind(on_press = partial(scatter.FindPath,t.data))
        scatter.add_widget(map_img)
        f = App_layout()
        f.add_widget(scatter)
        f.add_widget(t)
        f.add_widget(btn1)
        return f

if __name__ == '__main__':
    TestApp().run()




