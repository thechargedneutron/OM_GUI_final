import UnitOP

class Stream(UnitOP.UnitOP):
    def __init__(self,**kwargs):
        super(Stream, self).__init__(**kwargs)
        self.type = 0
        self.input_streams = {1: None}
        self.output_streams = {1: None}
        self.input_lines = {1: None}
        self.output_lines = {1: None}
        self.size_hint = (None, None)
        self.size2 = (70, 60)
        self.size = (53.33, 40)
        self.background_normal = 'Images/mat_operator.png'
        self.background_down = 'Images/mat_operator.png'
        self.connected_to = []
        self.PropertyList = ['Temperature', 'Pressure', 'Mass Flow', 'Molar Flow', 'Phase Mole Fraction']
        self.flash_spec = ['T and P', 'T and Vapor Fraction', 'P and Vapor Fraction']
        self.compound_spec = ['Molar Fractions', 'Mass Fractions']
        self.Connecting_Points_Input = []
        self.Connecting_Points_Output = []
        self.line_nos = []
        self.upward_connector_input = []
        self.downward_connector_input = []
        self.upward_connector_output = []
        self.downward_connector_output = []
        self.Connecting_Points_Output = []
        self.Connecting_Points_Input = []
        self.OM_Model = 'Mat_Stm'
        self.PropertyVal = ['50', '101.325', '100','1','0']
        self.check_stm = 0
        self.border = 0,0,0,0


    def Update_Conn_Pnts(self):
        self.Connecting_Points_Input = [self.x+8, self.y+20]
        self.Connecting_Points_Output = [self.x+48, self.y+20]
        self.upward_connector_output = [self.x+55,self.y+40]
        self.downward_connector_output = [self.x+55,self.y+0]
        self.upward_connector_input = [self.x , self.y + 40]
        self.downward_connector_input = [self.x , self.y + 0]



    def on_submit(self, instance):
        self.PropertyVal = []
        self.name = self.name_ob.text
        self.text_label.text = self.name
        UnitOP.UnitOP.drop_connections[self.name] = UnitOP.UnitOP.drop_connections[self.bef_name]
        for property in self.PropertyObj:
            self.PropertyVal.append(property.text)





