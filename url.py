from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty
from kivy.properties import NumericProperty
from kivy.graphics.vertex_instructions import Rectangle
from kivy.graphics.vertex_instructions import Line
from kivy.uix.bubble import Bubble,BubbleButton
from kivy.uix.popup import Popup
from kivy.uix.modalview import ModalView
from functools import partial
from kivy.properties import ObjectProperty
from kivy.uix.scrollview import ScrollView
from kivy.uix.slider import Slider
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics.context_instructions import Color
from kivy.graphics.instructions import InstructionGroup
from kivy.uix.actionbar import ActionBar
from kivy.uix.actionbar import ActionView
from kivy.uix.actionbar import ActionButton
from kivy.uix.actionbar import ActionPrevious
from kivy.uix.dropdown import DropDown
from kivy.uix.progressbar import ProgressBar
from kivy.lang import Builder
from kivy.lang import Builder
from textwrap import dedent
from kivy.garden.graph import Graph, MeshLinePlot
from math import sin
import CORBA
import os
import random
import StaticUO
from OMPython import OMCSession
import UnitOP
from Error import Error

Thermodynamic_models = ['Peng-Robinson','SRK','NRTL','UNIQUAC']
# File_options = ['New Steady-state Simulation','Open','Save','Save As','Close Active Simulation','Exit Openmodellica']
File_options = ['open','save']
Edit_options = ['Undo','Redo','Cut Selected Objects','Copy Selected Objects','Paste Objects','Remove selected objects','Clone selected objects','Recalculate object','Export data to Clipboard','Simulation settings','General settings']
Insert_options = ['Flowsheet Object','Property Table','Master Property Table','Linked Spreadsheet Table','Image','Text','Rectangle']
Tools_options = ['Petroleum Characterization (Bulk C7+)','Petroleum Characterization (Distillation Curves)','Petroleum Array Manager','Reactions Manager','Pure Compound Property Viewer/Editor','User Database Manager','CAPE-OPEN Component Registration' ]
Utilities_options = ['Binary Plotter']
Optimization_options = ['Sensitivity Analysis','Multivariate Optimizer']
Scripts_options = ['Script Manager']
Results_options = ['Create Report']
Plugins_options = ['CAPE-OPEN Plugins','Natural Gas Properties']
Windows_options = ['Set Canvas Size']
View_options = ['Show Toolstrip','Console Output','calculation Queue','Watch panel','CAPE-OPEN Objects Reports','Flowsheet Toolstrip','Unit Systems Toolstrip',"Restore Docking Panels' Layout",'Close Opened Object Editors']
Help_options = ['Show Help','Documention','Openmodellica on the web','Donate!','About OpenModellica']

class MenuButton(Button):
    pass

class CompButton(Button):
    pass

class Remove_Bubble(Bubble):
    pass

class SPopUp(Popup):
    pass

class SSPopUp(ModalView):
    pass

class UtilityPopUp(ModalView):
    pass

class BinaryEnvelope(ModalView):
    pass

class CompPop(ModalView):
    pass

class ThermoPop(ModalView):
    pass

class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

class ResizePop(ModalView):
    pass

class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)


class MyTextInput(TextInput):

    def __init__(self, **kw):
        self.drop_down = DropDown(dismiss_on_select=True)
        self.drop_down.bind(on_select=self.on_select)
        super(MyTextInput, self).__init__(**kw)

    def on_select(self, *args):
        self.text = args[1]

    def on_touch_up(self, touch):
        if touch.grab_current == self:
            self.drop_down.open(self)
        return super(MyTextInput, self).on_touch_up(touch)

class OmWidget(FloatLayout):
    lines = {}
    Unit_Operations = []
    Unit_Operations_Labels = []
    data = []
    loadfile = ObjectProperty(None)
    savefile = ObjectProperty(None)
    text_input = ObjectProperty(None)

    word_list = []
    def __init__(self,**kwargs):
        super(OmWidget,self).__init__(**kwargs)


        fo = open("compounds.txt", "r+")
        self.error_popup = Error()
        self.error = self.error_popup.ids.error_message
        self.compo = ""
        self.plot = None
        self.utility_pop_up = ''
        self.binary_pop_up = ''
        self.rect= False
        self.rect_enable = True
        self.ids.scroll.do_scroll_x = False
        self.ids.scroll.do_scroll_y = False
        self.rect_start = []
        self.select_rect = ''
        self.Selected_Unit_Operations = []
        self.grab_w = ''
        self.select_box = InstructionGroup()
        self.tp = DropDown()
        self.resize_popup = ''
        self.current_grab_unit = None

        self.word_list = fo.read().splitlines()
        self.addedcomp = []
        self.comp_dropdown = DropDown()
        self.dropdown = DropDown()
        self.op_count = 1
        self.Selected_thermo_model = 'No Model Selected'
        self.data.append('model Flowsheet\n')
        self.multiselect = False;
        UnitOP.UnitOP.size_limit = self.ids.b1.size
        self.ids.hand_toggle.background_color = 0.5, 0.5, 0.5, 1
        self.ids.cursor_toggle.background_color = 1, 1, 1, 1
        self.filedropdown = DropDown(auto_width=False, width=300)
        # for model in File_options:
        #     btn = MenuButton(text=model, width=300)
        #     btn.text_size = btn.size
        #     self.filedropdown.add_widget(btn)
        btn = MenuButton(text="Open", width=300, on_press=self.show_load)
        btn.text_size = btn.size
        self.filedropdown.add_widget(btn)


        btn2 = MenuButton(text="Save as",width=300, on_press=self.show_save)
        btn2.text_size = btn2.size
        self.filedropdown.add_widget(btn2)

        self.editdropdown = DropDown(auto_width=False, width=300)
        for model in Edit_options:
            btn = MenuButton(text=model, width=200)
            btn.text_size = btn.size
            self.editdropdown.add_widget(btn)

        self.insertdropdown = DropDown(auto_width=False, width=300)
        for model in Insert_options:
            btn = MenuButton(text=model, width=200)
            btn.text_size = btn.size
            self.insertdropdown.add_widget(btn)

        self.toolsdropdown = DropDown(auto_width=False, width=400)
        for model in Tools_options:
            btn = MenuButton(text=model, width=350)
            btn.text_size = btn.size
            self.toolsdropdown.add_widget(btn)

        self.utilitiesdropdown = DropDown(auto_width=False, width=300)
        for model in Utilities_options:
            btn = MenuButton(text=model, width=100, on_press=self.add_utility)
            btn.text_size = btn.size
            self.utilitiesdropdown.add_widget(btn)

        self.optimizationdropdown = DropDown(auto_width=False, width=300)
        for model in Optimization_options:
            btn = MenuButton(text=model, width=200)
            btn.text_size = btn.size
            self.optimizationdropdown.add_widget(btn)

        self.scriptsdropdown = DropDown(auto_width=False, width=300)
        for model in Scripts_options:
            btn = MenuButton(text=model, width=150)
            btn.text_size = btn.size
            self.scriptsdropdown.add_widget(btn)

        self.resultsdropdown = DropDown(auto_width=False, width=300)
        for model in Results_options:
            btn = MenuButton(text=model, width=150)
            btn.text_size = btn.size
            self.resultsdropdown.add_widget(btn)

        self.pluginsdropdown = DropDown(auto_width=False, width=300)
        for model in Plugins_options:
            btn = MenuButton(text=model, width=200)
            btn.text_size = btn.size
            self.pluginsdropdown.add_widget(btn)

        self.windowsdropdown = DropDown(auto_width=False, width=300)
        for model in Windows_options:
            btn = MenuButton(text=model, width=150, on_press=self.change_canvas_size_menu)
            btn.text_size = btn.size
            self.windowsdropdown.add_widget(btn)

        self.viewdropdown = DropDown(auto_width=False, width=300)
        for model in View_options:
            btn = MenuButton(text=model, width=250)
            btn.text_size = btn.size
            self.viewdropdown.add_widget(btn)

        self.helpdropdown = DropDown(auto_width=False, width=300)
        for model in Help_options:
            btn = MenuButton(text=model, width=200)
            btn.text_size = btn.size
            self.helpdropdown.add_widget(btn)
        print self.ids.mixer.pos;
        print self.ids.mat_strm.pos;
        print self.ids.flash.pos;
        print self.ids.splitter.pos;
        print self.ids.valve.pos;


    def change_canvas_size_menu(self,*args):
        self.resize_popup = ResizePop()
        self.resize_popup.ids.canvas_width.text = str(self.ids.b1.size[0])
        self.resize_popup.ids.canvas_height.text = str(self.ids.b1.size[1])
        self.resize_popup.ids.submit_size.bind(on_press=self.change_canvas_size)
        self.resize_popup.open()

    def change_canvas_size(self,*args):
        self.ids.b1.size = [float(self.resize_popup.ids.canvas_width.text),float(self.resize_popup.ids.canvas_height.text)]
        self.resize_popup.dismiss()



    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self,*args):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()


    def show_save(self,*args):
        content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
        self._popup = Popup(title="Save file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        fo = open(os.path.join(path, filename[0]), "r+")
        k = []
        for i in self.Unit_Operations_Labels:
            k.append(i)

        for i in k:
            self.unit_op = i
            self.remove_unit_op()

        self.unit_op = ''
        self.ids.b1.clear_widgets()
        self.ids.b1.canvas.clear()
        # ins = InstructionGroup()
        # ins.add(Color(0.9, 0.9, 0.9, 1))
        # ins.add(Rectangle(size=self.size,pos=self.pos))
        # self.ids.b1.canvas.add(ins)
        saved_unit_op = fo.read().splitlines()
        for i in saved_unit_op:
            up = i.split("^")

            pos = (float(up[2]), float(up[3]));
            if up[1] == '0':
                self.add_unit_op(pos, StaticUO.SMatStrm.UO(), 0, up[6])
            elif up[1] == '1':
                self.add_unit_op(pos, StaticUO.SMixer.UO(), 0, up[11])
            elif up[1] == '2':
                self.add_unit_op(pos, StaticUO.SFlash.UO(), 0, up[8])

        for i in saved_unit_op:
            up = i.split("^")
            if up[1] == '0':
                pass
            elif up[1] == '1':
                for i in range(4, 10):
                    up[0] = int(up[0])
                    if up[i] != '-1':
                        self.Unit_Operations[up[0]].input_streams[i - 3] = self.Unit_Operations[int(up[i])]
                    else:
                        self.Unit_Operations[up[0]].input_streams[i - 3] = None
                if up[10] != '-1':
                    self.Unit_Operations[up[0]].output_streams[1] = self.Unit_Operations[int(up[10])]
                else:
                    self.Unit_Operations[up[0]].output_streams[1] = None

                self.Unit_Operations_Labels[up[0]].child.Update_Conn_Pnts()
                self.Unit_Operations_Labels[up[0]].child.connect += 1

            elif up[1] == '2':
                for i in range(4, 6):
                    up[0] = int(up[0])
                    if up[i] != '-1':
                        self.Unit_Operations[up[0]].input_streams[i - 3] = self.Unit_Operations[int(up[i])]
                    else:
                        self.Unit_Operations[up[0]].input_streams[i - 3] = None
                for i in range(6, 8):
                    up[0] = int(up[0])
                    if up[i] != '-1':
                        self.Unit_Operations[up[0]].output_streams[i - 5] = self.Unit_Operations[int(up[i])]
                    else:
                        self.Unit_Operations[up[0]].output_streams[i - 5] = None

                self.Unit_Operations_Labels[up[0]].child.Update_Conn_Pnts()
                self.Unit_Operations_Labels[up[0]].child.connect += 1

        self.dismiss_popup()

    def save(self, path, filename):
        fo = open(os.path.join(path, filename), "wb")

        v = 0
        for i in self.Unit_Operations:
            fo.write(str(v) + "^")
            fo.write(str(i.type) + "^")
            fo.write(str(i.center[0]) + "^")
            fo.write(str(i.center[1]) + "^")
            for j in i.input_streams:
                if i.input_streams[j]:
                    fo.write(str(self.Unit_Operations.index(i.input_streams[j])) + "^")
                else:
                    fo.write("-1" + "^")
            for j in i.output_streams:
                if i.output_streams[j]:
                    fo.write(str(self.Unit_Operations.index(i.output_streams[j])) + "^")
                else:
                    fo.write("-1" + "^")
            fo.write(i.name)
            fo.write("\n")
            v = v + 1

        fo.close()

        self.dismiss_popup()




    def add_popup(self,*args):
        interval_down = DropDown()
        for i in self.addedcomp:
            btn = Button(text=i, size_hint_y=None, height=25, background_normal='',
                         background_color=(0.4, 0.4, 0.4, 1))
            btn.bind(on_release=lambda btn: interval_down.select(btn.text))
            interval_down.add_widget(btn)
        interval_down.bind(on_select=lambda instance, x: setattr(args[0], 'text', x))
        interval_down.open(args[0])

    def add_popup2(self, *args):
        interval_down = DropDown()
        for i in self.addedcomp:
            if i != self.binary_pop_up.ids.compound_1.text:
                btn = Button(text=i, size_hint_y=None, height=25, background_normal='',
                             background_color=(0.4, 0.4, 0.4, 1))
                btn.bind(on_release=lambda btn: interval_down.select(btn.text))
                interval_down.add_widget(btn)
        interval_down.bind(on_select=lambda instance, x: setattr(args[0], 'text', x))
        interval_down.open(args[0])

    def add_popup3(self, *args):
        models = ['Peng-Robinson', 'SRK', 'NRTL', 'UNIQUAC']
        interval_down = DropDown()
        for i in models:
            if i != args[0].text:
                btn = Button(text=i, size_hint_y=None, height=25, background_normal='',
                             background_color=(0.4, 0.4, 0.4, 1))
                btn.bind(on_release=lambda btn: interval_down.select(btn.text))
                interval_down.add_widget(btn)
        interval_down.bind(on_select=lambda instance, x: setattr(args[0], 'text', x))
        interval_down.open(args[0])

    def PropPack(self, *args):
        comp1 = self.binary_pop_up.ids.compound_1.text
        comp2 = self.binary_pop_up.ids.compound_2.text
        pressure = self.binary_pop_up.ids.Pressure.text
        model = self.binary_pop_up.ids.property_package.text
        with open('PropPack.mo', 'w') as txtfile:
            txtfile.write('model PropPack\n')
            txtfile.write('parameter Chemsep_Database.' + comp1 + ' C1;\n')
            txtfile.write('parameter Chemsep_Database.' + comp2 + ' C2;\n')
            txtfile.write('parameter Real Pressure = ' + pressure + ';\n')
            txtfile.write('extends Thermodynamic_Packages.bubblepnt;\n')
            txtfile.write('extends Thermodynamic_Packages.' + model + '(NOC = 2, Comp = {C1,C2}, P = Pressure);\n')
            txtfile.write('end PropPack;\n')
        omc = OMCSession()
        omc.sendExpression("loadFile(\"Chemsep_Database.mo\")")
        omc.sendExpression("loadFile(\"Thermodynamic_Functions.mo\")")
        omc.sendExpression("loadFile(\"Thermodynamic_Packages.mo\")")
        omc.sendExpression("loadFile(\"PropPack.mo\")")
        resultval = omc.sendExpression("simulate(PropPack, stopTime=1.0, numberOfIntervals=50)")
        if self.plot != None:
            self.binary_pop_up.ids.graph.remove_plot(self.plot)
            self.plot = None

        self.plot = MeshLinePlot(color=[1, 0, 0,1])
        plot_points = []
        i = 0.01

        max = -1000000
        min = 1000000
        while i < 1:
            val_r = str(omc.sendExpression("val(T," + str(i) + ")"))
            plot_points.append((i, float(val_r)))
            if float(val_r)>max:
                max =float(val_r)
            if float(val_r)<min:
                min = float(val_r)
            i += 0.02

        self.plot.points = plot_points
        graph = self.binary_pop_up.ids.graph
        graph.y_ticks_major = (max-min)/10
        graph.ymin = min-10
        graph.ymax = max+10
        graph.add_plot(self.plot)



    def add_utility(self,*args):
        self.binary_pop_up = BinaryEnvelope()

        interval = self.binary_pop_up.ids.compound_1
        interval.bind(on_release=self.add_popup)
        self.binary_pop_up.ids.compound_2.bind(on_release=self.add_popup2)
        self.binary_pop_up.ids.property_package.bind(on_release=self.add_popup3)
        self.binary_pop_up.open()
        self.binary_pop_up.ids.calculate.bind(on_release=self.PropPack)


    # def binary_envelope(self,*args):
    #     self.utility_pop_up.dismiss()
    #     self.binary_pop_up = BinaryEnvelope()
    #     self.binary_pop_up.open()

    def select_hand(self):
        self.ids.hand_toggle.background_color = 1, 1, 1, 1
        self.ids.cursor_toggle.background_color = 0.5, 0.5, 0.5, 1
        self.rect_enable = False
        self.ids.scroll.do_scroll_x = True
        self.ids.scroll.do_scroll_y = True

    def select_cursor(self):
        self.ids.hand_toggle.background_color = 0.5, 0.5, 0.5, 1
        self.ids.cursor_toggle.background_color = 1, 1, 1, 1
        self.ids.scroll.do_scroll_x = False
        self.ids.scroll.do_scroll_y = False
        self.rect_enable = True

    def compile(self, instance):
        #self.data = []
        self.data.append('equation\n')
        for unit in self.Unit_Operations:
            if unit.OM_Model == 'Mat_Stm':
                count = 0
                for Prop in unit.PropertyVal:
                    if Prop != '':
                        self.data.append(unit.name + '.' + unit.PropertyList[count] + '=' + str(Prop) + ';\n')
                    count = count + 1


    def simulate(self,instance):

        self.SSP.dismiss()
        with open('Flowsheet.mo', 'w') as txtfile:
            for d in self.data:
                txtfile.write(d)
            txtfile.write('end Flowsheet;\n')
        SimStatus = SPopUp()
        SimStatus.bind(on_open=self.SimProgress)
        SimStatus.open()

    def select(self, *args):
        try:
            self.label.text = args[1][0]
        except:
            pass


    def SimProgress(self,instance):


        omc = OMCSession()
        omc.sendExpression("loadFile(\"test.mo\")")
        # instance.ids.ProgBar.value = 75
        # instance.ids.status.text = 'Compiling'
        omc.sendExpression("loadFile(\"Flowsheet.mo\")")
        # instance.ids.ProgBar.value = 85
        # instance.ids.status.text = 'Simulating'
        chek = omc.sendExpression("simulate(Flowsheet, stopTime=1.0)")


        # print chek
        for unit in self.Unit_Operations:

            if 'Mat_Stm' in unit.name:
                print 'yes'
                unit.PropertyVal = []
                for prop in unit.PropertyList:
                    resultstr = unit.name + '.' + prop
                    print resultstr
                    resultval = str(omc.sendExpression("val("+resultstr+", 0.5)"))
                    print resultval
                    unit.PropertyVal.append(resultval)
        # instance.ids.ProgBar.value = 100
        # instance.ids.status.text = 'Completed Successfully'


        instance.dismiss()

    def SimulationSettings(self, instance):
        self.SSP = SSPopUp()
        self.SSP.ids.Sim_But.bind(on_press=self.simulate)
        values1 = ["Number of Intervals", "Interval"]
        values2 = ["euler", "rungekutta", " dassl", "optimization", "radau5", "radau3", "impeuler", "trapezoid",
                   "lobatto4", "lobatto6", "symEuler", "symEulerSsc", "heun", "ida", "rungekutta_ssc", " qss "]
        values3 = ["coloured Num", "internationalNumerical", "colouredSymbolical", "numerical", "symbolical",
                   "kluSparse"]
        values4 = ["mat", "plt", "csv"]
        interval = self.SSP.ids.interval_type
        interval_down = DropDown()
        for i in values1:
            btn = Button(text=i, size_hint_y=None, height=25, background_normal='',
                         background_color=(0.4, 0.4, 0.4, 1))
            btn.bind(on_release=lambda btn: interval_down.select(btn.text))
            interval_down.add_widget(btn)
        interval_down.bind(on_select=lambda instance, x: setattr(interval, 'text', x))
        interval.bind(on_release=interval_down.open)

        method = self.SSP.ids.method
        method_down = DropDown()
        for i in values2:
            btn = Button(text=i, size_hint_y=None, height=25, background_normal='',
                         background_color=(0.4, 0.4, 0.4, 1))
            btn.bind(on_release=lambda btn: method_down.select(btn.text))
            method_down.add_widget(btn)
        method_down.bind(on_select=lambda instance, x: setattr(method, 'text', x))
        method.bind(on_release=method_down.open)

        output = self.SSP.ids.output
        output_down = DropDown()
        for i in values3:
            btn = Button(text=i, size_hint_y=None, height=25, background_normal='',
                         background_color=(0.4, 0.4, 0.4, 1))
            btn.bind(on_release=lambda btn: output_down.select(btn.text))
            output_down.add_widget(btn)
        output_down.bind(on_select=lambda instance, x: setattr(output, 'text', x))
        output.bind(on_release=output_down.open)

        output2 = self.SSP.ids.output2
        output2_down = DropDown()
        for i in values4:
            btn = Button(text=i, size_hint_y=None, height=25, background_normal='',
                         background_color=(0.4, 0.4, 0.4, 1))
            btn.bind(on_release=lambda btn: output2_down.select(btn.text))
            output2_down.add_widget(btn)
        output2_down.bind(on_select=lambda instance, x: setattr(output2, 'text', x))
        output2.bind(on_release=output2_down.open)

        self.SSP.open()



    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            k = True
            if 'multitouch_sim' not in touch.profile and not self.current_grab_unit:
                for i in self.Unit_Operations_Labels:
                    if i.collide_point(*self.compute_relative_position(touch)):
                        if touch.is_double_tap:
                            i.child.multi_touch += 1
                        else:
                            self.current_grab_unit = i;
            if 'multitouch_sim' not in touch.profile:
                for i in self.Unit_Operations_Labels:
                    i.canvas.before.clear()
            for i in self.Unit_Operations_Labels:
                if i.collide_point(*self.compute_relative_position(touch)):
                    k = False
            if self.select_rect != '':
                self.ids.b1.canvas.remove(self.select_rect)
            if 'multitouch_sim' not in touch.profile and not touch.grab_current == self:
                if self.ids.mixer.collide_point(*self.compute_relative_position3(touch)):
                    self.grab_w = StaticUO.SMixer()
                    self.add_widget(self.grab_w)
                    self.grab_w.center = touch.pos
                    touch.grab(self)
                elif self.ids.mat_strm.collide_point(*self.compute_relative_position3(touch)):
                    self.grab_w = StaticUO.SMatStrm()
                    self.add_widget(self.grab_w)
                    self.grab_w.center = touch.pos
                    touch.grab(self)
                elif self.ids.flash.collide_point(*self.compute_relative_position3(touch)):
                    self.grab_w = StaticUO.SFlash()
                    self.add_widget(self.grab_w)
                    self.grab_w.center = touch.pos
                    touch.grab(self)
                elif self.ids.splitter.collide_point(*self.compute_relative_position3(touch)):
                    self.grab_w = StaticUO.SSplitter()
                    self.add_widget(self.grab_w)
                    self.grab_w.center = touch.pos
                    touch.grab(self)
                elif self.ids.valve.collide_point(*self.compute_relative_position3(touch)):
                    self.grab_w = StaticUO.SValve()
                    self.add_widget(self.grab_w)
                    self.grab_w.center = touch.pos
                    touch.grab(self)
            if self.ids.b1.collide_point(*self.compute_relative_position(touch)) and k and not self.ids.unit_shelf.collide_point(*self.compute_relative_position3(touch)):
                touch.grab(self)
                self.rect = True
                self.rect_start = self.compute_relative_position(touch)

            if hasattr(self, 'bubb'):
                if not (self.bubb.collide_point(*self.compute_relative_position(touch))):
                    self.ids.b1.remove_widget(self.bubb)

            UnitOP.UnitOP.size_limit = self.ids.b1.size
            touch_pos = self.compute_relative_position(touch)
            for i in self.Unit_Operations_Labels:
                if i.collide_point(*self.compute_relative_position(touch)) and not self.ids.unit_shelf.collide_point(*self.compute_relative_position3(touch)):
                    if 'multitouch_sim' in touch.profile:
                        self.unit_op = i
                        self.bubb = Remove_Bubble()
                        self.bubb.arrow_pos = 'bottom_mid'
                        self.bubb.pos = (touch_pos[0] - self.bubb.size[0]/2,touch_pos[1])
                        self.bubb.add_widget(BubbleButton(text="Remove",on_press=self.remove_function))
                        self.ids.b1.add_widget(self.bubb)
        return super(OmWidget, self).on_touch_down(touch)

    def on_touch_move(self, touch, *args):
        if self.current_grab_unit:
            r_touch = self.compute_relative_position(touch);
            offset_x_r = self.ids.scroll.size[0]+ (self.ids.b1.size[0]-self.ids.scroll.size[0])*self.ids.scroll.scroll_x - (self.current_grab_unit.child.size[0]/2)
            offset_x_l = (self.ids.b1.size[0] - self.ids.scroll.size[0]) * self.ids.scroll.scroll_x + (self.current_grab_unit.child.size[0] / 2)
            offset_y_t = self.ids.scroll.size[1]+ (self.ids.b1.size[1]-self.ids.scroll.size[1])*self.ids.scroll.scroll_y - (self.current_grab_unit.child.size[1]/2)
            offset_y_b = (self.ids.b1.size[1] - self.ids.scroll.size[1]) * self.ids.scroll.scroll_y + (self.current_grab_unit.child.size[1] / 2)
            new_pos = [0,0]
            if r_touch[0] > offset_x_r:
                new_pos[0] = offset_x_r
            elif r_touch[0] < offset_x_l:
                new_pos[0] = offset_x_l
            else:
                new_pos[0] = r_touch[0]

            if r_touch[1] > offset_y_t:
                pass
            elif r_touch[1] < offset_y_b:
                pass
            else:
                new_pos[1] = r_touch[1]


                self.current_grab_unit.center = new_pos
            if self.current_grab_unit.child.connected == True:
                self.current_grab_unit.child.line_move = self.current_grab_unit.child.line_move + 1
        if touch.grab_current == self:
            if self.grab_w != '':
                self.grab_w.center = touch.pos

            if self.rect:
                if self.select_rect != '':
                    self.ids.b1.canvas.remove(self.select_rect)
                self.select_rect = InstructionGroup()
                touch_pos = self.compute_relative_position(touch)
                self.select_rect.add(Color(0, 0, 0, 0.2))
                self.select_rect.add(Rectangle(pos=self.rect_start,size=(touch_pos[0]-self.rect_start[0], touch_pos[1]-self.rect_start[1])))
                self.select_rect.add(Color(0, 0, 0, 0.8))
                self.select_rect.add(Line(rectangle=(self.rect_start[0],self.rect_start[1],touch_pos[0]-self.rect_start[0], touch_pos[1]-self.rect_start[1])))
                if self.rect_enable:
                    self.ids.b1.canvas.add(self.select_rect)



        return super(OmWidget, self).on_touch_move(touch, *args)

    def on_touch_up(self, touch, *args):
        if self.current_grab_unit:
            self.current_grab_unit = None
        for i in self.Unit_Operations_Labels:
            if i.collide_point(*self.compute_relative_position(touch)) and not self.ids.unit_shelf.collide_point(*self.compute_relative_position3(touch)):
                self.select_box = InstructionGroup()
                self.select_box.add(Color(0.6, 0, 0, 1))
                #0.3, 0.65, 1, 0.8
                self.select_box.add(Line(rectangle=(i.pos[0], i.pos[1], i.size[0], i.size[1])))
                i.canvas.before.clear()
                i.canvas.before.add(self.select_box)
                break
        if touch.grab_current == self:

            if self.rect and not self.ids.unit_shelf.collide_point(*self.compute_relative_position3(touch)):
                self.multiselect = False
                touch_pos = self.compute_relative_position(touch)
                if self.select_rect != '':
                    self.ids.b1.canvas.remove(self.select_rect)
                if touch_pos[0] > self.rect_start[0]:
                    x_ran = range(int(self.rect_start[0]),int(touch_pos[0]))
                else:
                    x_ran = range(int(touch_pos[0]),int(self.rect_start[0]))

                if touch_pos[1] > self.rect_start[1]:
                    y_ran = range(int(self.rect_start[1]), int(touch_pos[1]))
                else:
                    y_ran = range(int(touch_pos[1]), int(self.rect_start[1]))

                self.Selected_Unit_Operations = []
                if self.rect_enable:
                    for up in self.Unit_Operations_Labels:
                        if int(up.center[0]) in x_ran and int(up.center[1]) in y_ran:
                            self.multiselect = True
                            self.Selected_Unit_Operations.append(up)
                            self.select_box = InstructionGroup()
                            self.select_box.add(Color(0.6, 0, 0, 1))
                            self.select_box.add(Line(rectangle=(up.pos[0], up.pos[1], up.size[0], up.size[1])))
                            up.canvas.before.clear()
                            up.canvas.before.add(self.select_box)
                    self.rect = False
            if self.grab_w != '':
                if self.ids.scroll.collide_point(*touch.pos) and not self.ids.unit_shelf.collide_point(*self.compute_relative_position3(touch)):
                    self.add_unit_op(touch.pos,self.grab_w.UO(),1,"name")
            touch.ungrab(self)
            if self.grab_w != '':
                self.remove_widget(self.grab_w)
                self.grab_w = ''


        return super(OmWidget, self).on_touch_up(touch, *args)

    def compute_relative_position(self,touch):
        return (touch.pos[0] + (self.ids.b1.size[0]-self.ids.scroll.size[0])*self.ids.scroll.scroll_x , touch.pos[1]+(self.ids.b1.size[1]-self.ids.scroll.size[1])*self.ids.scroll.scroll_y)

    def compute_relative_position2(self, touch):
        return (touch[0] + (self.ids.b1.size[0] - self.ids.scroll.size[0]) * self.ids.scroll.scroll_x,
                touch[1] + (self.ids.b1.size[1] - self.ids.scroll.size[1]) * self.ids.scroll.scroll_y)

    def compute_relative_position3(self, touch):
        return (touch.pos[0] - (self.ids.main.size[0] - 150),touch.pos[1] + (self.ids.unit_shelf.size[1] - self.ids.scroll_shelf.size[1]) * self.ids.scroll_shelf.scroll_y)
         # return touch.pos
    def add_unit_op(self,touch,UO,c,name):

        a = UO;
        b = UnitOP.UnitOPM()
        a.bind(connect=self.on_connect)
        a.bind(line_move=self.on_line_move)
        a.name = a.OM_Model + str(self.op_count)
        if(c==0):
            a.name = name
        a.pos_hint = {'center_x': 0.5}
        self.data.append('test.' + a.OM_Model + ' ' + a.OM_Model + str(self.op_count) + ';\n')
        b.size = a.size2
        b.ids.layout.add_widget(a)
        b.child = a
        label = Label(id='label', size_hint_y=None, size=(0, 20), font_size=14, color=(0, 0, 0, 1))
        label.text = a.name
        b.ids.layout.add_widget(label)
        a.text_label = label
        if c==1:
            b.center = self.compute_relative_position2(touch)
        else:
            b.center = touch
            a.center = (touch[0],touch[1]+14)
        self.ids.b1.add_widget(b)
        self.Unit_Operations.append(a)
        self.Unit_Operations_Labels.append(b)
        UnitOP.UnitOP.all_operators.append(a)
        self.op_count += 1
        if (a.check_stm == 0):
            UnitOP.UnitOP.Operators.append(a)
        UnitOP.UnitOP.drop_connections[a.name] = len(self.Unit_Operations) - 1

    def remove_function(self, i):
        self.ids.b1.remove_widget(self.bubb)
        if self.multiselect:
            for i in self.Selected_Unit_Operations:
                self.unit_op = i
                self.remove_unit_op(1)
            self.multiselect =False
        else:
            self.remove_unit_op(1)


    def remove_unit_op(self,*args):
        i = self.Unit_Operations.index(self.unit_op.child)
        i = i + 1
        while i < len(self.Unit_Operations):
            UnitOP.UnitOP.drop_connections[self.Unit_Operations[i].name] -= 1
            i = i + 1

        child = self.unit_op.child
        for key in child.input_streams:
            if child.input_streams[key]:
                if child.check_stm == 0:
                    child.input_streams[key].output_streams[child.conn_point_input+1] = None
                    child.input_streams[key].output_lines[child.conn_point_input + 1] = None
                else:
                    child.input_streams[key].output_streams[1] = None
                    child.input_streams[key].output_lines[1] = None
        for key in child.output_streams:
            if child.output_streams[key]:
                if child.check_stm == 0:
                    child.output_streams[key].input_streams[child.conn_point_output+1] = None
                    child.output_streams[key].input_lines[child.conn_point_output+1] = None
                else:
                    child.output_streams[key].input_streams[1] = None
                    child.output_streams[key].input_lines[1] = None
        for key in child.input_lines:
            if child.input_lines[key]:
                self.ids.b1.canvas.remove(child.input_lines[key])
                child.input_lines[key] = None
        for key in child.output_lines:
            if child.output_lines[key]:
                self.ids.b1.canvas.remove(child.output_lines[key])
                child.input_lines[key] = None
        self.ids.b1.remove_widget(self.unit_op)

        self.Unit_Operations_Labels.remove(self.unit_op)
        self.Unit_Operations.remove(self.unit_op.child)
        UnitOP.UnitOP.all_operators.remove(self.unit_op.child)
        if self.unit_op.child in UnitOP.UnitOP.Operators:
            UnitOP.UnitOP.Operators.remove(self.unit_op.child)
    def on_connect(self, instance, value):
        p = 0
        instance.connected = True
        for key in instance.input_lines:
            if instance.input_lines[key]:
                self.ids.b1.canvas.remove(instance.input_lines[key])
                instance.input_lines[key] = None
        for key in instance.output_lines:
            if instance.output_lines[key]:
                self.ids.b1.canvas.remove(instance.output_lines[key])
                instance.input_lines[key] = None
        for key in instance.input_streams:
            if instance.input_streams[key]:
                val = instance.input_streams[key]
                val.output_streams[1] = instance
                val.connected = True
                val.Update_Conn_Pnts()

                val.conn_point_output = p
                sourcepos = val.Connecting_Points_Output
                destpos = instance.Connecting_Points_Input[p]
                line = InstructionGroup()
                print sourcepos
                print destpos
                line.add(Color(0.6, 0.4, 0.2, 1))
                if sourcepos[0] < destpos[0]:
                    line1 = (sourcepos[0], sourcepos[1], sourcepos[0] + (destpos[0] - sourcepos[0]) / 2, sourcepos[1])
                    line2 = (sourcepos[0] + (destpos[0] - sourcepos[0]) / 2, sourcepos[1],sourcepos[0] + (destpos[0] - sourcepos[0]) / 2, destpos[1])
                    line3 = (sourcepos[0] + (destpos[0] - sourcepos[0]) / 2, destpos[1], destpos[0], destpos[1])
                elif sourcepos[1] >= destpos[1]:
                    print "high"
                    sourcepos_new = val.downward_connector_output
                    destpos_new = instance.upward_connector_input
                    line.add(Line(points=(sourcepos[0],sourcepos[1],sourcepos_new[0],sourcepos[1]),width=1))
                    line.add(Line(points=(sourcepos_new[0], sourcepos[1],sourcepos_new[0],sourcepos_new[1]),width=1))
                    line.add(Line(points=(destpos[0], destpos[1], destpos_new[0], destpos[1]),width=1))
                    line.add(Line(points=(destpos_new[0], destpos[1], destpos_new[0], destpos_new[1]),width=1))

                    if (sourcepos_new[1] < destpos_new[1]):
                        line1 = (sourcepos_new[0], sourcepos_new[1], sourcepos_new[0] + (destpos_new[0] - sourcepos_new[0]) / 2, sourcepos_new[1])
                        line2 = (sourcepos_new[0] + (destpos_new[0] - sourcepos_new[0]) / 2, sourcepos_new[1],sourcepos_new[0] + (destpos_new[0] - sourcepos_new[0]) / 2, destpos_new[1])
                        line3 = (sourcepos_new[0] + (destpos_new[0] - sourcepos_new[0]) / 2, destpos_new[1], destpos_new[0], destpos_new[1])
                    else:
                        line1 = (sourcepos_new[0], sourcepos_new[1], sourcepos_new[0], sourcepos_new[1] + (-sourcepos_new[1] + destpos_new[1]) / 2)
                        line2 = (sourcepos_new[0], sourcepos_new[1] + (-sourcepos_new[1] + destpos_new[1]) / 2, destpos_new[0],sourcepos_new[1] + (-sourcepos_new[1] + destpos_new[1]) / 2)
                        line3 = (destpos_new[0], sourcepos_new[1] + (-sourcepos_new[1] + destpos_new[1]) / 2, destpos_new[0],destpos_new[1])

                elif sourcepos[1] < destpos[1]:
                    print "low"
                    sourcepos_new = val.upward_connector_output
                    destpos_new = instance.downward_connector_input
                    line.add(Line(points=(sourcepos[0], sourcepos[1], sourcepos_new[0], sourcepos[1]),width=1))
                    line.add(Line(points=(sourcepos_new[0], sourcepos[1], sourcepos_new[0], sourcepos_new[1]),width=1))
                    line.add(Line(points=(destpos[0], destpos[1], destpos_new[0], destpos[1]),width=1))
                    line.add(Line(points=(destpos_new[0], destpos[1], destpos_new[0], destpos_new[1]),width=1))
                    if (sourcepos_new[1] > destpos_new[1]):
                        line1 = (sourcepos_new[0], sourcepos_new[1], sourcepos_new[0] + (destpos_new[0] - sourcepos_new[0]) / 2,sourcepos_new[1])
                        line2 = (sourcepos_new[0] + (destpos_new[0] - sourcepos_new[0]) / 2, sourcepos_new[1],sourcepos_new[0] + (destpos_new[0] - sourcepos_new[0]) / 2, destpos_new[1])
                        line3 = (sourcepos_new[0] + (destpos_new[0] - sourcepos_new[0]) / 2, destpos_new[1], destpos_new[0],destpos_new[1])
                    else:
                        line1 = (sourcepos_new[0], sourcepos_new[1], sourcepos_new[0],sourcepos_new[1] + (-sourcepos_new[1] + destpos_new[1]) / 2)
                        line2 = ( sourcepos_new[0], sourcepos_new[1] + (-sourcepos_new[1] + destpos_new[1]) / 2, destpos_new[0],sourcepos_new[1] + (-sourcepos_new[1] + destpos_new[1]) / 2)
                        line3 = (destpos_new[0], sourcepos_new[1] + (-sourcepos_new[1] + destpos_new[1]) / 2, destpos_new[0],destpos_new[1])


                line.add(Line(points=line1, width=1))
                line.add(Line(points=line2, width=1))
                line.add(Line(points=line3, width=1))
                instance.input_lines[key] = line
                val.output_lines[1] = line
                self.ids.b1.canvas.add(line)
                if 'equation\n' not in self.data:
                    self.data.append('equation\n')
                self.data.append('connect (' + instance.name + '.port' + str(p) + ', ' + val.name + '.conn);\n')
            p = p + 1
        p=0
        for key in instance.output_streams:
            if instance.output_streams[key]:
                val = instance.output_streams[key]
                val.input_streams[1] = instance
                val.connected = True
                val.Update_Conn_Pnts()
                val.conn_point_input = p
                sourcepos = instance.Connecting_Points_Output[p]
                destpos = val.Connecting_Points_Input
                line = InstructionGroup()
                line.add(Color(0.6, 0.4, 0.2, 1))

                if sourcepos[0] < destpos[0]:
                    line1 = (sourcepos[0], sourcepos[1], sourcepos[0] + (destpos[0] - sourcepos[0]) / 2, sourcepos[1])
                    line2 = (sourcepos[0] + (destpos[0] - sourcepos[0]) / 2, sourcepos[1],
                             sourcepos[0] + (destpos[0] - sourcepos[0]) / 2, destpos[1])
                    line3 = (sourcepos[0] + (destpos[0] - sourcepos[0]) / 2, destpos[1], destpos[0], destpos[1])
                elif sourcepos[1] >= destpos[1]:
                    print "high"
                    sourcepos_new = instance.downward_connector_output
                    destpos_new = val.upward_connector_input
                    line.add(Line(points=(sourcepos[0], sourcepos[1], sourcepos_new[0], sourcepos[1]), width=1))
                    line.add(Line(points=(sourcepos_new[0], sourcepos[1], sourcepos_new[0], sourcepos_new[1]), width=1))
                    line.add(Line(points=(destpos[0], destpos[1], destpos_new[0], destpos[1]), width=1))
                    line.add(Line(points=(destpos_new[0], destpos[1], destpos_new[0], destpos_new[1]), width=1))

                    if (sourcepos_new[1] < destpos_new[1]):
                        line1 = (
                        sourcepos_new[0], sourcepos_new[1], sourcepos_new[0] + (destpos_new[0] - sourcepos_new[0]) / 2,
                        sourcepos_new[1])
                        line2 = (sourcepos_new[0] + (destpos_new[0] - sourcepos_new[0]) / 2, sourcepos_new[1],
                                 sourcepos_new[0] + (destpos_new[0] - sourcepos_new[0]) / 2, destpos_new[1])
                        line3 = (
                        sourcepos_new[0] + (destpos_new[0] - sourcepos_new[0]) / 2, destpos_new[1], destpos_new[0],
                        destpos_new[1])
                    else:
                        line1 = (sourcepos_new[0], sourcepos_new[1], sourcepos_new[0],
                                 sourcepos_new[1] + (-sourcepos_new[1] + destpos_new[1]) / 2)
                        line2 = (
                        sourcepos_new[0], sourcepos_new[1] + (-sourcepos_new[1] + destpos_new[1]) / 2, destpos_new[0],
                        sourcepos_new[1] + (-sourcepos_new[1] + destpos_new[1]) / 2)
                        line3 = (
                        destpos_new[0], sourcepos_new[1] + (-sourcepos_new[1] + destpos_new[1]) / 2, destpos_new[0],
                        destpos_new[1])

                elif sourcepos[1] < destpos[1]:
                    print "low"
                    sourcepos_new = instance.upward_connector_output
                    destpos_new = val.downward_connector_input
                    line.add(Line(points=(sourcepos[0], sourcepos[1], sourcepos_new[0], sourcepos[1]), width=1))
                    line.add(Line(points=(sourcepos_new[0], sourcepos[1], sourcepos_new[0], sourcepos_new[1]), width=1))
                    line.add(Line(points=(destpos[0], destpos[1], destpos_new[0], destpos[1]), width=1))
                    line.add(Line(points=(destpos_new[0], destpos[1], destpos_new[0], destpos_new[1]), width=1))
                    if (sourcepos_new[1] > destpos_new[1]):
                        line1 = (
                        sourcepos_new[0], sourcepos_new[1], sourcepos_new[0] + (destpos_new[0] - sourcepos_new[0]) / 2,
                        sourcepos_new[1])
                        line2 = (sourcepos_new[0] + (destpos_new[0] - sourcepos_new[0]) / 2, sourcepos_new[1],
                                 sourcepos_new[0] + (destpos_new[0] - sourcepos_new[0]) / 2, destpos_new[1])
                        line3 = (
                        sourcepos_new[0] + (destpos_new[0] - sourcepos_new[0]) / 2, destpos_new[1], destpos_new[0],
                        destpos_new[1])
                    else:
                        line1 = (sourcepos_new[0], sourcepos_new[1], sourcepos_new[0],
                                 sourcepos_new[1] + (-sourcepos_new[1] + destpos_new[1]) / 2)
                        line2 = (
                        sourcepos_new[0], sourcepos_new[1] + (-sourcepos_new[1] + destpos_new[1]) / 2, destpos_new[0],
                        sourcepos_new[1] + (-sourcepos_new[1] + destpos_new[1]) / 2)
                        line3 = (
                        destpos_new[0], sourcepos_new[1] + (-sourcepos_new[1] + destpos_new[1]) / 2, destpos_new[0],
                        destpos_new[1])




                line.add(Line(points=line1, width=1))
                line.add(Line(points=line2, width=1))
                line.add(Line(points=line3, width=1))
                instance.output_lines[key] = line
                val.input_lines[1] = line
                self.ids.b1.canvas.add(line)
                if 'equation\n' not in self.data:
                    self.data.append('equation\n')
                self.data.append('connect (' + instance.name + '.port' + str(p) + ', ' + val.name + '.conn);\n')
            p = p + 1



    def on_line_move(self, instance, value):

        for key in instance.input_lines:
            if instance.input_lines[key]:
                self.ids.b1.canvas.remove(instance.input_lines[key])
                instance.Update_Conn_Pnts()

                if (instance.check_stm == 0):
                    instance.input_streams[1].Update_Conn_Pnts()
                    sourcepos = instance.input_streams[1].Connecting_Points_Output[instance.conn_point_input]
                    destpos = instance.Connecting_Points_Input
                else:
                    instance.input_streams[key].Update_Conn_Pnts()
                    sourcepos = instance.input_streams[key].Connecting_Points_Output
                    destpos = instance.Connecting_Points_Input[key-1]
                line = InstructionGroup()
                line.add(Color(0.6, 0.4, 0.2, 1))
                if sourcepos[0] < destpos[0]:
                    line1 = (sourcepos[0], sourcepos[1], sourcepos[0] + (destpos[0] - sourcepos[0]) / 2, sourcepos[1])
                    line2 = (sourcepos[0] + (destpos[0] - sourcepos[0]) / 2, sourcepos[1],
                             sourcepos[0] + (destpos[0] - sourcepos[0]) / 2, destpos[1])
                    line3 = (sourcepos[0] + (destpos[0] - sourcepos[0]) / 2, destpos[1], destpos[0], destpos[1])
                elif sourcepos[1] >= destpos[1]:
                    if (instance.check_stm == 0):
                        instance.input_streams[1].Update_Conn_Pnts()
                        sourcepos_new =  instance.input_streams[1].downward_connector_output
                        destpos_new = instance.upward_connector_input
                    else:
                        instance.input_streams[key].Update_Conn_Pnts()
                        sourcepos_new = instance.input_streams[key].downward_connector_output
                        destpos_new = instance.upward_connector_input
                    line.add(Line(points=(sourcepos[0], sourcepos[1], sourcepos_new[0], sourcepos[1]), width=1))
                    line.add(Line(points=(sourcepos_new[0], sourcepos[1], sourcepos_new[0], sourcepos_new[1]), width=1))
                    line.add(Line(points=(destpos[0], destpos[1], destpos_new[0], destpos[1]), width=1))
                    line.add(Line(points=(destpos_new[0], destpos[1], destpos_new[0], destpos_new[1]), width=1))

                    if (sourcepos_new[1] < destpos_new[1]):
                        line1 = (
                        sourcepos_new[0], sourcepos_new[1], sourcepos_new[0] + (destpos_new[0] - sourcepos_new[0]) / 2,
                        sourcepos_new[1])
                        line2 = (sourcepos_new[0] + (destpos_new[0] - sourcepos_new[0]) / 2, sourcepos_new[1],
                                 sourcepos_new[0] + (destpos_new[0] - sourcepos_new[0]) / 2, destpos_new[1])
                        line3 = (
                        sourcepos_new[0] + (destpos_new[0] - sourcepos_new[0]) / 2, destpos_new[1], destpos_new[0],
                        destpos_new[1])
                    else:
                        line1 = (sourcepos_new[0], sourcepos_new[1], sourcepos_new[0],
                                 sourcepos_new[1] + (-sourcepos_new[1] + destpos_new[1]) / 2)
                        line2 = (
                        sourcepos_new[0], sourcepos_new[1] + (-sourcepos_new[1] + destpos_new[1]) / 2, destpos_new[0],
                        sourcepos_new[1] + (-sourcepos_new[1] + destpos_new[1]) / 2)
                        line3 = (
                        destpos_new[0], sourcepos_new[1] + (-sourcepos_new[1] + destpos_new[1]) / 2, destpos_new[0],
                        destpos_new[1])

                elif sourcepos[1] < destpos[1]:
                    if (instance.check_stm == 0):
                        instance.input_streams[1].Update_Conn_Pnts()
                        sourcepos_new = instance.input_streams[1].upward_connector_output
                        destpos_new = instance.downward_connector_input
                    else:
                        instance.input_streams[key].Update_Conn_Pnts()
                        sourcepos_new = instance.input_streams[key].upward_connector_output
                        destpos_new = instance.downward_connector_input
                    line.add(Line(points=(sourcepos[0], sourcepos[1], sourcepos_new[0], sourcepos[1]), width=1))
                    line.add(Line(points=(sourcepos_new[0], sourcepos[1], sourcepos_new[0], sourcepos_new[1]), width=1))
                    line.add(Line(points=(destpos[0], destpos[1], destpos_new[0], destpos[1]), width=1))
                    line.add(Line(points=(destpos_new[0], destpos[1], destpos_new[0], destpos_new[1]), width=1))
                    if (sourcepos_new[1] > destpos_new[1]):
                        line1 = (
                        sourcepos_new[0], sourcepos_new[1], sourcepos_new[0] + (destpos_new[0] - sourcepos_new[0]) / 2,
                        sourcepos_new[1])
                        line2 = (sourcepos_new[0] + (destpos_new[0] - sourcepos_new[0]) / 2, sourcepos_new[1],
                                 sourcepos_new[0] + (destpos_new[0] - sourcepos_new[0]) / 2, destpos_new[1])
                        line3 = (
                        sourcepos_new[0] + (destpos_new[0] - sourcepos_new[0]) / 2, destpos_new[1], destpos_new[0],
                        destpos_new[1])
                    else:
                        line1 = (sourcepos_new[0], sourcepos_new[1], sourcepos_new[0],
                                 sourcepos_new[1] + (-sourcepos_new[1] + destpos_new[1]) / 2)
                        line2 = (
                        sourcepos_new[0], sourcepos_new[1] + (-sourcepos_new[1] + destpos_new[1]) / 2, destpos_new[0],
                        sourcepos_new[1] + (-sourcepos_new[1] + destpos_new[1]) / 2)
                        line3 = (
                        destpos_new[0], sourcepos_new[1] + (-sourcepos_new[1] + destpos_new[1]) / 2, destpos_new[0],
                        destpos_new[1])


                line.add(Line(points=line1, width=1))
                line.add(Line(points=line2, width=1))
                line.add(Line(points=line3, width=1))
                if(instance.check_stm == 0):
                    instance.input_streams[1].output_lines[instance.conn_point_input + 1] = line
                    instance.input_lines[1] = line
                else:
                    instance.input_lines[key] = line
                    instance.input_streams[key].output_lines[1] = line
                self.ids.b1.canvas.add(line)
        for key in instance.output_lines:
            if instance.output_lines[key]:
                self.ids.b1.canvas.remove(instance.output_lines[key])
                instance.Update_Conn_Pnts()
                if (instance.check_stm == 0):
                    instance.output_streams[1].Update_Conn_Pnts()
                    sourcepos = instance.Connecting_Points_Output
                    destpos = instance.output_streams[1].Connecting_Points_Input[instance.conn_point_output]
                else:
                    instance.output_streams[key].Update_Conn_Pnts()
                    sourcepos = instance.Connecting_Points_Output[key - 1]
                    destpos = instance.output_streams[key].Connecting_Points_Input
                line = InstructionGroup()
                line.add(Color(0.6, 0.4, 0.2, 1))

                if sourcepos[0] < destpos[0]:
                    line1 = (sourcepos[0], sourcepos[1], sourcepos[0] + (destpos[0] - sourcepos[0]) / 2, sourcepos[1])
                    line2 = (sourcepos[0] + (destpos[0] - sourcepos[0]) / 2, sourcepos[1],
                             sourcepos[0] + (destpos[0] - sourcepos[0]) / 2, destpos[1])
                    line3 = (sourcepos[0] + (destpos[0] - sourcepos[0]) / 2, destpos[1], destpos[0], destpos[1])
                elif sourcepos[1] >= destpos[1]:
                    if (instance.check_stm == 0):
                        sourcepos_new = instance.downward_connector_output
                        destpos_new = instance.output_streams[1].upward_connector_input
                    else:
                        sourcepos_new = instance.downward_connector_output
                        destpos_new =  instance.output_streams[key].upward_connector_input
                    line.add(Line(points=(sourcepos[0], sourcepos[1], sourcepos_new[0], sourcepos[1]), width=1))
                    line.add(Line(points=(sourcepos_new[0], sourcepos[1], sourcepos_new[0], sourcepos_new[1]), width=1))
                    line.add(Line(points=(destpos[0], destpos[1], destpos_new[0], destpos[1]), width=1))
                    line.add(Line(points=(destpos_new[0], destpos[1], destpos_new[0], destpos_new[1]), width=1))

                    if (sourcepos_new[1] < destpos_new[1]):
                        line1 = (
                            sourcepos_new[0], sourcepos_new[1],
                            sourcepos_new[0] + (destpos_new[0] - sourcepos_new[0]) / 2,
                            sourcepos_new[1])
                        line2 = (sourcepos_new[0] + (destpos_new[0] - sourcepos_new[0]) / 2, sourcepos_new[1],
                                 sourcepos_new[0] + (destpos_new[0] - sourcepos_new[0]) / 2, destpos_new[1])
                        line3 = (
                            sourcepos_new[0] + (destpos_new[0] - sourcepos_new[0]) / 2, destpos_new[1], destpos_new[0],
                            destpos_new[1])
                    else:
                        line1 = (sourcepos_new[0], sourcepos_new[1], sourcepos_new[0],
                                 sourcepos_new[1] + (-sourcepos_new[1] + destpos_new[1]) / 2)
                        line2 = (
                            sourcepos_new[0], sourcepos_new[1] + (-sourcepos_new[1] + destpos_new[1]) / 2,
                            destpos_new[0],
                            sourcepos_new[1] + (-sourcepos_new[1] + destpos_new[1]) / 2)
                        line3 = (
                            destpos_new[0], sourcepos_new[1] + (-sourcepos_new[1] + destpos_new[1]) / 2, destpos_new[0],
                            destpos_new[1])

                elif sourcepos[1] < destpos[1]:
                    if (instance.check_stm == 0):
                        sourcepos_new =  instance.upward_connector_output
                        destpos_new = instance.output_streams[1].downward_connector_input
                    else:
                        sourcepos_new =  instance.upward_connector_output
                        destpos_new = instance.output_streams[key].downward_connector_input
                    line.add(Line(points=(sourcepos[0], sourcepos[1], sourcepos_new[0], sourcepos[1]), width=1))
                    line.add(Line(points=(sourcepos_new[0], sourcepos[1], sourcepos_new[0], sourcepos_new[1]), width=1))
                    line.add(Line(points=(destpos[0], destpos[1], destpos_new[0], destpos[1]), width=1))
                    line.add(Line(points=(destpos_new[0], destpos[1], destpos_new[0], destpos_new[1]), width=1))
                    if (sourcepos_new[1] > destpos_new[1]):
                        line1 = (
                            sourcepos_new[0], sourcepos_new[1],
                            sourcepos_new[0] + (destpos_new[0] - sourcepos_new[0]) / 2,
                            sourcepos_new[1])
                        line2 = (sourcepos_new[0] + (destpos_new[0] - sourcepos_new[0]) / 2, sourcepos_new[1],
                                 sourcepos_new[0] + (destpos_new[0] - sourcepos_new[0]) / 2, destpos_new[1])
                        line3 = (
                            sourcepos_new[0] + (destpos_new[0] - sourcepos_new[0]) / 2, destpos_new[1], destpos_new[0],
                            destpos_new[1])
                    else:
                        line1 = (sourcepos_new[0], sourcepos_new[1], sourcepos_new[0],
                                 sourcepos_new[1] + (-sourcepos_new[1] + destpos_new[1]) / 2)
                        line2 = (
                            sourcepos_new[0], sourcepos_new[1] + (-sourcepos_new[1] + destpos_new[1]) / 2,
                            destpos_new[0],
                            sourcepos_new[1] + (-sourcepos_new[1] + destpos_new[1]) / 2)
                        line3 = (
                            destpos_new[0], sourcepos_new[1] + (-sourcepos_new[1] + destpos_new[1]) / 2, destpos_new[0],
                            destpos_new[1])

                line.add(Line(points=line1, width=1))
                line.add(Line(points=line2, width=1))
                line.add(Line(points=line3, width=1))
                if(instance.check_stm == 0):
                    instance.output_lines[1] = line
                    instance.output_streams[1].input_lines[instance.conn_point_output + 1] = line
                else:
                    instance.output_lines[key] = line
                    instance.output_streams[key].input_lines[1] = line
                self.ids.b1.canvas.add(line)

    def on_text(self, instance, value):
        dropdown = instance.drop_down
        dropdown.clear_widgets()
        if not self.compo.ids.comp_input.text == "":
            for i in self.word_list:
                if value in i:
                    btn = CompButton(text=i, color=(0, 0, 0, 1), background_normal='',background_color=(0.7, 0.7, 0.7, 1))
                    btn.bind(on_release=lambda gbtn: dropdown.select(gbtn.text))
                    dropdown.add_widget(btn)

    def CompPop(self, instance):
        self.comp_dropdown.max_height = 200
        self.comp_dropdown.clear_widgets()
        for c in self.addedcomp:
            btn = Button(text=c,color=(0, 0, 0, 1), size_hint_y=None, height=30, background_normal='',background_color=(0.7, 0.7, 0.7, 1), halign='left',padding=[0, 2])
            btn.bind(on_release=self.select_remove_compound)
            self.comp_dropdown.add_widget(btn)
        self.compo = CompPop()
        self.compo.ids.add_comp.bind(on_press=self.add_compound)
        self.compo.ids.remove_comp.bind(on_press=self.remove_compound)
        self.compo.ids.comp_input.bind(text=self.on_text)
        self.compo.ids.show_comp.bind(on_release=self.comp_dropdown.open)
        self.compo.open()

    def add_compound(self, instance):
        comp = str(self.compo.ids.comp_input.text)
        if comp not in self.word_list:
            self.error.text = "Invalid Compound!"
            self.error_popup.open()
        else:
            if comp not in self.addedcomp:
                UnitOP.UnitOP.compound_elements.append(str(self.compo.ids.comp_input.text))
                self.addedcomp.append(str(self.compo.ids.comp_input.text))
            self.comp_dropdown.clear_widgets()
            for c in self.addedcomp:
                btn = Button(text=c, color=(0, 0, 0, 1), size_hint_y=None, height=30, background_normal='',background_color=(0.7, 0.7, 0.7, 1), halign='left',padding=[0, 2])
                btn.bind(on_release=self.select_remove_compound)
                self.comp_dropdown.add_widget(btn)


    def remove_compound(self, instance):
        self.comp_dropdown.clear_widgets()
        if self.compo.ids.show_comp.text in self.addedcomp:
            self.addedcomp.remove(self.compo.ids.show_comp.text)
            UnitOP.UnitOP.compound_elements.remove(self.compo.ids.show_comp.text)
        for c in self.addedcomp:
            btn = Button(text=c, color=(0, 0, 0, 1), size_hint_y=None, height=30, background_normal='',background_color=(0.7, 0.7, 0.7, 1), halign='left',padding=[0, 2])
            btn.bind(on_release=self.select_remove_compound)
            self.comp_dropdown.add_widget(btn)
        self.compo.ids.show_comp.text = 'Show Compounds'



    def ThermoPop(self,instance):
        self.tp = ThermoPop();
        self.Thermodropdown = DropDown()
        for model in Thermodynamic_models:
            btn = Button(text=model,color=(0, 0, 0, 1), size_hint_y=None, height=30, background_normal='',background_color=(0.7, 0.7, 0.7, 1), halign='left',padding=[0, 2])
            btn.bind(on_release=self.ThermoSelect)
            self.Thermodropdown.add_widget(btn)
        # self.ShowVLEModels = Button(text='Show VLE Models', size_hint=(1, 0.7), pos_hint={'center_x': 0, 'center_y': 0.7})
        self.tp.ids.show_vle.bind(on_release=self.Thermodropdown.open)
        self.tp.ids.present_model.text='Selected Model: '+ self.Selected_thermo_model
        self.tp.open()


    def ThermoSelect(self,instance):
        self.Selected_thermo_model = instance.text
        self.tp.ids.present_model.text = 'Selected Model: ' + instance.text
        self.Thermodropdown.dismiss()

    def select_remove_compound(self, instance):
        self.compo.ids.show_comp.text = instance.text
        self.comp_dropdown.dismiss()

class Omapp(App):

    def build(self):
        return OmWidget()

if __name__ == "__main__" :
    Omapp().run()

