import UnitOP

class Stream(UnitOP.UnitOP):
    def __init__(self,**kwargs):
        super(Stream, self).__init__(**kwargs)
        self.input_streams = {1: None}
        self.output_streams = {1: None}
        self.input_lines = {1: None}
        self.output_lines = {1: None}
        self.size_hint = (None, None)
        self.size2 = (80, 70)
        self.size = (70, 52.5)
        self.background_normal = 'Images/mat_operator.png'
        self.connected_to = []
        self.PropertyList = ['Temperature', 'Pressure', 'Flow Rate','Mass Flow', 'Molar Flow', 'Volumetric Flow','Specific Enthalpy','Specific Entropy','Phase Mole Fraction']
        self.Connecting_Points_Input = []
        self.Connecting_Points_Output = []
        self.line_nos = []
        self.OM_Model = 'Mat_Stm'
        self.PropertyVal = ['50', '101.325', '100','1','0','0','0','','']
        self.check_stm = 0

    def Update_Conn_Pnts(self):
        self.Connecting_Points_Input = [self.x+18, self.y+26]
        self.Connecting_Points_Output = [self.x+52, self.y+26]


    def on_submit(self, instance):
        self.PropertyVal = []
        self.name = self.name_ob.text
        self.text_label.text = self.name
        UnitOP.UnitOP.drop_connections[self.name] = UnitOP.UnitOP.drop_connections[self.bef_name]
        for property in self.PropertyObj:
            self.PropertyVal.append(property.text)
        print self.PropertyVal




