import UnitOP

class Stream(UnitOP.UnitOP):
    def __init__(self,**kwargs):
        super(Stream, self).__init__(**kwargs)
        self.size = (30, 15)
        self.background_normal = 'MatStm.png'
        self.connected_to = []
        self.PropertyList = ['TEMPERATURE', 'PRESSURE', 'FLOWRATE']
        self.Connecting_Points = []
        self.line_nos = []
        self.OM_Model = 'Mat_Stm'
        self.PropertyVal = ['50', '101.325', '100']

    def Update_Conn_Pnts(self):
        self.Connecting_Points = [[self.x+30,self.y+(15/2)],[self.x+30,self.y+(15/2)],[self.x+30,self.y+(15/2)]]

    def on_submit(self, instance):
        self.PropertyVal = []
        for property in self.PropertyObj:
            self.PropertyVal.append(property.text)
        print self.PropertyVal




