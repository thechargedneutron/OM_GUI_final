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
from kivy.uix.modalview import ModalView
Builder.load_file('popup.kv')

class PropInputLabel(Label):
    pass

class PropInputTextInput(TextInput):
    pass

class c1PopUp(ModalView):
    pass

class Select_Button(Button):
    pass

class c2PopUp(ModalView):
    pass
class dDown(DropDown):
    DrNumber = NumericProperty(0)

class butt(Button):
    DrNumber = NumericProperty(0)
    border = 0,0,0,0

class UnitOPM(Factory.CustButton):
    def __init__(self, **kwargs):
        super(UnitOPM, self).__init__(**kwargs)
        self.child = Button()

    # def on_touch_down(self, touch):
    #     if self.child.collide_point(*touch.pos):
    #
    #         if touch.is_double_tap:
    #             # touch.multitouch_sim = True
    #             self.child.multi_touch = self.child.multi_touch + 1
    #         else:
    #             touch.grab(self)
    #
    #     return False
    #
    # def on_touch_up(self, touch):
    #     if touch.grab_current is self:
    #         # self.unpressed = touch.pos
    #         touch.ungrab(self)
    #     return True
    #
    # def on_touch_move(self, touch):
    #     if touch.grab_current is self:
    #         self.center_x = touch.x
    #         self.center_y = touch.y
    #         if self.child.connected == True:
    #             self.child.line_move = self.child.line_move + 1
    #         return False
    #     return super(UnitOPM, self).on_touch_move(touch)

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
            self.type = -1;
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
            self.PropLabelStreams = []
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
            self.updated_input_operators = []
            self.updated_output_operators = []
            self.flash_spec = []
            self.c = []
            self.upward_connector_input = []
            self.downward_connector_input = []
            self.upward_connector_output = []
            self.downward_connector_output = []
            self.compound_amounts = []
            self.compound_input_molar = []
            self.compound_input_mass = []

        def on_multi_touch(self, instance, value):
            self.c = c1PopUp()
            if self.check_stm == 0:
                self.c = c2PopUp()
            self.PropertyObj = []
            self.PropInput = []
            self.DropDownsInput = []
            self.MainButtonInput = []
            self.DropDownsOutput = []
            self.MainButtonOutput = []
            self.c.ids.name_label.text_size = self.c.ids.name.size
            self.bef_name = self.name
            self.c.ids.name.text = self.name
            self.name_ob = self.c.ids.name
            i=0
            self.updated_input_operators = []
            self.updated_output_operators = []

            if self.check_stm == 0:
                self.PropLabelStreams = []
                self.compound_amounts.append([])
                self.compound_amounts.append([])
                for Property in self.PropertyList:
                    self.PropLabelStreams.append(PropInputLabel(text=Property))
                    self.c.ids.first_tab.add_widget(self.PropLabelStreams[i])
                    self.PropInput.append(TextInput(text=str(self.PropertyVal[i]), size_hint_y=None, height=25, valign='middle',font_size=12, multiline=False))
                    self.PropertyObj.append(self.PropInput[i])
                    self.c.ids.first_tab.add_widget(self.PropInput[i])
                    i=i+1
                i=0
                for comp in self.compound_elements:

                    # self.c.ids.compound_col_1.add_widget(Label(text=comp,size_hint_x=1, size_hint_y=None, font_size=12,size=(0, 20)))
                    # self.c.ids.compound_col_2.add_widget(TextInput(text="1.0000", size_hint_y=None, font_size=8, size=(0, 20)))
                    self.c.ids.composition_compound.add_widget(PropInputLabel(text=comp))
                    self.compound_amounts[0].append('0')
                    self.compound_amounts[1].append('0')
                    self.compound_input_molar.append(PropInputTextInput(text=self.compound_amounts[0][i]))
                    self.compound_input_mass.append(PropInputTextInput(text=self.compound_amounts[1][i]))
                    self.c.ids.composition_amount.add_widget(PropInputTextInput(text=self.compound_amounts[0][i]))
                    i += 1
                self.PropLabelStreams[4].color = (0.3,0.3,0.3,1)
                self.PropInput[4].readonly = True
                self.PropInput[4].cursor_blink = True

            i=0
            for Property in self.PropertyListInput:
                PropLabel = PropInputLabel(text=Property)
                self.c.ids.first_tab.add_widget(PropLabel)
                if self.check_stm != 0:
                    self.MainButtonInput.append(Select_Button(text='None', size_hint_y=None, height=25))
                    if self.input_streams[i + 1]:
                        self.MainButtonInput[len(self.MainButtonInput)-1].text = self.input_streams[i+1].name
                    self.DropDownsInput.append(dDown(DrNumber=i))
                    # btn = butt(text='Select', size_hint_y=None, height=25, DrNumber=i, background_normal='',background_color=(0.4, 0.4, 0.4, 1))
                    # btn.bind(on_release=lambda btn: self.DropDownsInput[btn.DrNumber].select(btn.text))
                    # self.DropDownsInput[i].add_widget(btn)
                    # for item in self.Operators:
                    #     btn = butt(text=item.name, size_hint_y=None, height=25, DrNumber=i,background_normal='',background_color=(0.4,0.4,0.4,1))
                    #     btn.bind(on_release=lambda btn: self.DropDownsInput[btn.DrNumber].select(btn.text))
                    #     self.DropDownsInput[i].add_widget(btn)
                    # self.MainButtonInput[i].bind(on_release=self.DropDownsInput[i].open)
                    self.MainButtonInput[i].bind(on_release=self.generate_dp_input)
                    self.DropDownsInput[i].bind(on_select=lambda instance, x: setattr(self.MainButtonInput[instance.DrNumber], 'text', x))
                    self.c.ids.first_tab.add_widget(self.MainButtonInput[i])
                i = i+1
            self.c.ids.first_tab.add_widget(Label(text="", size_hint_y=None,  height=25))
            self.c.ids.first_tab.add_widget(Label(text="", size_hint_y=None,height=25))
            i = 0
            for Property in self.PropertyListOutput:
                PropLabel = PropInputLabel(text=Property)
                self.c.ids.first_tab.add_widget(PropLabel)
                if self.check_stm != 0:
                    self.MainButtonOutput.append(Select_Button(text='None', size_hint_y=None, height=25))
                    if self.output_streams[i + 1]:
                        self.MainButtonOutput[len(self.MainButtonOutput) - 1].text = self.output_streams[i + 1].name
                    self.DropDownsOutput.append(dDown(DrNumber=i,auto_dismiss=True))
                    # btn = butt(text='Select', size_hint_y=None, height=25, DrNumber=i, background_normal='',background_color=(0.4, 0.4, 0.4, 1))
                    # btn.bind(on_release=lambda btn: self.DropDownsOutput[btn.DrNumber].select(btn.text))
                    # self.DropDownsOutput[i].add_widget(btn)
                    # for item in self.Operators:
                    #     btn = butt(text=item.name, size_hint_y=None, height=25, DrNumber=i, background_normal='',
                    #                background_color=(0.4, 0.4, 0.4, 1))
                    #     btn.bind(on_release=lambda btn: self.DropDownsOutput[btn.DrNumber].select(btn.text))
                    #     self.DropDownsOutput[i].add_widget(btn)
                    self.MainButtonOutput[i].bind(on_release=self.generate_dp_output)
                    self.DropDownsOutput[i].bind(on_select=lambda instance, x: setattr(self.MainButtonOutput[instance.DrNumber], 'text', x))
                    self.c.ids.first_tab.add_widget(self.MainButtonOutput[i])
                i = i + 1
            self.c.ids.submit.bind(on_press=self.on_submit)
            if self.check_stm == 0:
                self.c.ids.flash_spec.bind(on_press=self.show_flash_spec)
                self.c.ids.compound_spec.bind(on_press=self.show_compound_spec)
            for operator in self.Operators:
                if not operator.output_streams[1]:
                    self.updated_input_operators.append(operator)
                else:
                    for k in self.MainButtonInput:
                        if operator.name == k.text:
                            self.updated_input_operators.append(operator)

            for operator in self.Operators:
                if not operator.input_streams[1]:
                    self.updated_output_operators.append(operator)
                else:
                    for k in self.MainButtonOutput:
                        if operator.name == k.text:
                            self.updated_output_operators.append(operator)

            self.c.open()



        def show_flash_spec(self,instance):
            dr = DropDown()
            dr.bind(on_select=self.select_flash_spec)
            for i in self.flash_spec:
                if i != instance.text:
                    btn = butt(text=i, size_hint_y=None, height=25, background_normal='',
                               background_color=(0.4, 0.4, 0.4, 1),font_size=12)
                    btn.bind(on_release=lambda btn: dr.select(btn.text))
                    dr.add_widget(btn)
            dr.open(instance)

        def select_flash_spec(self, instance, text):
            self.c.ids.flash_spec.text = text
            for i in self.PropInput:
                i.readonly = False
            for i in self.PropLabelStreams:
                i.color = (0,0,0,1)
            if(text == "T and P"):
                self.PropLabelStreams[4].color = (0.3, 0.3, 0.3, 1)
                self.PropInput[4].readonly = True
            elif(text == "T and Vapor Fraction"):
                self.PropLabelStreams[1].color = (0.3, 0.3, 0.3, 1)
                self.PropInput[1].readonly = True
            elif (text == "P and Vapor Fraction"):
                self.PropLabelStreams[0].color = (0.3, 0.3, 0.3, 1)
                self.PropInput[0].readonly = True

        def show_compound_spec(self, instance):
            dr = DropDown()
            dr.bind(on_select=self.select_compound_spec)
            for i in self.compound_spec:
                btn = butt(text=i, size_hint_y=None, height=25, background_normal='',
                           background_color=(0.4, 0.4, 0.4, 1), font_size=12)
                btn.bind(on_release=lambda btn: dr.select(btn.text))
                dr.add_widget(btn)
            dr.open(instance)

        def select_compound_spec(self, instance, text):
            self.c.ids.compound_spec.text = text
            self.c.ids.composition_amount.clear_widgets()
            i=0
            while i < len(self.compound_input_molar):
                if text == "Molar Fractions":
                    self.c.ids.composition_amount.add_widget(self.compound_input_molar[i])
                else:
                    self.c.ids.composition_amount.add_widget(self.compound_input_mass[i])
                i += 1


        def generate_dp_input(self,instance):

            i = self.MainButtonInput.index(instance)
            self.DropDownsInput[i].clear_widgets()
            if instance.text != 'None':
                btn = butt(text='None', size_hint_y=None, height=25, DrNumber=i, background_normal='',
                           background_color=(0.4, 0.4, 0.4, 1))
                btn.bind(on_release=lambda btn: self.DropDownsInput[btn.DrNumber].select(btn.text))
                self.DropDownsInput[i].add_widget(btn)
            for item in self.updated_input_operators:
                insert = True
                for button in self.MainButtonInput:
                    if item.name == button.text:
                        insert = False
                if insert:
                    btn = butt(text=item.name, size_hint_y=None, height=25, DrNumber=i, background_normal='',
                               background_color=(0.4, 0.4, 0.4, 1))
                    btn.bind(on_release=lambda btn: self.DropDownsInput[btn.DrNumber].select(btn.text))
                    self.DropDownsInput[i].add_widget(btn)
            # self.MainButtonInput[i].bind(on_release=self.DropDownsInput[i].open)
            self.DropDownsInput[i].bind(on_select=lambda instance, x: setattr(self.MainButtonInput[instance.DrNumber],

                                                                               'text', x))
            self.DropDownsInput[i].open(instance)

        def generate_dp_output(self, instance):

            i = self.MainButtonOutput.index(instance)
            self.DropDownsOutput[i].clear_widgets()
            if instance.text != 'None':
                btn = butt(text='None', size_hint_y=None, height=25, DrNumber=i, background_normal='',
                       background_color=(0.4, 0.4, 0.4, 1))
                btn.bind(on_release=lambda btn: self.DropDownsOutput[btn.DrNumber].select(btn.text))
                self.DropDownsOutput[i].add_widget(btn)
            for item in self.updated_output_operators:
                insert = True
                for button in self.MainButtonOutput:
                    if item.name == button.text:
                        insert = False
                if insert:
                    btn = butt(text=item.name, size_hint_y=None, height=25, DrNumber=i, background_normal='',
                               background_color=(0.4, 0.4, 0.4, 1))
                    btn.bind(on_release=lambda btn: self.DropDownsOutput[btn.DrNumber].select(btn.text))
                    self.DropDownsOutput[i].add_widget(btn)
            # self.MainButtonInput[i].bind(on_release=self.DropDownsInput[i].open)
            self.DropDownsOutput[i].bind(on_select=lambda instance, x: setattr(self.MainButtonOutput[instance.DrNumber],
                                                                              'text', x))
            self.DropDownsOutput[i].open(instance)

        def open_prop(self, instance):
                self.PropInput = []

                i = 0
                for p in self.PropertyVal:
                    self.PropInput.append(TextInput(text = str(p),size_hint_y=None, height=25, valign='middle', font_size=12, multiline=False))

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
