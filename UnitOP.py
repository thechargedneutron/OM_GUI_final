from kivy.app import App
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty
from kivy.properties import NumericProperty
from kivy.graphics.vertex_instructions import Rectangle
from kivy.graphics.vertex_instructions import Line
from kivy.uix.bubble import Bubble
from kivy.uix.popup import Popup
from functools import partial
from kivy.uix.scrollview import ScrollView
from kivy.uix.slider import Slider
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics.context_instructions import Color
from kivy.graphics.instructions import InstructionGroup
from kivy.lang import Builder
from kivy.uix.dropdown import DropDown
from url import OmWidget
Builder.load_file('popup.kv')

class cPopUp(Popup):
    pass
class dDown(DropDown):
    DrNumber = NumericProperty(0)

class butt(Button):
    DrNumber = NumericProperty(0)

class UnitOP(Button):
        Operators = []
        drop_connections = {}
        size_limit = [100, 100]
        unpressed = ListProperty([0, 0])
        double_tap = NumericProperty(0)
        multi_touch = NumericProperty(0)
        current_touch = None
        line_move = NumericProperty(0)
        connect = NumericProperty(0)


        def __init__(self, **kwargs):
            super(UnitOP, self).__init__(**kwargs)
            self.size_hint = None, None
            self.size = (30, 15)
            self.connected = False
            self.background_normal = 'MatStm.png'
            self.PropertyList = []
            self.PropertyObj = []
            self.PropertyVal = ['50','101.325','100']
            self.OM_Model = ''
            self.name = ''
            self.PropInput = [TextInput(size_hint_y=None, height=25, valign='middle', font_size=12, multiline=False),TextInput(size_hint_y=None, height=25, valign='middle', font_size=12, multiline=False),TextInput(size_hint_y=None, height=25, valign='middle', font_size=12, multiline=False)]
            self.conn_point = 0
            self.check_stm = 1
            self.DropDowns =[]
            self.MainButton = []



        def on_touch_down(self, touch):
            if self.collide_point(*touch.pos):
                if touch.is_double_tap:
                    touch.multitouch_sim = True
                    self.multi_touch = self.multi_touch + 1
                # if 'multitouch_sim' in touch.profile:
                #     touch.multitouch_sim = True
                #     self.multi_touch = self.multi_touch + 1
                else:
                    touch.grab(self)
            return False

        def on_touch_up(self, touch):
            if touch.grab_current is self:
                self.unpressed = touch.pos
                touch.ungrab(self)
            return True


        def on_touch_move(self, touch):
            if touch.grab_current is self:
                if touch.x > UnitOP.size_limit[0]-self.size[0]:
                    self.x = UnitOP.size_limit[0]-self.size[0]
                    self.y = self.pos[1]
                    self.unpressed = (0, 0)
                elif touch.y > UnitOP.size_limit[1]-self.size[1]:
                    self.x = self.pos[0]
                    self.y = UnitOP.size_limit[1]-self.size[1]
                else:
                    self.center_x = touch.x
                    self.center_y = touch.y
                #              if self.connect != 0:
                if self.connected == True:
                    self.line_move = self.line_move + 1

                return False
            return super(UnitOP, self).on_touch_move(touch)

        # def on_unpressed(self,instance,pos):
        #     if self.connect != 0:
        #         self.line_move = self.line_move + 1

        def on_multi_touch(self, instance, value):
            c = cPopUp()
            i = 0
            self.PropertyObj = []
            self.PropInput = []
            self.DropDowns = []
            self.MainButton = []
            c.ids.name_label.text_size = c.ids.name.size
            c.ids.name.text =  self.name
            for Property in self.PropertyList:
                PropLabel = Label(text=Property, size_hint_y=None, height=25, halign='left', valign='middle', font_size=14)
                PropLabel.text_size = PropLabel.size
                self.PropInput.append(TextInput(text = str(self.PropertyVal[i]),size_hint_y=None, height=25, valign='middle', font_size=12, multiline=False))
                self.PropertyObj.append(self.PropInput[i])
                c.ids.first_tab.add_widget(PropLabel)
                if self.check_stm == 0:
                    c.ids.first_tab.add_widget(self.PropInput[i])
                else:
                    self.MainButton.append(Button(text='Select', size_hint_y=None, height=25))
                    self.DropDowns.append(dDown(DrNumber=i))
                    for item in self.Operators:
                        btn = butt(text=item.name, size_hint_y=None, height=25, DrNumber=i,background_normal='',background_color=(0.4,0.4,0.4,1))
                        btn.bind(on_release=lambda btn: self.DropDowns[btn.DrNumber].select(btn.text))
                        self.DropDowns[i].add_widget(btn)
                    self.MainButton[i].bind(on_release=self.DropDowns[i].open)
                    self.DropDowns[i].bind(on_select=lambda instance, x: setattr(self.MainButton[instance.DrNumber], 'text', x))
                    c.ids.first_tab.add_widget(self.MainButton[i])
                i = i+1
                c.ids.submit.bind(on_press=self.on_submit)
            c.open()

        def open_prop(self,instance):
                self.PropInput = []
                print 'yes'
                i = 0
                for p in self.PropertyVal:
                    self.PropInput.append(TextInput(text = str(p),size_hint_y=None, height=25, valign='middle', font_size=12, multiline=False))
                    print p
                    i = i + 1

        def scroll_change(self, scrlv, instance, value):
            scrlv.scroll_y = value

        def slider_change(self, s, instance, value):
            if value >= 0:
                # this to avoid 'maximum recursion depth exceeded' error
                s.value = value

        def on_submit(self, instance):
            self.PropertyVal = []
            self.PropertyObj = self.PropInput
            for Property in self.PropertyObj:
                self.PropertyVal.append(Property.text)
            if self.connected == False:
                self.connect = self.connect + 1
