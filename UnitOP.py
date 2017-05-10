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


class UnitOP(Button):


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



        def on_touch_down(self, touch):
            if self.collide_point(*touch.pos):
                if 'multitouch_sim' in touch.profile:
                    touch.multitouch_sim = True
                    self.multi_touch = self.multi_touch + 1
                else:
                    touch.grab(self)
            return False

        def on_touch_up(self, touch):
            if touch.grab_current is self:
                if self.x > 382:
                    self.pos = (0, 0)
                    self.unpressed = (0, 0)
                else:
                    self.unpressed = touch.pos
                touch.ungrab(self)
            return True


        def on_touch_move(self, touch):
            if touch.grab_current is self:
                self.x = touch.x - .1
                self.y = touch.y - .1
                #              if self.connect != 0:
                if self.connected == True:
                    self.line_move = self.line_move + 1

                return False
            return super(UnitOP, self).on_touch_move(touch)

        # def on_unpressed(self,instance,pos):
        #     if self.connect != 0:
        #         self.line_move = self.line_move + 1

        def on_multi_touch(self, instance, value):
            prop = Popup(title="Properties", size_hint=(0.3, 1), auto_dismiss=True, pos_hint={'right': 0.3, 'top': 1})
            # prop.bind(on_open=self.open_prop)
            layout1 = StackLayout(orientation='lr-tb')
            layout4 = GridLayout(cols=1)
            submit = Button(text='Submit')
            submit.bind(on_press=self.on_submit)
            scrlv = ScrollView(size_hint=(1, 0.5))
            s = Slider(min=0, max=1, value=25, orientation='vertical', step=0.01, size_hint=(2, 0.5))
            scrlv.bind(scroll_y=partial(self.slider_change, s))
            s.bind(value=partial(self.scroll_change, scrlv))
            layout2 = GridLayout(cols=2, size_hint_y=None)
            layout2.bind(minimum_height=layout2.setter('height'))
            i = 0
            self.PropertyObj = []
            self.PropInput = []
            for Property in self.PropertyList:
                PropLabel = Label(text=Property, size_hint_y=None, height=25, valign='middle', font_size=14)
                PropLabel.text_size = (PropLabel.size)
                self.PropInput.append(TextInput(text = str(self.PropertyVal[i]),size_hint_y=None, height=25, valign='middle', font_size=12, multiline=False))
                self.PropertyObj.append(self.PropInput[i])
                layout2.add_widget(PropLabel)
                layout2.add_widget(self.PropInput[i])
                i = i+1
            layout4.add_widget(layout2)
            layout4.add_widget(submit)
            scrlv.add_widget(layout4)
            layout1.add_widget(scrlv)
            layout1.add_widget(s)
            prop.content = layout1
            prop.open()


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
