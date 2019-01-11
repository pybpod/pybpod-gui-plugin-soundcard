from AnyQt import QtGui
from AnyQt.QtWidgets import QFileDialog
from confapp import conf
from pybpodgui_api.utils.generate_sound import generate_sound
from pyforms_gui.basewidget import BaseWidget
from pyforms_gui.controls.control_base import ControlBase
from pyforms_gui.controls.control_button import ControlButton
from pyforms_gui.controls.control_combo import ControlCombo
from pyforms_gui.controls.control_emptywidget import ControlEmptyWidget
from pyforms_gui.controls.control_label import ControlLabel
from pyforms_gui.controls.control_number import ControlNumber
from pyforms_gui.controls.control_text import ControlText

from .module_api import SoundCardModule, SampleRate


class SoundGenerationPanel(ControlEmptyWidget):

    def __init__(self):
        super(SoundGenerationPanel, self).__init__()

        self._firstname = ControlText('First name', 'Default value')
        self._middlename = ControlText('Middle name')
        self._lastname = ControlText('Lastname name')
        self._fullname = ControlText('Full name')
        self._button = ControlButton('Press this button')

        # Define the organization of the forms
        # self.formset = ['_firstname', '_middlename', '_lastname', '_fullname', '_button', ' ']
        self.value = [self._firstname, self._middlename, self._lastname, self._fullname, self._button]


class SoundCardModuleGUI(SoundCardModule, BaseWidget):

    TITLE = 'Sound Card module'

    def __init__(self, parent_win=None):
        BaseWidget.__init__(self, self.TITLE, parent_win=parent_win)
        SoundCardModule.__init__(self)

        self._sound_generation = SoundGenerationPanel()

        self._sound_card = SoundCardModule()
        self._wave_int = []

        self._serial_port = ControlCombo('Serial port', changed_event=self.__combo_usb_ports_changed_evt)
        self._refresh_serials = ControlButton('',
                                              icon=QtGui.QIcon(conf.REFRESH_SMALL_ICON),
                                              default=self.__refresh_usb_ports_btn_pressed,
                                              helptext="Press here to refresh the list of available devices.")
        self._connect_btn = ControlButton('Connect', default=self.__connect_btn_pressed)
        self._filename = ControlText('Sound filename', '')
        self._saveas_btn = ControlButton('Save As...', default=self.__prompt_save_file_evt)

        self._freq_label = ControlLabel('Frequency', style='font-weight:bold;margin-left:0')
        self._freq_left = ControlNumber('Left Channel', default=10000, minimum=0, maximum=2000000)
        self._freq_right = ControlNumber('Right Channel', default=10000, minimum=0, maximum=2000000)
        self._duration = ControlNumber('Duration (s)', default=1, minimum=0, maximum=100000, decimals=2)

        self._fs = ControlCombo('Sample frequency')
        self._fs.add_item('96 KHz', SampleRate._96000HZ)
        self._fs.add_item('192 KHz', SampleRate._192000HZ)

        self._gen_btn = ControlButton('Generate sound', default=self.__generate_sound_and_save)
        self._gen_btn.enabled = False

        self.formset = [
            'h5: Sound generation',
            ('_serial_port', '_refresh_serials', '_connect_btn'),
            ('_filename', '_saveas_btn'),
            ('h5:Frequency', '_freq_left', '_freq_right'),
            '_duration',
            '_fs',
            '_gen_btn']

        self.set_margin(10)

        self._fill_usb_ports()

    def _fill_usb_ports(self):
        self._serial_port.add_item('', '')
        if self._sound_card:
            usb_devices = self._sound_card.devices
            for n, item in enumerate(usb_devices):
                item_str = item.product + ' {n} (port={port})'.format(n=n, port=item.port_number)
                self._serial_port.add_item(item_str, item)

    def __combo_usb_ports_changed_evt(self):
        # TODO: self._sound_card.close()
        self._connect_btn.enabled = True

    def __refresh_usb_ports_btn_pressed(self):
        tmp = self._serial_port.value
        self._serial_port.clear()
        self._fill_usb_ports()
        self._serial_port.value = tmp

    def __connect_btn_pressed(self):

        if not self._serial_port.value:
            self.warning("Please select a serial port before proceeding.", "No serial port selected")
            return

        self._sound_card.open(device=self._serial_port.value)

        # update some visual elements?
        self._connect_btn.enabled = False

    def __prompt_save_file_evt(self):
        """
        Opens a window for user to select where to save the sound .bin file
        """
        self._filename.value, _ = QFileDialog.getSaveFileName()
        if self._filename.value:
            self._gen_btn.enabled = True
        else:
            self._gen_btn.enabled = False

    def __generate_sound_and_save(self):
        if not self._sound_card.connected:
            self.warning("Please connect to the sound card before proceeding",
                         "No connection to the sound card established.")
            return

        if not self._filename.value:
            self.warning("Please select a destination file for the generated sound", "No sound file selected")
            return

        self._wave_int = generate_sound(self._filename.value,
                                        self._fs.value.value,  # fs.value has a Enum so we need to get the value from it
                                        self._duration.value,
                                        int(self._freq_left.value),
                                        int(self._freq_right.value),
                                        True)

        self.success("Sound file written successfully to '{filename}'".format(filename=self._filename),
                     "File written successfully")
