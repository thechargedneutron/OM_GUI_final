from kivy.uix.button import Button
from kivy.properties import NumericProperty
from UnitOP import UnitOP
from Mixer import Mixer
from MatStrm import Stream
from Flash import Flash

class SMixer(Button):
    included = NumericProperty(0)
    UO = Mixer
    def __init__(self, **kwargs):
        super(SMixer, self).__init__(**kwargs)
        self.size_hint = None, None
        self.width = 150
        self.height = 103
        self.background_normal = 'Images/mixer_new.png'
        self.background_down = 'Images/mixer_new.png'

class SMatStrm(Button):
    included = NumericProperty(0)
    UO = Stream
    def __init__(self, **kwargs):
        super(SMatStrm, self).__init__(**kwargs)
        self.size_hint = None, None
        self.width = 150
        self.height = 90

        self.background_normal = 'Images/mat_strm_new.png'
        self.background_down = 'Images/mat_strm_new.png'

class SFlash(Button):
    included = NumericProperty(0)
    UO = Flash
    def __init__(self, **kwargs):
        super(SFlash, self).__init__(**kwargs)
        self.width = 150
        self.height = 103
        self.size_hint = None, None
        self.background_normal = 'Images/flash_new.png'
        self.background_down = 'Images/flash_new.png'


