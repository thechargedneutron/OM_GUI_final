import UnitOP

class Mixer(UnitOP.UnitOP):
    def __init__(self,**kwargs):
        super(Mixer, self).__init__(**kwargs)
        self.stream_count = [6, 1]
        self.input_streams = {1: None, 2: None, 3: None, 4: None, 5: None, 6:None}
        self.output_streams = {1: None}
        self.input_lines = {1: None, 2: None, 3: None, 4: None, 5: None, 6: None}
        self.output_lines = {1: None}
        self.size_hint = (None, None)
        self.size2 = (60, 115.75)
        self.size = (52, 87)
        self.background_normal = 'Mixer1.png'
        self.PropertyListInput = ['INPUT 1','INPUT 2','INPUT 3','INPUT 4','INPUT 5','INPUT 6']
        self.PropertyListOutput = ['OUTPUT']
        self.Connecting_Points_Input = []
        self.Connecting_Points_Output = []
        self.line_nos = []
        self.OM_Model = 'Mixer'
        self.PropertyVal = ['', '', '']
    def Update_Conn_Pnts(self):
        self.Connecting_Points_Input = [[self.x, self.y + 81], [self.x, self.y + 66], [self.x, self.y + 51], [self.x, self.y + 36],[self.x, self.y + 21], [self.x, self.y + 6]]
        self.Connecting_Points_Output = [[self.x + 52, self.y + (87 / 2)]]

    def on_submit(self, instance):
        self.Connecting_Points_Input = [[self.x, self.y + 81], [self.x, self.y + 66], [self.x, self.y + 51], [self.x, self.y + 36], [self.x, self.y + 21], [self.x, self.y + 6]]
        self.Connecting_Points_Output = [[self.x + 52, self.y + (87 / 2)]]
        self.name = self.name_ob.text
        self.text_label.text = self.name
        UnitOP.UnitOP.drop_connections[self.name] = UnitOP.UnitOP.drop_connections[self.bef_name]
        val = 1;
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
        for Property in self.MainButtonInput:
            if Property.text != "Select":
                self.input_streams[val] = self.all_operators[self.drop_connections[Property.text]]
            val +=1
        print self.input_streams
        val = 1;
        for Property in self.MainButtonOutput:
            if Property.text != "Select":
                self.output_streams[val] = self.all_operators[self.drop_connections[Property.text]]
            val +=1
        print self.output_streams
        # if self.connected == False:
        self.connect = self.connect + 1





