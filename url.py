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
from kivy.uix.actionbar import ActionBar
from kivy.uix.actionbar import ActionView
from kivy.uix.actionbar import ActionButton
from kivy.uix.actionbar import ActionPrevious
from kivy.uix.dropdown import DropDown

import StaticUO
from OMPython import OMCSession
import UnitOP

Thermodynamic_models = ['Peng-Robinson','SRK','NRTL','UNIQUAC']
File_options = ['New Steady-state Simulation','New Compound Creator Study','New Data Regression Study','New UNIFAC Parameter Regression Case','Open','Open Samples','Save','Save All','Save As','Close Active Simulation','Close All','Exit Openmodellica']
Edit_options = ['Undo','Redo','Cut Selected Objects','Copy Selected Objects','Paste Objects','Remove selected objects','Clone selected objects','Recalculate object','Export data to Clipboard','Simulation settings','General settings']
Insert_options = ['Flowsheet Object','Property Table','Master Property Table','Linked Spreadsheet Table','Image','Text','Rectangle']
Tools_options = ['Petroleum Characterization (Bulk C7+)','Petroleum Characterization (Distillation Curves)','Petroleum Array Manager','Reactions Manager','Pure Compound Property Viewer/Editor','User Database Manager','CAPE-OPEN Component Registration' ]
Utilities_options = ['Add Utility']
Optimization_options = ['Sensitivity Analysis','Multivariate Optimizer']
Scripts_options = ['Script Manager']
Results_options = ['Create Report']
Plugins_options = ['CAPE-OPEN Plugins','Natural Gas Properties']
Windows_options = ['Cascade','Group Horizontally','Group Vertically',]
View_options = ['Show Toolstrip','Console Output','calculation Queue','Watch panel','CAPE-OPEN Objects Reports','Flowsheet Toolstrip','Unit Systems Toolstrip',"Restore Docking Panels' Layout",'Close Opened Object Editors']
Help_options = ['Show Help','Documention','Openmodellica on the web','Donate!','About OpenModellica']

class MenuButton(Button):
    pass

class OmWidget(GridLayout):
    lines = []
    Unit_Operations = []
    data = []
    def __init__(self,**kwargs):
        super(OmWidget,self).__init__(**kwargs)
        self.addedcomp = []
        self.dropdown = DropDown()
        self.Selected_thermo_model = 'No Model Selected'
        self.data.append('model Flowsheet\n')
        UnitOP.UnitOP.size_limit = self.ids.b1.size
        self.filedropdown = DropDown(auto_width=False, width=300)
        for model in File_options:
            btn = MenuButton(text=model, width=300)
            btn.text_size = btn.size
            self.filedropdown.add_widget(btn)

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
            btn = MenuButton(text=model, width=100)
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
            btn = MenuButton(text=model, width=150)
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
        with open('Flowsheet.mo', 'w') as txtfile:
            for d in self.data:
                txtfile.write(d)
            txtfile.write('end Flowsheet;\n')
            #
            # omc = OMCSession()
            # omc.sendExpression("loadFile(\"/Users/rahuljain/Desktop/MIxerModel/test.mo\")")
            # omc.sendExpression("loadFile(\"/Users/rahuljain/Desktop/OM_GUI/Flowsheet.mo\")")
            # chek = omc.sendExpression("simulate(Flowsheet, stopTime=1.0)")
            # print chek
            # for unit in self.Unit_Operations:
            #     if 'Mat_Stm' in unit.name:
            #         print 'yes'
            #         unit.PropertyVal = []
            #         for prop in unit.PropertyList:
            #             resultstr = unit.name + '.' + prop
            #             print resultstr
            #             resultval = str(omc.sendExpression("val("+resultstr+", 0.5)"))
            #             print resultval
            #             unit.PropertyVal.append(resultval)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            UnitOP.UnitOP.size_limit = self.ids.b1.size
        return super(OmWidget, self).on_touch_down(touch)

    def add_but(self,instance,value):
        a = instance.UO()
        a.bind(connect=self.on_connect)
        a.bind(line_move=self.on_line_move)
        a.name = a.OM_Model+str(value)
        self.data.append('test.'+a.OM_Model+' '+a.OM_Model+str(value)+';\n')
#        a.bind(multi_touch = self.MultiTouch)
        self.ids.b1.add_widget(a)
        self.Unit_Operations.append(a)
        if(a.check_stm == 0):
            UnitOP.UnitOP.Operators.append(a)
        UnitOP.UnitOP.drop_connections[a.name] = len(self.Unit_Operations)-1

    def on_connect(self, instance, value):
        p = 0
        instance.connected = True
        for val in instance.connected_to:
            self.Unit_Operations[val].connected_to.append(self.Unit_Operations.index(instance))
            self.Unit_Operations[val].connected = True
            self.Unit_Operations[val].Update_Conn_Pnts()
            self.Unit_Operations[val].conn_point = p
            destpos = self.Unit_Operations[val].Connecting_Points[p]
            sourcepos = instance.Connecting_Points[p]
            horzpoint = (sourcepos[0],sourcepos[1],destpos[0],sourcepos[1])
            vertpoint = (destpos[0],sourcepos[1],destpos[0],destpos[1])
            line = InstructionGroup()
            line.add(Color(0, 0, 0, 0.5))
            line.add(Line(points=horzpoint, width=1))
            line.add(Line(points=vertpoint,width=1))
            self.lines.append(line)
            self.Unit_Operations[val].line_nos.append(len(self.lines)-1)
            instance.line_nos.append(len(self.lines)-1)
            self.ids.b1.canvas.add(line)
            if 'equation\n' not in self.data:
                self.data.append('equation\n')
            self.data.append('connect ('+instance.name+'.port'+str(p)+', '+self.Unit_Operations[val].name+'.conn);\n')
            p = p + 1


    def on_line_move(self, instance, value):
        ii=0

        for liine in instance.line_nos:
            self.ids.b1.canvas.remove(self.lines[liine])
            instance.Update_Conn_Pnts()
            self.Unit_Operations[instance.connected_to[ii]].Update_Conn_Pnts()
            destpos = self.Unit_Operations[instance.connected_to[ii]].Connecting_Points[instance.conn_point]
            sourcepos = instance.Connecting_Points[ii]
            if instance.check_stm == 0:
                t = destpos
                destpos = sourcepos
                sourcepos = t
            horzpoint = (sourcepos[0], sourcepos[1], destpos[0], sourcepos[1])
            vertpoint = (destpos[0], sourcepos[1], destpos[0], destpos[1])
            line = InstructionGroup()
            line.add(Color(0, 0, 0, 0.5))
            line.add(Line(points=horzpoint, width=1))
            line.add(Line(points=vertpoint, width=1))
            self.lines.pop(liine)
            self.lines.insert(liine,line)
            self.ids.b1.canvas.add(line)
            ii = ii + 1

    def CompPop(self, instance):
        self.dropdown.clear_widgets()
        for c in self.addedcomp:
            btn = Button(text=c, size_hint_y=None, height=40)
            btn.bind(on_release=self.select_remove_compound)
            self.dropdown.add_widget(btn)
        self.compo = Popup(title="COMPONDS SELECTION", size_hint=(0.7, 0.3), auto_dismiss=True,
                           pos_hint={'center_x': 0.5, 'center_y': 0.5}, opacity=0.8)
        self.lay1 = StackLayout(pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.lay = BoxLayout(size_hint=(1, 0.5), pos_hint={'center_x': 0.5, 'y': 0.5})
        self.lay2 = BoxLayout(size_hint=(1, 0.5), pos_hint={'center_x': 0.5, 'y': 0.5})
        self.add = Button(text="Add", size_hint=(0.3, 0.6), pos_hint={'center_x': 0, 'center_y': 0.7})
        self.add.bind(on_press=self.add_compound)
        self.remove = Button(text="Remove", size_hint=(0.3, 0.6), pos_hint={'center_x': 0, 'center_y': 0.9})
        self.remove.bind(on_press=self.remove_compound)
        self.inp = TextInput(text='', size_hint=(0.6, 0.6), pos_hint={'center_x': 0, 'center_y': 0.7}, hint_text='Ben')
        self.showcomp = Button(text='Show Compounds', size_hint=(0.6, 0.6), pos_hint={'center_x': 0, 'center_y': 0.9})
        self.showcomp.bind(on_release=self.dropdown.open)
        self.lay.add_widget(self.inp)
        self.lay.add_widget(self.add)
        self.lay1.add_widget(self.lay)
        self.lay2.add_widget(self.showcomp)
        self.lay2.add_widget(self.remove)
        self.lay1.add_widget(self.lay2)
        self.compo.content = self.lay1
        self.compo.open()

    def add_compound(self, instance):
        if str(self.inp.text) not in self.addedcomp:
            self.addedcomp.append(str(self.inp.text))
        self.dropdown.clear_widgets()
        for c in self.addedcomp:
            btn = Button(text=c, size_hint_y=None, height=40)
            btn.bind(on_release=self.select_remove_compound)
            self.dropdown.add_widget(btn)
        print self.addedcomp

    def remove_compound(self, instance):
        self.dropdown.clear_widgets()
        if self.showcomp.text in self.addedcomp:
            self.addedcomp.remove(self.showcomp.text)
        for c in self.addedcomp:
            btn = Button(text=c, size_hint_y=None, height=40)
            btn.bind(on_release=self.select_remove_compound)
            self.dropdown.add_widget(btn)
        self.showcomp.text = 'Show Compounds'


    def ThermoPop(self,instance):
        self.tp = Popup(title="VLE MODEL SELECTION", size_hint=(0.7, 0.3), auto_dismiss=True,
                           pos_hint={'center_x': 0.5, 'center_y': 0.5}, opacity=0.8)
        self.Thermodropdown = DropDown()
        for model in Thermodynamic_models:
            btn = Button(text=model,size_hint_y=None,height=40)
            btn.bind(on_release=self.ThermoSelect)
            self.Thermodropdown.add_widget(btn)
        self.ShowVLEModels = Button(text='Show VLE Models', size_hint=(1, 0.7), pos_hint={'center_x': 0, 'center_y': 0.7})
        self.ShowVLEModels.bind(on_release=self.Thermodropdown.open)
        self.PresentModel = Label(text='Selected Model: '+self.Selected_thermo_model)
        self.PM = BoxLayout(size_hint=(1, 0.5), pos_hint={'center_x': 0.5, 'y': 0.5})
        self.SM = BoxLayout(size_hint=(1, 0.5), pos_hint={'center_x': 0.5, 'y': 0.5})
        self.PM.add_widget(self.PresentModel)
        self.SM.add_widget(self.ShowVLEModels)
        self.thermlayout = StackLayout()
        self.thermlayout.add_widget(self.PM)
        self.thermlayout.add_widget(self.SM)
        self.tp.content = self.thermlayout
        self.tp.open()


    def ThermoSelect(self,instance):
        self.Selected_thermo_model = instance.text
        self.PresentModel.text = 'Selected Model: ' + instance.text
        self.Thermodropdown.dismiss()

    def select_remove_compound(self, instance):
        self.showcomp.text = instance.text
        self.dropdown.dismiss()

class Omapp(App):

    def build(self):
        return OmWidget()

if __name__ == "__main__" :
    Omapp().run()

