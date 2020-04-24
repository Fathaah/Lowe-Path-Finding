import kivy
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import *
class SearchBar(TextInput):
    def __init__(self,data_handler,message_popup, **kwargs):
        super().__init__(**kwargs)
        self.data_handler = data_handler
        self.bind(on_text_validate=self.on_enter)
        self.bind(focus=self.on_focus)
        self.dropdown = DropDown()
        self.message_popup = message_popup
        #self.add_widget(DropDown)
        for _, i in enumerate(data_handler.items_dict.items()):
            if _ > 2:
                print(i)
                btn = Button(text= i[0], size_hint_y=None, height=20)
                btn.bind(on_release = lambda btn: self.data_handler.add_element([btn.text] + data_handler.items_dict[btn.text]))
                self.dropdown.add_widget(btn)

    def on_enter(instance,value):
        #print(instance.text)
        if instance.text in instance.data_handler.items_dict:
            data = instance.data_handler.items_dict[instance.text]
            #print(data)
            instance.data_handler.add_element([instance.text] + data)
            instance.text = ''
        else:
            instance.message_popup.title = 'Error'
            popup_con = instance.message_popup.content = FloatLayout()
            popup_con.add_widget(Label(text = 'Sorry, item not found', pos_hint = {'x':0 , 'y': 0}))
            popup_con.add_widget(Label(text = '[b][color=#B6B3B3]Tap here to close the popup[/color][/b]', pos_hint = {'x':0 , 'y': -.7}, markup = True))
            instance.message_popup.open()
            

    def on_focus(instance, value,_):
        instance.text = ''
        #print(instance.dropdown)
        #instance.dropdown.open(instance)
        #print(_)
    def on_touch_up(self, touch):
        if touch.grab_current == self:
            self.dropdown.open(self)
        return super(SearchBar, self).on_touch_up(touch)
    
    
    
