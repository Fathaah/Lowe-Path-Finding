import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
import logging
from map import *
from kivy.config import Config 
from kivy.graphics import *
from search import *
from PathFinder import *
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from functools import partial 
Config.set('graphics', 'resizable', True) 
Window.size = (2160 / 4,2160 / 4)
dims = Window.size
Window.clearcolor = (1, 1, 1, 1)
class Main_segment(App):
    def build(self):
        layout = MainLayout()
        map = Map()
        popup = DisplayList(size_hint=(.75, .75 ), title = 'Shopping List',content = Label(text = 'Your shopping list is empty'))
        msg_popup = DisplayList(size_hint = (.75, .5))
        data_handler = DataHandler(map, popup)
        search_bar = SearchBar(data_handler, msg_popup, text = 'Enter item',multiline = False, size_hint=(.8, .05 ),pos_hint={'x':.5 - 0.8 / 2, 'y':1 - .08})
        btn1 = Button(text = 'Shopping List', size_hint=(.8, .05 ),pos_hint={'x':.5 - 0.8 / 2, 'y':.08})
        btn1.bind(on_press = popup.open)
        layout.add_widget(map)
        layout.add_widget(search_bar)
        layout.add_widget(btn1)
        return layout

class MainLayout(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class DataHandler():
    def __init__(self, map, popup):
        self.shopping_list = []
        self.items_dict = {'entrance': [(60,30), 0, (-1,-1), (-1,-1)],'check_out':[(23,4), 0, (23,4), (23,4)],
         'hammer' : [(20, 50), 0, (20, 50), (20, 50)], 'paint': [(29,10),0,(29,0), (29,25) ], 
         'wood' : [(8, 40), 0, (8,36), (8,47)], 'nails': [(47,10),0,(47,0), (47,25)], 'saw': [(12,28), 0, (20, 28), (1, 28)]}
        self.path_finder = PathFinder(dims)
        self.path = []
        self.map = map
        self.popup = popup

    def list_updated(self):
        #print('path')
        self.path, idx, idx_name = self.path_finder.find(self.shopping_list)
        #print(self.path)
        self.map.draw(self.path, idx, idx_name)
        self.popup.updateList(self)
    def add_element(self, element):
        temp = Data(element[0],element[1], element[2], element[3], element[4])
        self.shopping_list.append(temp)
        #print('Appending Successfull')
        #for e in self.shopping_list:
            #print('in shopping list ' + e.item_name)
        self.list_updated()
    def remove_element(self, element, btn):
        print(element[3:])
        temp = self.shopping_list.copy()
        self.shopping_list = []
        for ele in temp:
            if ele.item_name != element[3:]:
                self.shopping_list.append(ele)
        self.list_updated()

class Data():
    def __init__(self, name, pos,on_stock, pos_1, pos_2):
        self.item_name = name
        self.pos = pos
        self.on_stock = on_stock
        self.pos_1 = pos_1
        self.pos_2 = pos_2

class DisplayList(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    def updateList(self, data_handler):
        items_to_buy = data_handler.shopping_list
        content = FloatLayout()
        
        for i in range(len(items_to_buy)):
            btn = Button(text = str(i + 1) + '. ' + items_to_buy[i].item_name, size_hint = (0.9, 0.05), pos_hint = {'x':0 , 'y': 1 - 0.075 * (i + 1)})
            btn.bind(on_press = partial(data_handler.remove_element, btn.text))
            content.add_widget(btn)
        self.content = content


        


if __name__ == "__main__":
    Main_segment().run()

 