import UnitOP

class Mixer(UnitOP.UnitOP):
    def __init__(self,**kwargs):
        super(Mixer, self).__init__(**kwargs)
        self.type = 1
        self.stream_count = [6, 1]
        self.input_streams = {1: None, 2: None, 3: None, 4: None, 5: None, 6:None}
        self.output_streams = {1: None}
        self.input_lines = {1: None, 2: None, 3: None, 4: None, 5: None, 6: None}
        self.output_lines = {1: None}
        self.size_hint = (None, None)
        # self.size2 = (60, 115.75)
        # self.size = (52, 87)
        self.size2 = (140,150)
        self.size = (130,130)
        self.background_normal = 'Images/mixer_operator.png'
        self.PropertyListInput = ['INPUT 1','INPUT 2','INPUT 3','INPUT 4','INPUT 5','INPUT 6']
        self.PropertyListOutput = ['OUTPUT']
        self.Connecting_Points_Input = []
        self.Connecting_Points_Output = []
        self.line_nos = []
        self.border= 0,0,0,0
        self.OM_Model = 'Mixer'
        self.PropertyVal = ['', '', '']
    def Update_Conn_Pnts(self):
        self.Connecting_Points_Input = [[self.x+40, self.y + 101], [self.x+40, self.y + 86], [self.x+40, self.y + 71], [self.x+40, self.y + 56],[self.x+40, self.y + 41], [self.x+40, self.y + 26]]
        self.Connecting_Points_Output = [[self.x + 100, self.y + 66]]


    def on_submit(self, instance):
        self.Connecting_Points_Input = [[self.x+40, self.y + 101], [self.x+40, self.y + 86], [self.x+40, self.y + 71], [self.x+40, self.y + 56], [self.x+40, self.y + 41], [self.x+40, self.y + 26]]
        self.Connecting_Points_Output = [[self.x + 100, self.y + 66]]
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
            if Property.text != 'None':
                self.input_streams[val] = self.all_operators[self.drop_connections[Property.text]]
            val +=1

        val = 1;
        for Property in self.MainButtonOutput:
            if Property.text != 'None':
                self.output_streams[val] = self.all_operators[self.drop_connections[Property.text]]
            val +=1

        # if self.connected == False:
        self.connect = self.connect + 1





