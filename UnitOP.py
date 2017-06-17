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
from kivy.factory import Factory
Builder.load_file('popup.kv')

class cPopUp(Popup):
    pass
class dDown(DropDown):
    DrNumber = NumericProperty(0)

class butt(Button):
    DrNumber = NumericProperty(0)

class UnitOPM(Factory.CustButton):
    def __init__(self, **kwargs):
        super(UnitOPM, self).__init__(**kwargs)
        self.child = Button()

    def on_touch_down(self, touch):
        if self.child.collide_point(*touch.pos):
            if touch.is_double_tap:
                # touch.multitouch_sim = True
                self.child.multi_touch = self.child.multi_touch + 1
            else:
                touch.grab(self)
        return False

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            # self.unpressed = touch.pos
            touch.ungrab(self)
        return True

    def on_touch_move(self, touch):
        if touch.grab_current is self:
            self.center_x = touch.x
            self.center_y = touch.y
            if self.child.connected == True:
                self.child.line_move = self.child.line_move + 1
            return False
        return super(UnitOPM, self).on_touch_move(touch)

class UnitOP(Button):
        Operators = []
        all_operators = []
        drop_connections = {}
        size_limit = [100, 100]
        unpressed = ListProperty([0, 0])
        double_tap = NumericProperty(0)
        multi_touch = NumericProperty(0)
        current_touch = None
        line_move = NumericProperty(0)
        connect = NumericProperty(0)
        compound_elements = []


        def __init__(self, **kwargs):
            super(UnitOP, self).__init__(**kwargs)
            self.stream_count = []
            self.input_streams = {}
            self.output_streams = {}
            self.input_lines = {}
            self.output_lines = {}
            self.connected = False
            self.PropertyListInput = []
            self.PropertyListOutput = []
            self.PropertyObj = []
            self.OM_Model = ''
            self.name = ''
            self.PropInput = []
            self.conn_point_input = 0
            self.conn_point_output = 0
            self.check_stm = 1
            self.DropDownsInput =[]
            self.MainButtonInput = []
            self.DropDownsOutput = []
            self.MainButtonOutput = []
            self.name_ob = TextInput()
            self.bef_name = ''
            self.text_label = Label()

        def on_multi_touch(self, instance, value):
            c = cPopUp()
            i = 0
            self.PropertyObj = []
            self.PropInput = []
            self.DropDownsInput = []
            self.MainButtonInput = []
            self.DropDownsOutput = []
            self.MainButtonOutput = []
            c.ids.name_label.text_size = c.ids.name.size
            self.bef_name = self.name
            c.ids.name.text = self.name
            self.name_ob = c.ids.name
            i=0
            if self.check_stm == 0:
                for Property in self.PropertyList:
                    PropLabel = Label(text=Property, size_hint_y=None, height=25, halign='left', valign='middle',font_size=14)
                    PropLabel.text_size = PropLabel.size
                    c.ids.first_tab.add_widget(PropLabel)
                    self.PropInput.append(TextInput(text=str(self.PropertyVal[i]), size_hint_y=None, height=25, valign='middle',font_size=12, multiline=False))
                    self.PropertyObj.append(self.PropInput[i])
                    c.ids.first_tab.add_widget(self.PropInput[i])
                    i=i+1
            for comp in self.compound_elements:
                c.ids.compound_col_1.add_widget(Label(text=comp,size_hint_x=1, size_hint_y=None, font_size=12,size=(0, 20)))
                c.ids.compound_col_2.add_widget(TextInput(text="1.0000", size_hint_y=None, font_size=8, size=(0, 20)))
            for Property in self.PropertyListInput:
                PropLabel = Label(text=Property, size_hint_y=None, height=25, halign='left', valign='middle', font_size=14)
                PropLabel.text_size = PropLabel.size
                c.ids.first_tab.add_widget(PropLabel)
                if self.check_stm == 0:
                    self.PropInput.append(TextInput(text=str(self.PropertyVal[i]), size_hint_y=None, height=25, valign='middle',font_size=12, multiline=False))
                    self.PropertyObj.append(self.PropInput[i])
                    c.ids.first_tab.add_widget(self.PropInput[i])
                else:
                    self.MainButtonInput.append(Button(text='Select', size_hint_y=None, height=25))
                    if self.input_streams[i + 1]:
                        self.MainButtonInput[len(self.MainButtonInput)-1].text = self.input_streams[i+1].name
                    self.DropDownsInput.append(dDown(DrNumber=i))
                    btn = butt(text='Select', size_hint_y=None, height=25, DrNumber=i, background_normal='',background_color=(0.4, 0.4, 0.4, 1))
                    btn.bind(on_release=lambda btn: self.DropDownsInput[btn.DrNumber].select(btn.text))
                    self.DropDownsInput[i].add_widget(btn)
                    for item in self.Operators:
                        btn = butt(text=item.name, size_hint_y=None, height=25, DrNumber=i,background_normal='',background_color=(0.4,0.4,0.4,1))
                        btn.bind(on_release=lambda btn: self.DropDownsInput[btn.DrNumber].select(btn.text))
                        self.DropDownsInput[i].add_widget(btn)
                    self.MainButtonInput[i].bind(on_release=self.DropDownsInput[i].open)
                    self.DropDownsInput[i].bind(on_select=lambda instance, x: setattr(self.MainButtonInput[instance.DrNumber], 'text', x))
                    c.ids.first_tab.add_widget(self.MainButtonInput[i])
                i = i+1
            i = 0
            for Property in self.PropertyListOutput:
                PropLabel = Label(text=Property, size_hint_y=None, height=25, halign='left', valign='middle',
                                  font_size=14)
                PropLabel.text_size = PropLabel.size
                self.PropInput.append(
                    TextInput(text=str(self.PropertyVal[i]), size_hint_y=None, height=25, valign='middle', font_size=12,
                              multiline=False))
                self.PropertyObj.append(self.PropInput[i])
                c.ids.first_tab.add_widget(PropLabel)
                if self.check_stm == 0:
                    c.ids.first_tab.add_widget(self.PropInput[i])
                else:
                    self.MainButtonOutput.append(Button(text='Select', size_hint_y=None, height=25))
                    if self.output_streams[i + 1]:
                        self.MainButtonOutput[len(self.MainButtonOutput) - 1].text = self.output_streams[i + 1].name
                    self.DropDownsOutput.append(dDown(DrNumber=i))
                    btn = butt(text='Select', size_hint_y=None, height=25, DrNumber=i, background_normal='',background_color=(0.4, 0.4, 0.4, 1))
                    btn.bind(on_release=lambda btn: self.DropDownsOutput[btn.DrNumber].select(btn.text))
                    self.DropDownsOutput[i].add_widget(btn)
                    for item in self.Operators:
                        btn = butt(text=item.name, size_hint_y=None, height=25, DrNumber=i, background_normal='',
                                   background_color=(0.4, 0.4, 0.4, 1))
                        btn.bind(on_release=lambda btn: self.DropDownsOutput[btn.DrNumber].select(btn.text))
                        self.DropDownsOutput[i].add_widget(btn)
                    self.MainButtonOutput[i].bind(on_release=self.DropDownsOutput[i].open)
                    self.DropDownsOutput[i].bind(on_select=lambda instance, x: setattr(self.MainButtonOutput[instance.DrNumber], 'text', x))
                    c.ids.first_tab.add_widget(self.MainButtonOutput[i])
                i = i + 1
            c.ids.submit.bind(on_press=self.on_submit)
            c.open()

        def open_prop(self, instance):
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
            self.name = self.name_ob.text
            UnitOP.UnitOP.drop_connections[self.name] = UnitOP.UnitOP.drop_connections[self.bef_name]
            for Property in self.PropertyObj:
                self.PropertyVal.append(Property.text)
            # if self.connected == False:
            self.connect = self.connect + 1
