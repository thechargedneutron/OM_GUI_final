import UnitOP

class Flash(UnitOP.UnitOP):
    def __init__(self,**kwargs):
        super(Flash, self).__init__(**kwargs)
        self.stream_count = [2, 2]
        self.input_lines = {1: None, 2: None}
        self.output_lines = {1: None, 2: None}
        self.input_streams = {1: None, 2: None}
        self.output_streams = {1: None, 2: None}
        self.size_hint = (None, None)
        self.size2 = (140, 175)
        self.size = (130, 151.6)
        self.background_normal = 'Images/flash_operator.png'
        self.PropertyListInput = ['INPUT 1','INPUT 2']
        self.PropertyListOutput = ['OUTPUT 1', 'OUTPUT 2']
        self.Connecting_Points_Input = []
        self.Connecting_Points_Output = []
        self.line_nos = []
        self.OM_Model = 'Flash'
        self.PropertyVal = ['', '', '', '']

    def Update_Conn_Pnts(self):
        self.Connecting_Points_Input = [[self.x+43, self.y+110],[self.x+43,self.y+44]]
        self.Connecting_Points_Output = [ [self.x+87, self.y+110],[self.x+87, self.y+44]]

    def on_submit(self, instance):
        self.Connecting_Points_Input = [[self.x+43, self.y + 110], [self.x+43, self.y + 44]]
        self.Connecting_Points_Output = [[self.x + 87, self.y + 110], [self.x+87, self.y + 44]]
        self.name = self.name_ob.text
        self.text_label.text = self.name
        UnitOP.UnitOP.drop_connections[self.name] = UnitOP.UnitOP.drop_connections[self.bef_name]
        for key in self.input_streams:
            if self.input_streams[key]:
                self.input_streams[key].output_streams[1] = None
                self.input_streams[key].output_lines[1] = None
                self.input_streams[key] = None
        for key in self.output_streams:
            if self.output_streams[key]:
                self.output_streams[key].input_streams[1] = None
                self.output_streams[key].input_lines[1] = None
                self.output_streams[key] = None
        val = 1;
        for Property in self.MainButtonInput:
            if Property.text != "Select":
                self.input_streams[val] = self.all_operators[self.drop_connections[Property.text]]
            val += 1
        print self.input_streams
        val = 1;
        for Property in self.MainButtonOutput:
            if Property.text != "Select":
                self.output_streams[val] = self.all_operators[self.drop_connections[Property.text]]
            val += 1
        self.connect = self.connect + 1





