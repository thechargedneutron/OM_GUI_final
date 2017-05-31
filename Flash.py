import UnitOP

class Flash(UnitOP.UnitOP):
    def __init__(self,**kwargs):
        super(Flash, self).__init__(**kwargs)
        self.size = (50, 134)
        self.background_normal = 'Flash.png'
        self.PropertyList = ['INPUT 1','INPUT 2','OUTPUT 1','OUTPUT 2']
        self.connected_to = []
        self.Connecting_Points = []
        self.line_nos = []
        self.OM_Model = 'Flash'
        self.PropertyVal = ['', '', '', '']

    def Update_Conn_Pnts(self):
        self.Connecting_Points = [[self.x,self.y+14], [self.x, self.y+120], [self.x+52, self.y+14], [self.x+52, self.y+120]]

    def on_submit(self, instance):
        self.Connecting_Points = [[self.x,self.y+14], [self.x, self.y+120], [self.x+52, self.y+14], [self.x+52, self.y+120]]
        self.name = self.name_ob.text
        UnitOP.UnitOP.drop_connections[self.name] = UnitOP.UnitOP.drop_connections[self.bef_name]
        for Property in self.MainButton:
            self.connected_to.append(self.drop_connections[Property.text])
            self.PropertyVal.append(self.drop_connections[Property.text])
            print self.connected_to
        if self.connected == False:
            self.connect = self.connect + 1





