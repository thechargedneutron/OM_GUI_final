import UnitOP

class Flash(UnitOP.UnitOP):
    def __init__(self,**kwargs):
        super(Flash, self).__init__(**kwargs)
        self.size = (50, 134)
        self.background_normal = 'Flash.png'
        self.PropertyList = ['INPUT1','INPUT2','OUTPUT1','OUTPUT2']
        self.connected_to = []
        self.Connecting_Points = []
        self.line_nos = []
        self.OM_Model = 'Flash'
        self.PropertyVal = ['', '', '', '']

    def Update_Conn_Pnts(self):
        self.Connecting_Points = [[self.x,self.y+14], [self.x, self.y+120], [self.x+52, self.y+14], [self.x+52, self.y+120]]

    def on_submit(self, instance):
        self.Connecting_Points = [[self.x,self.y+14], [self.x, self.y+120], [self.x+52, self.y+14], [self.x+52, self.y+120]]
        for Property in self.PropertyObj:
            self.connected_to.append(int(Property.text))
            self.PropertyVal.append(Property.text)
            print self.connected_to
        if self.connected == False:
            self.connect = self.connect + 1





