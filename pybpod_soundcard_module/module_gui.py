from pyforms_gui.basewidget import BaseWidget
from .module_api import SoundCardModule

class SoundCardModuleGUI(SoundCardModule, BaseWidget):

    TITLE = 'Sound Card module'

    def __init__(self, parent_win=None):
        BaseWidget.__init__(self, self.TITLE, parent_win=parent_win)
        SoundCardModule.__init__(self)


